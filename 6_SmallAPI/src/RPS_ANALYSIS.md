# 📊 Phân Tích RPS: 100 Users → 48 RPS

## 🔍 Vấn Đề

**Thực tế:**
- 100 CCU (Concurrent Users)
- P99 Response Time = 69ms (rất nhanh!)
- RPS = 48 (thấp hơn mong đợi)

**Lý thuyết (nếu không có wait_time):**
```
RPS ≈ 100 / 0.069 ≈ 1450 RPS
```

**Thực tế:**
```
RPS = 48 RPS
```

## ✅ Nguyên Nhân: WAIT_TIME

### Tính Toán

```
Mỗi vòng = Response Time + Wait Time
         = 0.069 + ~2.0
         = ~2.069 giây

RPS = 100 / 2.069 ≈ 48 RPS ✅
```

**Kết luận:** Đúng là do `wait_time` trong code!

### Cấu Hình Hiện Tại

```python
# config.py
WAIT_TIME_MIN = 1.0  # giây
WAIT_TIME_MAX = 3.0  # giây
# Trung bình = 2.0 giây
```

```python
# locustfile.py
wait_time = between(Config.WAIT_TIME_MIN, Config.WAIT_TIME_MAX)
# = between(1.0, 3.0) giây
```

## 📈 So Sánh

| Scenario | Response Time | Wait Time | Mỗi Vòng | RPS (100 users) |
|----------|---------------|-----------|----------|-----------------|
| **Hiện tại** | 69ms | 1-3s (avg 2s) | ~2.07s | **48 RPS** |
| Không wait | 69ms | 0s | 0.069s | ~1450 RPS |
| Wait thấp | 69ms | 0.1-0.3s (avg 0.2s) | 0.27s | ~370 RPS |
| Wait rất thấp | 69ms | 0.01-0.05s (avg 0.03s) | 0.1s | ~1000 RPS |

## 🎯 Tại Sao Có Wait Time?

### Ưu Điểm (Load Test Thực Tế)
- ✅ **Mô phỏng user thật**: User không gửi request liên tục
- ✅ **Ổn định hệ thống**: Không ép server quá mức
- ✅ **Test thực tế**: Phản ánh hành vi user thật

### Nhược Điểm (Stress Test)
- ❌ **RPS thấp**: Không tận dụng hết khả năng server
- ❌ **Không ép được giới hạn**: Khó tìm điểm break của hệ thống

## 🔧 Cách Điều Chỉnh

### Option 1: Giảm Wait Time (Tăng RPS)

**Mục đích:** Stress test, ép server xử lý tối đa

```python
# config.py hoặc .env
QWEN_API_WAIT_MIN=0.01
QWEN_API_WAIT_MAX=0.1

# Kết quả:
# RPS ≈ 100 / (0.069 + 0.055) ≈ 800 RPS
```

### Option 2: Loại Bỏ Wait Time (RPS Tối Đa)

**Mục đích:** Tìm giới hạn tuyệt đối của server

```python
# config.py
WAIT_TIME_MIN=0.0
WAIT_TIME_MAX=0.0

# hoặc trong locustfile.py
wait_time = constant(0)  # Không chờ

# Kết quả:
# RPS ≈ 100 / 0.069 ≈ 1450 RPS (lý thuyết)
# ⚠️ Cảnh báo: Server có thể bị quá tải!
```

### Option 3: Giữ Wait Time (Load Test)

**Mục đích:** Test thực tế, mô phỏng user thật

```python
# Giữ nguyên
WAIT_TIME_MIN=1.0
WAIT_TIME_MAX=3.0

# RPS ≈ 48 RPS (như hiện tại)
```

## 📊 Bảng Đề Xuất

| Mục Đích | Wait Time | RPS (100 users) | Khi Nào Dùng |
|----------|-----------|-----------------|--------------|
| **Load Test** | 1-3s | ~48 RPS | ✅ Hiện tại - Test thực tế |
| **Stress Test** | 0.1-0.5s | ~200-500 RPS | Tìm điểm break |
| **Performance Test** | 0.01-0.1s | ~800-1000 RPS | Tìm giới hạn |
| **Max Stress** | 0s | ~1450 RPS | ⚠️ Ép tối đa (nguy hiểm) |

## ⚠️ Lưu Ý Khi Giảm Wait Time

1. **Server có thể quá tải:**
   - Response time tăng
   - Error rate tăng
   - Có thể crash

2. **Monitoring quan trọng:**
   - Theo dõi response time
   - Theo dõi error rate
   - Theo dõi CPU/Memory server

3. **Tăng dần:**
   - Bắt đầu với wait_time = 0.5s
   - Giảm dần xuống 0.1s, 0.05s
   - Quan sát khi nào server bắt đầu chậm

## ✅ Kết Luận

**Câu trả lời:** **CÓ, đúng là do wait_time trong luồng!**

- Wait time 1-3s → RPS thấp (~48) nhưng **ổn định và thực tế**
- Wait time 0s → RPS cao (~1450) nhưng **có thể quá tải server**

**Khuyến nghị:**
- **Load Test**: Giữ wait_time 1-3s (như hiện tại)
- **Stress Test**: Giảm wait_time xuống 0.1-0.5s
- **Performance Test**: Giảm wait_time xuống 0.01-0.1s






