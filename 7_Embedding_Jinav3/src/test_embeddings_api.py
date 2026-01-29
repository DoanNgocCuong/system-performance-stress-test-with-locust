"""
Script test API /v1/embeddings để kiểm tra API có hoạt động không.
Sử dụng payload mẫu từ user query.
"""

import requests
import json
import sys
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from config import Config
from data_generators import EmbeddingsPayloadGenerator

# API URL
API_URL = f"{Config.BASE_URL}{Config.EMBEDDINGS_ENDPOINT}"

print("="*80)
print("TEST API /v1/embeddings")
print("="*80)
print(f"\nURL: {API_URL}")
print(f"Base URL: {Config.BASE_URL}")
print(f"Endpoint: {Config.EMBEDDINGS_ENDPOINT}")
print(f"Model: {Config.MODEL_NAME}")

# Tạo payload mẫu
print(f"\n{'='*80}")
print("Generating payload...")
print(f"{'='*80}\n")

# Sử dụng payload mẫu từ user query
payload = {
    "model": "jinaai/jina-embeddings-v3",
    "input": "hello world"
}

# Hoặc có thể dùng generator:
# payload = EmbeddingsPayloadGenerator.generate_payload()

print(f"Model: {payload['model']}")
print(f"Input: {payload['input']}")

print(f"\n{'='*80}")
print("Sending request...")
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
            print(f"\nSUCCESS! API is working correctly!")
            print(f"\nResponse JSON (truncated):")
            
            # Hiển thị response nhưng truncate nếu quá dài
            response_str = json.dumps(data, indent=2, ensure_ascii=False)
            if len(response_str) > 1000:
                print(response_str[:1000] + "\n... (truncated)")
            else:
                print(response_str)
            
            # Kiểm tra format response
            if "data" in data:
                print(f"\nResponse has 'data' field - Correct format!")
                if len(data["data"]) > 0:
                    embedding_item = data["data"][0]
                    if "embedding" in embedding_item:
                        embedding_length = len(embedding_item["embedding"])
                        print(f"Embedding vector length: {embedding_length}")
                        print(f"Embedding vector sample (first 5 values): {embedding_item['embedding'][:5]}")
            else:
                print(f"\nWARNING: Response does not have 'data' field")
                
        except json.JSONDecodeError:
            print(f"\nERROR: Response is not valid JSON")
            print(f"Response text: {response.text[:500]}")
    else:
        print(f"\nERROR! Status code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except requests.exceptions.Timeout:
    print(f"\nERROR: Request timeout (exceeded 30 seconds)")
except requests.exceptions.ConnectionError:
    print(f"\nERROR: Cannot connect to {API_URL}")
    print(f"   Please check:")
    print(f"   - Is the URL correct?")
    print(f"   - Is the server running?")
    print(f"   - Is the firewall blocking the connection?")
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*80}")
print("TEST COMPLETED")
print(f"{'='*80}\n")



