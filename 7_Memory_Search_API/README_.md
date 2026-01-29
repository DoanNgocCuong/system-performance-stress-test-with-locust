# Locust Stress Test - Memories và Search API

Test suite cho stress testing các API Memories và Search.

## 📁 Cấu Trúc Project

```
7_Memories_Search_API/
├── src/
│   ├── locustfile.py          # File chính chứa Locust tasks
│   ├── config.py              # Configuration và constants
│   ├── data_generators.py     # Classes generate test data
│   ├── test_memories_api.py   # Script test đơn giản cho /memories
│   ├── test_search_api.py     # Script test đơn giản cho /search
│   └── requirements.txt       # Python dependencies
└── README.md                  # Documentation này
```

## 🚀 Cài Đặt

1. Cài đặt dependencies:
```powershell
cd src
pip install -r requirements.txt
```

## 📊 API Endpoints được Test

### 1. POST /memories
- **Mục đích**: Lưu trữ messages với user_id, run_id, và messages array
- **Payload**: Chứa user_id, run_id, và messages array (với role và content)
- **Weight**: 1 (có thể điều chỉnh trong `config.py`)
- **Messages Length**: Mặc định 100-200 turns (messages) để test với conversation dài và phức tạp

### 2. POST /search
- **Mục đích**: Tìm kiếm với query, user_id, top_k, limit, score_threshold
- **Payload**: Chứa query, user_id, top_k, limit, score_threshold
- **Weight**: 1 (có thể điều chỉnh trong `config.py`)

## 🎯 Ví dụ curl Commands

### API /memories

```bash
curl --location 'http://103.253.20.30:8889/memories' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": "Nguyễn Minh Phúc",
    "run_id": "run_1",
    "messages": [
        {
            "content": "<emotion type=\"excited\"/> Chào cậu, tớ là Pika đây! <emotion type=\"happy\"/> Cuối tuần vừa rồi tớ đã được đi chơi ở một hành tinh có rất nhiều kẹo mút. <emotion type=\"curious\"/> Thế cuối tuần của cậu thì sao?",
            "role": "assistant"
        },
        {
            "content": " Michael Buzzell",
            "role": "user"
        }
    ]
}'
```

### API /search

```bash
curl --location 'http://103.253.20.30:8889/search' \
--header 'Content-Type: application/json' \
--data '{
    "query": "Sở thích",
    "user_id": "Đoàn Ngọc Cường",
    "top_k": 3,
    "limit": 10,
    "score_threshold": 0.7
}'
```

## 🧪 Chạy Script Test Đơn Giản

### Test API /memories

```powershell
cd src
python test_memories_api.py
```

### Test API /search

```powershell
cd src
python test_search_api.py
```

Các script này sẽ:
- Tạo payload mẫu
- Gửi request đến API
- In kết quả response
- Hiển thị lỗi nếu có

## 🏃 Chạy Locust Stress Test

### Cách 1: Chạy với Web UI (Recommended)

```powershell
cd src
locust -f locustfile.py --host=http://103.253.20.30:8889
```

Sau đó mở browser tại: **http://localhost:8089**

### Cách 2: Chạy Headless (Không có UI)

```powershell
cd src
locust -f locustfile.py --host=http://103.253.20.30:8889 --headless -u 100 -r 10 -t 60s
```

**Parameters:**
- `-u 100`: 100 concurrent users
- `-r 10`: Spawn rate 10 users/second
- `-t 60s`: Chạy trong 60 giây

## ⚙️ Cấu Hình

### Qua file `.env` (tạo ở thư mục `7_Memories_Search_API/`):

```env
# Base URL
MEMORIES_API_BASE_URL=http://103.253.20.30:8889

# Search API Parameters
SEARCH_TOP_K=3
SEARCH_LIMIT=10
SEARCH_SCORE_THRESHOLD=0.7

# Locust Wait Time (giây)
WAIT_TIME_MIN=1.0
WAIT_TIME_MAX=3.0

# Task Weights
WEIGHT_MEMORIES=1
WEIGHT_SEARCH=1
```

### Cấu hình trong `config.py`:

Tất cả các tham số có thể được override qua `.env` file. Nếu không có `.env`, sẽ dùng giá trị mặc định trong `config.py`.

### Cấu hình Messages Turns (cho Memories API):

```env
# Số lượng messages turns cho Memories API (mặc định: 100-200)
MIN_MESSAGES_TURNS=100
MAX_MESSAGES_TURNS=200
```

**Lưu ý:**
- Mặc định: 100-200 turns để test với conversation dài và phức tạp
- Mỗi request sẽ có số lượng messages ngẫu nhiên trong khoảng này
- Script test đơn giản (`test_memories_api.py`) có option để dùng conversation ngắn hơn (5-10 turns) cho test nhanh

## 📝 Notes

- **Base URL mặc định**: `http://103.253.20.30:8889`
- **Wait time**: 1-3 giây giữa các requests (có thể config)
- **Task weights**: Mặc định cả 2 APIs có weight = 1 (50:50)
- **Sample data**: Scripts sử dụng sample data từ user query
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

