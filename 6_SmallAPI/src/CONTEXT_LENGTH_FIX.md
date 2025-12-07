# 🔧 Fix: Locust Fail 100% - Context Length Exceeded

## 🔍 Vấn Đề

**Triệu chứng:**
- Locust test fail 100%
- Response time rất nhanh (~9ms)
- Response size nhỏ (~114 bytes)
- Status code: 400

**Nguyên nhân:**
```
"This model's maximum context length is 600 tokens. 
However, your request has 830 input tokens."
```

Model **Qwen3-0.6B** có giới hạn **600 tokens**, nhưng:
- System prompt: ~400 tokens
- Một số dữ liệu trong Excel: >200 tokens (tổng >600 tokens)
- → API trả về 400 Bad Request
- → Locust đánh dấu fail

## ✅ Giải Pháp

### 1. Truncate Dữ Liệu Khi Quá Dài (KHÔNG BỎ ĐI)

**File:** `excel_data_loader.py`

Thêm logic truncate trong `get_random_new_data()`:

```python
def get_random_new_data(self, max_tokens: int = 200) -> str:
    """
    Lấy dữ liệu ngẫu nhiên từ TẤT CẢ dữ liệu.
    Nếu dữ liệu quá dài, sẽ tự động truncate (cắt ngắn) thay vì bỏ đi.
    
    Args:
        max_tokens: Số tokens tối đa (mặc định 200)
                   - System prompt: ~400 tokens
                   - User content: ~200 tokens
                   - Tổng: ~600 tokens (giới hạn của model)
    """
    # Lấy dữ liệu ngẫu nhiên từ TẤT CẢ dữ liệu (KHÔNG bỏ đi)
    data = random.choice(self._new_data_list)
    
    # Nếu quá dài, truncate thay vì bỏ đi
    max_chars = max_tokens * 4  # ~4 ký tự = 1 token
    if len(data) > max_chars:
        # Truncate ở vị trí hợp lý (không cắt giữa từ)
        truncated = data[:max_chars]
        last_newline = truncated.rfind('\n')
        last_space = truncated.rfind(' ')
        cut_pos = max(last_newline, last_space)
        
        if cut_pos > max_chars * 0.8:
            return truncated[:cut_pos]
        return truncated
    
    return data
```

### 2. Cải Thiện Xử Lý Lỗi 400

**File:** `locustfile.py`

Thêm xử lý đặc biệt cho lỗi context length:

```python
elif response.status_code == 400:
    error_data = response.json()
    error_msg = error_data.get("error", {}).get("message", "")
    
    # Nếu là lỗi context length, đánh dấu với message rõ ràng
    if "context length" in error_msg.lower():
        response.failure(
            f"Context length exceeded (data too long): {error_msg[:200]}"
        )
```

## 📊 Kết Quả

### Trước khi fix:
- ❌ Fail: 100% (121/121 requests)
- ❌ Lý do: Context length exceeded

### Sau khi fix:
- ✅ Success: 100% (10/10 requests test)
- ✅ Tổng dữ liệu: 5949 dòng (KHÔNG bỏ đi dòng nào)
- ✅ Dữ liệu quá dài: 131/5949 dòng (2.2%) - sẽ được truncate khi sử dụng

## 🎯 Thống Kê Dữ Liệu

| Metric | Giá Trị |
|--------|---------|
| Tổng số dòng | 5949 (100% - KHÔNG bỏ đi) |
| Dữ liệu hợp lệ (≤800 ký tự) | 5818 (97.8%) - dùng trực tiếp |
| Dữ liệu quá dài (>800 ký tự) | 131 (2.2%) - sẽ truncate khi dùng |
| Giới hạn tokens | 200 tokens (~800 ký tự) |

## ✅ Cách Hoạt Động

1. **Khi load Excel:** Load tất cả 5949 dòng (KHÔNG bỏ đi dòng nào)

2. **Khi lấy random data:** 
   - Random từ TẤT CẢ 5949 dòng
   - Nếu dữ liệu quá dài (>800 ký tự), tự động truncate
   - Truncate ở vị trí hợp lý (không cắt giữa từ)
   - Đảm bảo không vượt quá 600 tokens tổng

3. **Nếu vẫn có lỗi 400:**
   - Locust sẽ đánh dấu fail với message rõ ràng
   - Dễ debug hơn

## 🔧 Tùy Chỉnh

Nếu muốn điều chỉnh giới hạn:

```python
# Trong excel_data_loader.py, thay đổi max_tokens
new_data = loader.get_random_new_data(max_tokens=150)  # Stricter
new_data = loader.get_random_new_data(max_tokens=250)  # More lenient
```

**Lưu ý:** 
- System prompt ~400 tokens
- Model limit: 600 tokens
- → User content nên ≤200 tokens để an toàn

## 📝 Test

Chạy test để xác nhận:

```bash
python debug_locust_failure.py  # Test 10 requests
python check_data_filtering.py   # Kiểm tra số lượng dữ liệu hợp lệ
```

## ✅ Kết Luận

- ✅ Đã fix lỗi context length exceeded
- ✅ **KHÔNG bỏ đi dữ liệu nào** - tất cả 5949 dòng đều được sử dụng
- ✅ Tự động truncate dữ liệu quá dài (thay vì bỏ đi)
- ✅ Locust test sẽ không còn fail 100%

