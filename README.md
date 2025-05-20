# Remaining Useful Life (RUL) Prediction Service

Đây là hệ thống dự đoán tuổi thọ còn lại (RUL) cho thiết bị sử dụng mô hình học máy LSTM và được triển khai thông qua FastAPI.

## Môi trường yêu cầu

- Python 3.10
- Docker và Docker Compose (nếu muốn triển khai với Docker)

## Cài đặt và sử dụng

### Phương pháp 1: Sử dụng môi trường ảo Python

1. **Tạo môi trường ảo**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Linux/Mac
   # hoặc
   venv\Scripts\activate  # Trên Windows
   ```

2. **Cài đặt các thư viện phụ thuộc**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy ứng dụng**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 15000
   ```

### Phương pháp 2: Sử dụng Docker

1. **Xây dựng và khởi chạy container với Docker Compose**:

   ```bash
   docker-compose up --build
   ```

   Hoặc chạy ở chế độ nền:

   ```bash
   docker-compose up --build -d
   ```

2. **Dừng container**:
   ```bash
   docker-compose down
   ```

### Phương pháp 3: Xây dựng và chạy Docker image thủ công

1. **Xây dựng Docker image**:

   ```bash
   docker build -t rul-prediction-service .
   ```

2. **Chạy container**:
   ```bash
   docker run -p 15000:15000 --name rul-prediction-service rul-prediction-service
   ```

## Sử dụng API

Sau khi khởi chạy, API có thể được truy cập tại địa chỉ: `http://localhost:15000`

### Endpoints

1. **Kiểm tra trạng thái**:

   ```
   GET /
   ```

   Trả về thông báo "Hellow World" nếu API đang chạy.

2. **Dự đoán RUL**:

   ```
   POST /predict
   ```

   Body request mẫu (JSON):

   ```json
   {
   	"sensor_2": 445.0,
   	"sensor_3": 549.68,
   	"sensor_4": 1343.43,
   	"sensor_7": 1112.93,
   	"sensor_8": 3.91,
   	"sensor_9": 5.7,
   	"sensor_11": 137.36,
   	"sensor_12": 2211.86,
   	"sensor_13": 8311.32,
   	"sensor_14": 1.01,
   	"sensor_15": 41.69,
   	"sensor_17": 129.78,
   	"sensor_20": 2387.99,
   	"sensor_21": 8074.83
   }
   ```

## Cấu trúc dự án

- `main.py`: Mã nguồn chính của API FastAPI
- `model.py`: Định nghĩa mô hình LSTM
- `preprocess_data.py`: Mã tiền xử lý dữ liệu
- `requirements.txt`: Danh sách các thư viện phụ thuộc với phiên bản cụ thể
- `Dockerfile`: Cấu hình để xây dựng Docker image
- `docker-compose.yml`: Cấu hình để quản lý container Docker
- `final_model.weights.h5`: File trọng số đã được huấn luyện của mô hình
- `train_FD004.txt`: Dữ liệu huấn luyện

## Lưu ý

- Dự án này sử dụng các phiên bản cụ thể của các thư viện để đảm bảo tính tương thích và ổn định. Không nên thay đổi phiên bản các thư viện trong `requirements.txt` trừ khi có lý do đặc biệt.
- Mô hình đã được huấn luyện sẵn và được lưu trong file `final_model.weights.h5`.
- API chạy mặc định trên cổng 15000. Có thể thay đổi bằng cách chỉnh sửa file `Dockerfile` và `docker-compose.yml`.

## Hướng dẫn sử dụng API với curl

```bash
curl -X POST "http://localhost:15000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_2": 445.0,
    "sensor_3": 549.68,
    "sensor_4": 1343.43,
    "sensor_7": 1112.93,
    "sensor_8": 3.91,
    "sensor_9": 5.7,
    "sensor_11": 137.36,
    "sensor_12": 2211.86,
    "sensor_13": 8311.32,
    "sensor_14": 1.01,
    "sensor_15": 41.69,
    "sensor_17": 129.78,
    "sensor_20": 2387.99,
    "sensor_21": 8074.83
  }'
```

## Video

[![Watch the video](https://drive.google.com/file/d/1b-6QSMeDsWP5ku0DculEdSMrVSiMaQhN/view?usp=sharing)](https://drive.google.com/file/d/1b-6QSMeDsWP5ku0DculEdSMrVSiMaQhN/view?usp=sharing)
