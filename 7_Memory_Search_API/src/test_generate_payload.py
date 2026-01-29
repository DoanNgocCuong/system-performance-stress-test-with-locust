"""
Script test de kiem tra generate payload cho Memories API.
"""

import json
import sys
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_generators import MemoriesPayloadGenerator
from config import Config

print("="*80)
print("TEST GENERATE PAYLOAD - Memories API")
print("="*80)

print(f"\nConfig:")
print(f"  MIN_MESSAGES_TURNS: {Config.MIN_MESSAGES_TURNS}")
print(f"  MAX_MESSAGES_TURNS: {Config.MAX_MESSAGES_TURNS}")

try:
    print(f"\n{'='*80}")
    print("Generating payload...")
    print(f"{'='*80}\n")
    
    payload = MemoriesPayloadGenerator.generate_payload()
    
    print(f"SUCCESS!")
    print(f"  User ID: {payload['user_id']}")
    print(f"  Run ID: {payload['run_id']}")
    print(f"  Messages count: {len(payload['messages'])}")
    
    # Tính payload size
    payload_json = json.dumps(payload)
    payload_size = len(payload_json)
    print(f"  Payload size: {payload_size:,} bytes ({payload_size/1024:.2f} KB)")
    
    # Kiểm tra pattern
    assistant_count = sum(1 for msg in payload['messages'] if msg['role'] == 'assistant')
    user_count = sum(1 for msg in payload['messages'] if msg['role'] == 'user')
    print(f"  Assistant messages: {assistant_count}")
    print(f"  User messages: {user_count}")
    
    print(f"\n{'='*80}")
    print("SAMPLE MESSAGES (3 dau tien):")
    print(f"{'='*80}\n")
    for i, msg in enumerate(payload['messages'][:3], 1):
        content_preview = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
        print(f"{i}. [{msg['role']}] {content_preview}")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

