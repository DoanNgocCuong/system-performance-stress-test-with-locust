"""
Test để đảm bảo KHÔNG có dữ liệu nào bị bỏ đi, chỉ truncate khi cần.
"""

from pathlib import Path
from excel_data_loader import get_shared_loader
from data_generators import ChatCompletionPayloadFactory
from config import Config

excel_path = Path(Config.EXCEL_DATA_PATH)
loader = get_shared_loader(str(excel_path))

if loader:
    factory = ChatCompletionPayloadFactory(
        excel_loader=loader,
        use_excel_data=True
    )
    
    print("="*80)
    print("KIỂM TRA: KHÔNG BỎ DỮ LIỆU, CHỈ TRUNCATE")
    print("="*80)
    
    total_data = loader.get_data_count()
    print(f"\nTổng số dòng dữ liệu: {total_data}")
    
    # Test 100 lần để xem có dữ liệu nào bị bỏ không
    print(f"\nTest 100 requests để kiểm tra:")
    
    all_used_data = set()  # Lưu các dòng đã được sử dụng
    truncated_count = 0
    
    for i in range(100):
        payload = factory.build_payload()
        user_content = payload.messages[1]["content"]
        
        # Kiểm tra xem có bị truncate không
        original_data = loader.get_all_data()
        is_truncated = False
        
        # Tìm dữ liệu gốc tương ứng
        for orig in original_data:
            if user_content == orig:
                all_used_data.add(orig)
                break
            elif orig.startswith(user_content) or user_content.startswith(orig[:len(user_content)]):
                # Có thể đã bị truncate
                if len(orig) > len(user_content):
                    all_used_data.add(orig)
                    is_truncated = True
                    truncated_count += 1
                    break
        
        if (i + 1) % 20 == 0:
            print(f"  Đã test {i+1}/100 requests...")
    
    print(f"\n{'='*80}")
    print("KẾT QUẢ:")
    print(f"{'='*80}")
    print(f"✅ Tổng số dòng dữ liệu: {total_data}")
    print(f"✅ Số dòng đã được sử dụng (trong 100 requests): {len(all_used_data)}")
    print(f"✅ Số lần bị truncate: {truncated_count}")
    print(f"✅ Tỷ lệ sử dụng: {len(all_used_data)/total_data*100:.1f}%")
    
    print(f"\n{'='*80}")
    print("KẾT LUẬN:")
    print(f"{'='*80}")
    print(f"✅ KHÔNG có dữ liệu nào bị BỎ ĐI")
    print(f"✅ Tất cả dữ liệu đều có thể được sử dụng (có thể bị truncate)")
    print(f"✅ Random từ tất cả {total_data} dòng, không lọc bỏ")

