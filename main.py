from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import create_model
import numpy as np 
import tensorflow as tf
import random 
import pandas as pd 
from preprocess_data import add_remaining_useful_life, prep_data, gen_data_wrapper, gen_label_wrapper, gen_test_data, evaluate

seed = 42
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)

# First sample
# {
#   "sensor_2": 445.0,
#   "sensor_3": 549.68,
#   "sensor_4": 1343.43,
#   "sensor_7": 1112.93,
#   "sensor_8": 3.91,
#   "sensor_9": 5.7,
#   "sensor_11": 137.36,
#   "sensor_12": 2211.86,
#   "sensor_13": 8311.32,
#   "sensor_14": 1.01,
#   "sensor_15": 41.69,
#   "sensor_17": 129.78,
#   "sensor_20": 2387.99,
#   "sensor_21": 8074.83
# }

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

app = FastAPI()

index_names = ['unit_nr', 'time_cycles']
setting_names = ['setting_1', 'setting_2', 'setting_3']
sensor_names = ['s_{}'.format(i+1) for i in range(0,21)]
col_names = index_names + setting_names + sensor_names

remaining_sensors = ['s_2', 's_3', 's_4', 's_7', 's_8', 's_9',
       's_11', 's_12', 's_13', 's_14', 's_15', 's_17', 's_20', 's_21']
drop_sensors = [element for element in sensor_names if element not in remaining_sensors]
sequence_length, alpha = 30, 0.1
input_shape = (sequence_length, len(remaining_sensors))
# Declare default model 
file_weight = 'fd004_model.weights.h5'
model = create_model(input_shape, nodes_per_layer=[256], dropout=0.1, activation='sigmoid', weights_file=file_weight)
model.load_weights('final_model.weights.h5')

# Declare some default values for test 
value = []
unit_nr, time_cycles, setting_1, setting_2, setting_3 = 1, 1, 20.0072, 0.7, 100.0
columns = ['unit_nr', 'time_cycles', 'setting_1', 'setting_2', 'setting_3'] + sensor_names

# Read file train 
train = pd.read_csv('train_FD004.txt', sep='\s+', header=None, names=col_names)
train = add_remaining_useful_life(train)
train['RUL'] = train['RUL'].clip(upper=125)


@app.get('/')
async def root():
    return {'message': 'Hellow World'}

@app.post('/predict')
async def predict(params:Params):
    try: 
        sensor_values = dict(zip(remaining_sensors, list(params.dict().values())))
        sensor_values_list = [sensor_values.get(sensor, 0.0) for sensor in sensor_names]
        value = [unit_nr, time_cycles, setting_1, setting_2, setting_3] + sensor_values_list
        # Create datafame for value 
        input_test = pd.DataFrame(data=[value], columns=columns)
        # Processing data
        X_train_interim, X_test_interim = prep_data(train, input_test, drop_sensors, remaining_sensors, alpha)
        test_gen = list(gen_test_data(X_test_interim, sequence_length, remaining_sensors, -99.))
        test_array = np.array(test_gen).astype(np.float32)

        # Predict 
        y_hat_test = model.predict(test_array)
        
        return {'message': 'Successfully predicted', 
                'input shape': str(test_array.shape), 
                'sequence length': int(sequence_length),
                'num features': int(test_array.shape[2]),
                'Remaining Useful Life (RUL) prediction': f"{float(y_hat_test[0][0]):.2f}"}
    except Exception as e: 
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
