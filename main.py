import time
import random
import numpy as np
import pandas as pd
import tensorflow as tf

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, Summary, generate_latest, CONTENT_TYPE_LATEST
from logging_config import logger

from model import create_model
from preprocess_data import (
    add_remaining_useful_life,
    prep_data,
    gen_test_data,
)

# Thiết lập seed giống file gốc
seed = 42
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)

app = FastAPI()

# Định nghĩa Params giữ nguyên file gốc
class Params(BaseModel):
    sensor_2: float = 445.0
    sensor_3: float = 549.68
    sensor_4: float = 1343.43
    sensor_7: float = 1112.93
    sensor_8: float = 3.91
    sensor_9: float = 5.7
    sensor_11: float = 137.36
    sensor_12: float = 2211.86
    sensor_13: float = 8311.32
    sensor_14: float = 1.01
    sensor_15: float = 41.69
    sensor_17: float = 129.78
    sensor_20: float = 2387.99
    sensor_21: float = 8074.83

# Các metric cho API và model
REQUESTS = Counter('api_requests_total', 'HTTP requests total', ['method', 'endpoint', 'status'])
LATENCY = Histogram('api_latency_seconds', 'Request latency', ['endpoint'])
INFERENCE_TIME = Summary('model_inference_seconds', 'Time for model inference')
BAD_CONF = Counter('model_confidence_below_threshold', 'Low-confidence predictions')

# Thông số giữ nguyên file gốc
index_names = ['unit_nr', 'time_cycles']
setting_names = ['setting_1', 'setting_2', 'setting_3']
sensor_names = ['s_{}'.format(i+1) for i in range(21)]
col_names = index_names + setting_names + sensor_names
remaining_sensors = ['s_2','s_3','s_4','s_7','s_8','s_9','s_11','s_12','s_13','s_14','s_15','s_17','s_20','s_21']
drop_sensors = [s for s in sensor_names if s not in remaining_sensors]
sequence_length, alpha = 30, 0.1
input_shape = (sequence_length, len(remaining_sensors))

# Load model giống file gốc
file_weight = 'fd004_model.weights.h5'
model = create_model(
    input_shape,
    nodes_per_layer=[256],
    dropout=0.1,
    activation='sigmoid',
    weights_file=file_weight
)
model.load_weights('final_model.weights.h5')

# Chuẩn bị dữ liệu train giống file gốc
train = pd.read_csv('train_FD004.txt', sep='\s+', header=None, names=col_names)
train = add_remaining_useful_life(train)
train['RUL'] = train['RUL'].clip(upper=125)

# Middleware để đo API metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    REQUESTS.labels(request.method, request.url.path, response.status_code).inc()
    LATENCY.labels(request.url.path).observe(duration)
    return response

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post('/predict')
async def predict(params: Params):
    try:
        # Tạo dict sensor theo file gốc
        sensor_values = dict(zip(remaining_sensors, list(params.dict().values())))
        # Danh sách đầy đủ sensors
        sensor_values_list = [sensor_values.get(sensor, 0.0) for sensor in sensor_names]
        # Giá trị mặc định giống file gốc
        unit_nr, time_cycles, setting_1, setting_2, setting_3 = 1, 1, 20.0072, 0.7, 100.0
        value = [unit_nr, time_cycles, setting_1, setting_2, setting_3] + sensor_values_list
        # Tạo DataFrame như file gốc
        input_test = pd.DataFrame([value], columns=col_names)

        # Xử lý dữ liệu
        X_train_interim, X_test_interim = prep_data(
            train, input_test, drop_sensors, remaining_sensors, alpha
        )
        test_gen = list(gen_test_data(X_test_interim, sequence_length, remaining_sensors, -99.))
        test_array = np.array(test_gen, dtype=np.float32)

        # Inference và đo thời gian
        start_inf = time.time()
        y_hat = model.predict(test_array)
        inf_time = time.time() - start_inf
        INFERENCE_TIME.observe(inf_time)

        # Lấy kết quả và giám sát confidence
        rul_pred = float(y_hat[0][0])
        if rul_pred < 0.6:
            BAD_CONF.inc()
            logger.warning(f"Low confidence: {rul_pred}")
        logger.info(f"Inference took {inf_time:.3f}s, RUL={rul_pred:.2f}")

        return {
            'message': 'Successfully predicted',
            'input shape': str(test_array.shape),
            'sequence length': sequence_length,
            'num features': test_array.shape[2],
            'Remaining Useful Life (RUL) prediction': f"{rul_pred:.2f}"  
        }
    except Exception as e:
        logger.exception("Error in /predict")
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/metrics')
async def metrics():
    data = generate_latest()
    return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)