"""
Script test API /search để kiểm tra API có hoạt động không.
Sử dụng payload mẫu từ user query.
"""

import requests
import json
from config import Config
from data_generators import SearchPayloadGenerator

# API URL
API_URL = f"{Config.BASE_URL}{Config.ENDPOINT_SEARCH}"

print("="*80)
print("TEST API /search")
print("="*80)
print(f"\nURL: {API_URL}")
print(f"Base URL: {Config.BASE_URL}")
print(f"Endpoint: {Config.ENDPOINT_SEARCH}")

# Tạo payload mẫu (có thể dùng sample từ user query hoặc generate)
print(f"\n{'='*80}")
print("ĐANG TẠO PAYLOAD...")
print(f"{'='*80}\n")

# Sử dụng payload mẫu từ user query
payload = {
    "query": "Sở thích",
    "user_id": "Đoàn Ngọc Cường",
    "top_k": 3,
    "limit": 10,
    "score_threshold": 0.7
}

# Hoặc có thể dùng generator:
# payload = SearchPayloadGenerator.generate_payload()

print(f"✅ Query: {payload['query']}")
print(f"✅ User ID: {payload['user_id']}")
print(f"✅ Top K: {payload['top_k']}")
print(f"✅ Limit: {payload['limit']}")
print(f"✅ Score Threshold: {payload['score_threshold']}")

print(f"\n{'='*80}")
print("ĐANG GỬI REQUEST...")
print(f"{'='*80}\n")

try:
    # Gửi request
    response = requests.post(
        API_URL,
        json=payload,
        headers=Config.DEFAULT_HEADERS,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"\n✅ SUCCESS! API hoạt động bình thường!")
            print(f"\nResponse JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Kiểm tra format response (có thể có kết quả tìm kiếm)
            if isinstance(data, list):
                print(f"\n✅ Response là array với {len(data)} kết quả")
            elif isinstance(data, dict):
                print(f"\n✅ Response là object với các keys: {list(data.keys())}")
                
        except json.JSONDecodeError:
            print(f"\n❌ Lỗi: Response không phải JSON hợp lệ")
            print(f"Response text: {response.text[:500]}")
    else:
        print(f"\n❌ ERROR! Status code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except requests.exceptions.Timeout:
    print(f"\n❌ Lỗi: Request timeout (quá 30 giây)")
except requests.exceptions.ConnectionError:
    print(f"\n❌ Lỗi: Không thể kết nối đến {API_URL}")
    print(f"   Kiểm tra:")
    print(f"   - URL có đúng không?")
    print(f"   - Server có đang chạy không?")
    print(f"   - Firewall có chặn không?")
except Exception as e:
    print(f"\n❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*80}")
print("TEST HOÀN TẤT")
print(f"{'='*80}\n")



