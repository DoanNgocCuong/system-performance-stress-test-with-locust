"""
Script test API endpoint mới để kiểm tra API có hoạt động không.
"""

import requests
import json
from pathlib import Path
from excel_data_loader import get_shared_loader
from data_generators import ChatCompletionPayloadFactory
from config import Config

# API endpoint mới
API_URL = "http://103.253.20.30:7862/v1/chat/completions"

print("="*80)
print("TEST API ENDPOINT MỚI")
print("="*80)
print(f"\nURL: {API_URL}")

# Load dữ liệu từ Excel
excel_path = Path(Config.EXCEL_DATA_PATH)
loader = get_shared_loader(str(excel_path))

if loader:
    factory = ChatCompletionPayloadFactory(
        excel_loader=loader,
        use_excel_data=True
    )
    
    # Tạo payload
    payload = factory.build_payload()
    payload_dict = payload.to_dict()
    
    print(f"\n✅ Đã tạo payload với model: {payload_dict['model']}")
    print(f"✅ Số messages: {len(payload_dict['messages'])}")
    
    # Hiển thị user message (rút gọn)
    user_msg = next((m for m in payload_dict['messages'] if m['role'] == 'user'), None)
    if user_msg:
        content_preview = user_msg['content'][:150] + "..." if len(user_msg['content']) > 150 else user_msg['content']
        print(f"✅ User content (rút gọn): {content_preview}")
    
    print(f"\n{'='*80}")
    print("ĐANG GỬI REQUEST...")
    print(f"{'='*80}\n")
    
    try:
        # Gửi request
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            API_URL,
            json=payload_dict,
            headers=headers,
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
                
                # Kiểm tra format response
                if "choices" in data:
                    print(f"\n✅ Response có field 'choices' - Đúng format!")
                    if len(data["choices"]) > 0:
                        choice = data["choices"][0]
                        if "message" in choice:
                            print(f"✅ Message content: {choice['message'].get('content', '')[:200]}...")
                else:
                    print(f"\n⚠️  Response không có field 'choices'")
                    
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
        
else:
    print(f"\n❌ Không thể load dữ liệu từ Excel")



