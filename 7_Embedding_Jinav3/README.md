# Locust Stress Test - Jina Embeddings v3 API

Test suite cho stress testing API embeddings của Jina v3.

## 📁 Cấu Trúc Project

```
7_Embedding_Jinav3/
├── src/
│   ├── locustfile.py          # File chính chứa Locust tasks
│   ├── config.py              # Configuration và constants
│   ├── data_generators.py     # Classes generate test data
│   ├── test_embeddings_api.py # Script test đơn giản cho /v1/embeddings
│   └── requirements.txt       # Python dependencies
└── README.md                  # Documentation này
```

## 🚀 Cài Đặt

1. Cài đặt dependencies:
```powershell
cd src
pip install -r requirements.txt
```

## 📊 API Endpoint được Test

### POST /v1/embeddings
- **Mục đích**: Tạo embeddings từ text input
- **Payload**: Chứa `model` và `input` (text string)
- **Model mặc định**: `jinaai/jina-embeddings-v3`

## 🎯 Ví dụ curl Command

```bash
curl --location 'http://103.253.20.30:8080/v1/embeddings' \
--header 'Content-Type: application/json' \
--data '{"model": "jinaai/jina-embeddings-v3", "input": "hello world"}'
```

## 🧪 Chạy Script Test Đơn Giản

```powershell
cd src
python test_embeddings_api.py
```

Script này sẽ:
- Tạo payload mẫu
- Gửi request đến API
- In kết quả response
- Hiển thị lỗi nếu có

## 🏃 Chạy Locust Stress Test

### Cách 1: Chạy với Web UI (Recommended)

```powershell
cd src
locust -f locustfile.py --host=http://103.253.20.30:8080
```

Sau đó mở browser tại: **http://localhost:8089**

### Cách 2: Chạy Headless (Không có UI)

```powershell
cd src
locust -f locustfile.py --host=http://103.253.20.30:8080 --headless -u 100 -r 10 -t 60s
```

**Parameters:**
- `-u 100`: 100 concurrent users
- `-r 10`: Spawn rate 10 users/second
- `-t 60s`: Chạy trong 60 giây

## ⚙️ Cấu Hình

### Qua file `.env` (tạo ở thư mục `7_Embedding_Jinav3/`):

```env
# Base URL
EMBEDDINGS_API_BASE_URL=http://103.253.20.30:8080

# Endpoint
EMBEDDINGS_ENDPOINT=/v1/embeddings

# Model name
EMBEDDINGS_MODEL_NAME=jinaai/jina-embeddings-v3

# Wait time giữa các requests (giây)
EMBEDDINGS_WAIT_MIN=0.5
EMBEDDINGS_WAIT_MAX=2.0
```

### Cấu hình trong `config.py`:

Tất cả các tham số có thể được override qua `.env` file. Nếu không có `.env`, sẽ dùng giá trị mặc định trong `config.py`.

## 📝 Notes

- **Base URL mặc định**: `http://103.253.20.30:8080`
- **Wait time**: 0.5-2 giây giữa các requests (có thể config)
- **Model**: `jinaai/jina-embeddings-v3` (có thể config)
- **Input texts**: Script sử dụng sample texts (tiếng Anh và tiếng Việt) để test
- **Error handling**: Tất cả errors đều được log và báo cáo

## 🔧 Troubleshooting

### Lỗi kết nối
- Kiểm tra server có đang chạy không
- Kiểm tra URL và port có đúng không
- Kiểm tra firewall có chặn không

### Lỗi import module
- Đảm bảo đã cài đặt dependencies: `pip install -r requirements.txt`
- Đảm bảo đang ở đúng thư mục `src/` khi chạy scripts

### Lỗi response
- Kiểm tra format payload có đúng không
- Kiểm tra API server logs
- Kiểm tra status code và error message trong response
- Kiểm tra model name có đúng không

## 📊 Kết Quả Mong Đợi

Locust sẽ báo cáo:
- **Total Requests**: Tổng số requests đã gửi
- **Requests/sec (RPS)**: Số requests mỗi giây
- **Response Time**: Thời gian phản hồi (min, max, median, p95, p99)
- **Number of failures**: Số requests thất bại
- **Response time distribution**: Phân bổ thời gian phản hồi

## 🎯 Mục Đích Test

Test này được thiết kế để:
- Bắn hàng trăm/thousands requests đến API embeddings
- Kiểm tra performance và stability của API
- Tìm ra giới hạn của server
- Đo response time dưới tải đồng thời



