"""
Script test API /memories để kiểm tra API có hoạt động không.
Sử dụng payload mẫu từ user query.
"""

import requests
import json
from config import Config
from data_generators import MemoriesPayloadGenerator

# API URL
API_URL = f"{Config.BASE_URL}{Config.ENDPOINT_MEMORIES}"

print("="*80)
print("TEST API /memories")
print("="*80)
print(f"\nURL: {API_URL}")
print(f"Base URL: {Config.BASE_URL}")
print(f"Endpoint: {Config.ENDPOINT_MEMORIES}")

# Tạo payload mẫu
print(f"\n{'='*80}")
print("ĐANG TẠO PAYLOAD...")
print(f"{'='*80}\n")

# Cho test đơn giản, có thể dùng ít turns hơn (ví dụ: 10 turns)
# Hoặc dùng default (100-200 turns) để test với conversation dài
use_short_conversation = True  # Set False để dùng 100-200 turns

if use_short_conversation:
    # Test với 10 turns (nhanh hơn)
    payload = {
        "user_id": MemoriesPayloadGenerator.generate_user_id(),
        "run_id": MemoriesPayloadGenerator.generate_run_id(),
        "messages": MemoriesPayloadGenerator.generate_messages(min_turns=5, max_turns=10)
    }
    print(f"ℹ️  Sử dụng conversation ngắn (5-10 turns) cho test nhanh")
    print(f"   Để test với 100-200 turns, set use_short_conversation=False")
else:
    # Test với 100-200 turns (default)
    payload = MemoriesPayloadGenerator.generate_payload()
    print(f"ℹ️  Sử dụng conversation dài (100-200 turns)")

print(f"✅ User ID: {payload['user_id']}")
print(f"✅ Run ID: {payload['run_id']}")
print(f"✅ Số messages: {len(payload['messages'])}")
print(f"\nMessages preview (3 đầu tiên):")
for i, msg in enumerate(payload['messages'][:3], 1):
    content_preview = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
    print(f"  {i}. [{msg['role']}] {content_preview}")

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

