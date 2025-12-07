"""
Debug script để mô phỏng logic Locust và tìm lý do fail.
"""

import requests
import json
from pathlib import Path
from excel_data_loader import get_shared_loader
from data_generators import ChatCompletionPayloadFactory
from config import Config

API_URL = "http://103.253.20.30:7862/v1/chat/completions"

print("="*80)
print("DEBUG: MÔ PHỎNG LOGIC LOCUST")
print("="*80)

# Load dữ liệu
excel_path = Path(Config.EXCEL_DATA_PATH)
loader = get_shared_loader(str(excel_path))
factory = ChatCompletionPayloadFactory(excel_loader=loader, use_excel_data=True)

# Test nhiều requests để xem có request nào fail không
print(f"\nTest 10 requests để xem có request nào fail không:\n")

success_count = 0
fail_count = 0
fail_reasons = []

for i in range(10):
    try:
        payload = factory.build_payload()
        payload_dict = payload.to_dict()
        
        response = requests.post(
            API_URL,
            json=payload_dict,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Mô phỏng logic _check_response_success trong locustfile
        if response.status_code == 200:
            try:
                data = response.json()
                if "choices" in data:
                    success_count += 1
                    print(f"✅ Request {i+1}: SUCCESS")
                else:
                    fail_count += 1
                    reason = f"Missing 'choices' field. Keys: {list(data.keys())}"
                    fail_reasons.append(reason)
                    print(f"❌ Request {i+1}: FAIL - {reason}")
                    print(f"   Response: {response.text[:200]}")
            except json.JSONDecodeError as e:
                fail_count += 1
                reason = f"Invalid JSON: {e}"
                fail_reasons.append(reason)
                print(f"❌ Request {i+1}: FAIL - {reason}")
                print(f"   Response: {response.text[:200]}")
        else:
            fail_count += 1
            reason = f"Status code: {response.status_code}"
            fail_reasons.append(reason)
            print(f"❌ Request {i+1}: FAIL - {reason}")
            print(f"   Response: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        fail_count += 1
        reason = "Timeout"
        fail_reasons.append(reason)
        print(f"❌ Request {i+1}: FAIL - Timeout")
    except Exception as e:
        fail_count += 1
        reason = f"Exception: {e}"
        fail_reasons.append(reason)
        print(f"❌ Request {i+1}: FAIL - {reason}")

print(f"\n{'='*80}")
print("KẾT QUẢ:")
print(f"{'='*80}")
print(f"✅ Success: {success_count}/10")
print(f"❌ Fail: {fail_count}/10")

if fail_count > 0:
    print(f"\nLý do fail:")
    for i, reason in enumerate(set(fail_reasons), 1):
        print(f"  {i}. {reason}")



