"""
Test chi tiết response từ API để xem tại sao Locust bị fail.
"""

import requests
import json
from pathlib import Path
from excel_data_loader import get_shared_loader
from data_generators import ChatCompletionPayloadFactory
from config import Config

API_URL = "http://103.253.20.30:7862/v1/chat/completions"

print("="*80)
print("KIỂM TRA CHI TIẾT RESPONSE TỪ API")
print("="*80)

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
    
    print(f"\n📤 Gửi request với model: {payload_dict['model']}")
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=payload_dict, headers=headers, timeout=30)
        
        print(f"\n📥 Status Code: {response.status_code}")
        print(f"📏 Response Size: {len(response.text)} bytes")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        print(f"\n{'='*80}")
        print("RESPONSE BODY:")
        print(f"{'='*80}")
        print(response.text)
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\n{'='*80}")
                print("PARSED JSON:")
                print(f"{'='*80}")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                # Kiểm tra theo logic trong locustfile
                print(f"\n{'='*80}")
                print("KIỂM TRA THEO LOGIC LOCUST:")
                print(f"{'='*80}")
                
                has_choices = "choices" in data
                print(f"✅ Có field 'choices': {has_choices}")
                
                if has_choices:
                    print(f"✅ Số lượng choices: {len(data['choices'])}")
                    if len(data['choices']) > 0:
                        choice = data['choices'][0]
                        print(f"✅ Choice[0]: {json.dumps(choice, indent=2, ensure_ascii=False)}")
                        
                        if "message" in choice:
                            message = choice["message"]
                            print(f"✅ Có field 'message' trong choice")
                            print(f"✅ Message content: {message.get('content', 'N/A')}")
                        else:
                            print(f"❌ KHÔNG có field 'message' trong choice")
                else:
                    print(f"❌ KHÔNG có field 'choices' - Đây là lý do Locust fail!")
                    print(f"   Các keys có sẵn: {list(data.keys())}")
                    
            except json.JSONDecodeError as e:
                print(f"\n❌ Lỗi parse JSON: {e}")
                print(f"Response text: {response.text}")
        else:
            print(f"\n❌ Status code không phải 200: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

