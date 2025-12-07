"""
Hiển thị ví dụ các dòng dữ liệu quá dài.
"""

from pathlib import Path
from excel_data_loader import get_shared_loader
from config import Config

excel_path = Path(Config.EXCEL_DATA_PATH)
loader = get_shared_loader(str(excel_path))

if loader:
    print("="*80)
    print("VÍ DỤ DỮ LIỆU QUÁ DÀI")
    print("="*80)
    
    max_tokens = 200
    max_chars = max_tokens * 4  # ~800 ký tự
    
    all_data = loader.get_all_data()
    
    # Tìm các dòng quá dài
    long_data = [
        (i, data, len(data), len(data) // 4) 
        for i, data in enumerate(all_data, 1)
        if len(data) > max_chars
    ]
    
    print(f"\nTổng số dòng: {len(all_data)}")
    print(f"Giới hạn: {max_chars} ký tự (~{max_tokens} tokens)")
    print(f"Số dòng quá dài: {len(long_data)}")
    
    if long_data:
        print(f"\n{'='*80}")
        print("VÍ DỤ DÒNG QUÁ DÀI (3 mẫu đầu):")
        print(f"{'='*80}\n")
        
        for idx, (row_num, data, char_count, token_est) in enumerate(long_data[:3], 1):
            print(f"--- MẪU {idx} (Dòng {row_num}) ---")
            print(f"Độ dài: {char_count} ký tự (~{token_est} tokens)")
            print(f"Vượt quá: {char_count - max_chars} ký tự (~{(token_est - max_tokens)} tokens)")
            print(f"\nNỘI DUNG ĐẦY ĐỦ:")
            print("-" * 80)
            print(data)
            print("-" * 80)
            
            # Hiển thị phần sẽ bị truncate
            print(f"\nSẼ BỊ TRUNCATE THÀNH ({max_chars} ký tự đầu):")
            print("-" * 80)
            truncated = data[:max_chars]
            # Tìm vị trí cắt hợp lý
            last_newline = truncated.rfind('\n')
            last_space = truncated.rfind(' ')
            cut_pos = max(last_newline, last_space)
            
            if cut_pos > max_chars * 0.8:
                final_truncated = truncated[:cut_pos]
                print(final_truncated)
                print(f"\n... (đã cắt {char_count - len(final_truncated)} ký tự)")
            else:
                print(truncated)
                print(f"\n... (đã cắt {char_count - max_chars} ký tự)")
            print("-" * 80)
            print()
    else:
        print("\n✅ Không có dòng nào quá dài!")

