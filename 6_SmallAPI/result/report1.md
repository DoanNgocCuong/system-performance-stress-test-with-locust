![1765001111212](image/report1/1765001111212.png)



Em test con của a Trúc.

+, Random: 5949 dòng data (lấy từ lịch sử real workflow)
+, 100 CCU, P99 : 69ms => khá ngon anh [@Truc Le Van]() , anh [@Cuong Vu Cao]() ạ.

---



**Hiện 100 user, mỗi user có P99 = 69ms, mà sao RPS có 48 ?**

![Attachment](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/760047/59f0a10d-7055-4666-9ea5-84bf67a98bbb/image.jpg?AWSAccessKeyId=ASIA2F3EMEYEUX3CUAOU&Signature=HthF8IEJxwuIc8pCrWYnVKkQHU0%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEKj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDp%2ByrmB5xdHpC0YFkZUKyMKvu9yQ%2FKCnMn8ihrVfnevQIhAILWnQvFlKBQWGrrAZwaNqFwzTRijGNcyD7cCHG4VskZKvMECHEQARoMNjk5NzUzMzA5NzA1IgxPWXd%2BQk4YLPZfvDcq0AQcI7INZb6AUCiUhN1b8ZHGGm3iVfePjK1%2Fjnql25PxQyeUCa4v2SZYFApICHQzBGFLHMuF2rUjkGRKpVBw%2FZE2Tlb%2BNeuGvZPZRlovPUpb9KUowKIaEbXPAmZvVbdtYp2Grj%2B1jspy%2BBjehuIhzjxhyaHogRYD2bA2OinlRBsWI6Vk8vu%2BupHaF54mc70FMld6XDcFBwGcv0Tn%2FtWpJ0WtLq0dYoowKT4YhJHx2gxRLBK%2B9D8eqTBg0y1BbxL2gpZJ89enZcT%2Fsy59R1sYU9q5aX%2BwYXcNBFHLj1cqAKFziw85h2dUFHv43o8wsYTkOihrogRLLJSUA1iYFUqFP3SSVK3TMVMuBVyI9AC5YZVCEgYohf5qPH39MXqKAdjp3FOmIpuYf3kVl2DitftrQywZlJAdkpJjyIQdzN2NHFEVvSDri41OQg9UaHTeMLFd%2B6bQ%2B5GKPbRn%2FwfZJP41Mf82%2B84y3KiJs3XHJYi%2BRUB2FhnUYkB5lp42MMm0FhqdjocgyqAP2nm9hmYiJHwz6deaYvKXLM%2BCz9NWPi1TydWu8ikVzRMPtBAPfiRKvoAe8cUdqpdEfzkvqgQxV6rYP71rq0Sh598vZap1o0p19AJ7oRhkX7wHVnoGCT1ZnNCkTgCVKKkc5qUree4z%2FlmjanKxHirIlV57SSJZFgoMP8Mu%2Fneu0H%2BsmjF1f1vurZhpoDmGPuSVVIF7VrdaDfcud5vxhhvszhPOOe75QhRL5Uex4zV8ZJ%2Bd5h1tdO5xiJmDnach3cHssEl3udqqCNRCD%2FmAMPa1z8kGOpcBn6zVgL%2FK3lMm2aIxhCQ7Zhpz8ZMxN47VDscs5HFV72S9uzvuhYPn7WALtLrgkxEoyVuIJYwe596Ad0iETHhxuQDGvPTAsyZM3j4a9Vc4zeS0dXMTj7J0kVhVyDv%2FkbzWUIdd%2FxTtNiBW%2BmIV6SEQ6ajgnB8IVAkoIH3%2FhzvcYM%2B%2FCR9m7ljyCLnzPxJmZo2qFA1NZRfcFQ%3D%3D&Expires=1765008269)


RPS thấp hơn nhiều so với lý thuyết vì 100 user của bạn không phải lúc nào cũng “bắn” request liên tục; ngoài 69 ms xử lý còn có think time/wait time và overhead khác nên mỗi user chỉ tạo được ~0.48 request/giây.[tangowhisky37.github**+1**](https://tangowhisky37.github.io/PracticalPerformanceAnalyst/pages/spe_fundamentals/what_is_littles_law/)

## Tính nhanh từ số liệu của bạn

* Công thức xấp xỉ: RPS≈soˆˊ userresponse time + think time\text{RPS} \approx \frac{\text{số user}}{\text{response time + think time}}**RPS**≈**response time + think time**s**o**ˆ**ˊ** user.[corporatefinanceinstitute**+1**](https://corporatefinanceinstitute.com/resources/data-science/littles-law/)
* Đang có 100 user, RPS ≈ 48 → mỗi vòng một user mất khoảng 100/48≈2.08100 / 48 ≈ 2.08**100/48**≈**2.08** giây, trong đó response time ~0.069 giây, phần còn lại ~2 giây là thời gian chờ (think time, sleep, chuẩn bị request, network, v.v.).[stackoverflow**+1**](https://stackoverflow.com/questions/49552745/how-throughput-and-response-time-are-related)

## Vì sao không lên ~1450 RPS?

* Nếu 100 user mà chỉ có 69 ms/vòng, lý thuyết RPS ≈ 100/0.069≈1450100 / 0.069 ≈ 1450**100/0.069**≈**1450** nhưng đó là trường hợp không có think time và hệ thống + client đủ khỏe để bắn liên tục, điều này hiếm khi đúng với kịch bản Locust thực tế.[perfmatrix**+1**](https://www.perfmatrix.com/latency-bandwidth-throughput-and-response-time/)
* Trong Locust, các hàm `wait_time` (between, constant), thời gian xử lý Python, network, TLS handshake, logging… đều làm tăng chu kỳ mỗi vòng lên khoảng >2 giây nên RPS thực tế dừng lại quanh 48 là hợp lý với kịch bản hiện tại.[locust**+1**](https://docs.locust.io/en/stable/writing-a-locustfile.html)

Nếu bạn gửi snippet `wait_time` và task trong `locustfile.py`, có thể chỉnh giúp để RPS tăng lên gần giới hạn lý thuyết khi cần stress test.

---



Đúng, nguyên nhân chính là `wait_time` trong code. Đang kiểm tra cấu hình hiện tại:

[4 tools called]

## Trả lời: Có, đúng là do `wait_time` trong luồng

### Phân tích

**Tình huống:**

- 100 CCU
- P99 Response Time = 69ms (nhanh)
- RPS = 48 (thấp)

**Tính toán:**

```
Mỗi vòng = Response Time + Wait Time
         = 0.069s + ~2.0s (wait_time trung bình)
         = ~2.069 giây

RPS = 100 / 2.069 ≈ 48 RPS ✅
```

**Kết luận:** Đúng là do `wait_time = between(1.0, 3.0)` giây trong code.

### Cấu hình hiện tại

```python
# config.py
WAIT_TIME_MIN = 1.0  # giây
WAIT_TIME_MAX = 3.0  # giây
# Trung bình = 2.0 giây

# locustfile.py
wait_time = between(Config.WAIT_TIME_MIN, Config.WAIT_TIME_MAX)
```

### So sánh

| Wait Time                   | Mỗi Vòng | RPS (100 users)  | Mục đích             |
| --------------------------- | ---------- | ---------------- | ----------------------- |
| **1-3s (hiện tại)** | ~2.07s     | **48 RPS** | Load test thực tế     |
| 0.1-0.5s                    | ~0.27s     | ~370 RPS         | Stress test             |
| 0.01-0.1s                   | ~0.1s      | ~1000 RPS        | Performance test        |
| 0s                          | 0.069s     | ~1450 RPS        | Max stress (nguy hiểm) |

### Nếu muốn tăng RPS

**Option 1: Giảm wait_time (khuyến nghị cho stress test)**

```bash
# .env hoặc export
QWEN_API_WAIT_MIN=0.1
QWEN_API_WAIT_MAX=0.5

# Kết quả: RPS ≈ 100 / (0.069 + 0.3) ≈ 270 RPS
```

**Option 2: Loại bỏ wait_time (chỉ dùng khi cần ép tối đa)**

```python
# config.py
WAIT_TIME_MIN=0.0
WAIT_TIME_MAX=0.0

# ⚠️ Cảnh báo: Server có thể quá tải!
```

### Lưu ý

- Wait time 1-3s: phù hợp cho load test mô phỏng user thật
- Wait time thấp: phù hợp cho stress test, nhưng cần theo dõi server
- Không có wait time: có thể quá tải server, chỉ dùng khi cần tìm giới hạn

Đã tạo file `RPS_ANALYSIS.md` với phân tích chi tiết.

Bạn muốn giữ nguyên (load test) hay điều chỉnh để stress test?
