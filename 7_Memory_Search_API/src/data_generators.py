"""
Data generators module cho Locust test.
Chịu trách nhiệm tạo dữ liệu test động theo nguyên tắc Single Responsibility.
"""

import random
import uuid
import time
from typing import List, Dict, Any
from config import Config


# Sample assistant messages cho Memories API (với emotion tags)
SAMPLE_ASSISTANT_MESSAGES = [
    "<emotion type=\"excited\"/> Chào cậu, tớ là Pika đây! <emotion type=\"happy\"/> Cuối tuần vừa rồi tớ đã được đi chơi ở một hành tinh có rất nhiều kẹo mút. <emotion type=\"curious\"/> Thế cuối tuần của cậu thì sao?",
    "<emotion type=\"surprised\"/> Ôi! <emotion type=\"happy\"/> Chắc là cậu đã có một cuối tuần thật là vui và bận rộn đúng không? <emotion type=\"curious\"/> Cậu đã làm gì thế?",
    "<emotion type=\"happy\"/> Tớ hiểu rồi! <emotion type=\"curious\"/> Vậy cậu có muốn kể cho tớ nghe về một hoạt động nào đó mà cậu thích làm không?",
    "<emotion type=\"sad\"/> Ồ, vậy hả? <emotion type=\"curious\"/> Thế cậu có muốn kể cho tớ nghe về một trò chơi mà cậu thích không?",
    "<emotion type=\"sad\"/> Tớ hiểu rồi. <emotion type=\"curious\"/> Vậy cậu có muốn nghe Pika hát một bài không?",
    "<emotion type=\"happy\"/> Tuyệt vời! <emotion type=\"excited\"/> Pika rất vui khi được nói chuyện với cậu!",
    "<emotion type=\"curious\"/> Thế cậu thích loại nhạc gì? <emotion type=\"playful\"/> Pika có thể hát nhiều thể loại lắm!",
    "<emotion type=\"happy\"/> Được rồi! <emotion type=\"excited\"/> Hôm nay chúng mình sẽ học về điều gì nhỉ?",
    "<emotion type=\"curious\"/> Cậu có muốn chơi một trò chơi không? <emotion type=\"playful\"/> Pika có rất nhiều trò chơi hay!",
    "<emotion type=\"happy\"/> Pika rất vui vì cậu đã chia sẻ với Pika! <emotion type=\"encouraging\"/> Cậu đang làm rất tốt!",
    "<emotion type=\"calm\"/> Không sao đâu, cậu cứ từ từ. <emotion type=\"encouraging\"/> Pika sẽ chờ cậu.",
    "<emotion type=\"curious\"/> Cậu muốn làm gì tiếp theo? <emotion type=\"happy\"/> Pika sẵn sàng giúp cậu!",
    "<emotion type=\"proud\"/> Cậu đã làm rất tốt! <emotion type=\"happy\"/> Pika tự hào về cậu!",
    "<emotion type=\"thats_right\"/> Đúng rồi! <emotion type=\"happy\"/> Cậu trả lời chính xác!",
    "<emotion type=\"surprised\"/> Wow! <emotion type=\"excited\"/> Cậu giỏi quá!",
    "<emotion type=\"playful\"/> Haha, thú vị nhỉ! <emotion type=\"happy\"/> Cậu làm Pika cười!",
    "<emotion type=\"thinking\"/> Để Pika suy nghĩ một chút... <emotion type=\"curious\"/> Có vẻ như cậu đang nghĩ về điều gì đó thú vị!",
    "<emotion type=\"encouraging\"/> Cậu có thể làm được! <emotion type=\"happy\"/> Pika tin vào cậu!",
    "<emotion type=\"no_problem\"/> Không có gì đâu! <emotion type=\"happy\"/> Pika luôn sẵn sàng giúp cậu!",
    "<emotion type=\"worry\"/> Ồ, có vẻ như cậu đang gặp khó khăn. <emotion type=\"calm\"/> Đừng lo, mọi thứ sẽ ổn thôi!",
]

# Sample user messages cho Memories API
SAMPLE_USER_MESSAGES = [
    "Michael Buzzell",
    "Thì cái đoạn này thầy chê cáo nhiều là anh nghĩ là bây giờ chẳng có cách nào khác ngoài việc chúng ta tạo được một cái tập dữ liệu.",
    "Nhưng mà cái con này nó vẫn đang bị Con này nó hết kết nối rồi.",
    "A, còn một vấn đề nữa cơ là nó đang bị lặp lại audio.",
    "cái á, giữ, một bài đi á, mà anh không không cần xét luồng này, cứ xét một bài thì được. Thích một bài là thích được. Thích bài nào ấy nhỉ, ông nhỉ? Thích bài nào ấy nhỉ? 573. 573.",
    "Tôi muốn học bài.",
    "Pika ơi, hôm nay tôi muốn chơi một trò chơi.",
    "Bạn có thể giúp tôi học tiếng Anh không?",
    "Tôi thích nghe nhạc.",
    "Cuối tuần vừa rồi tôi đã đi chơi.",
    "Tôi muốn kể cho Pika nghe về một chuyện vui.",
    "Hôm nay tôi cảm thấy hơi buồn.",
    "Tôi đang nghĩ về một vấn đề.",
    "Pika có thể giải thích cho tôi không?",
    "Tôi không hiểu lắm, bạn có thể nói rõ hơn không?",
    "Được rồi, cảm ơn Pika!",
    "Tôi muốn thử một cái mới.",
    "Bạn có biết về chủ đề này không?",
    "Tôi thắc mắc về điều này.",
    "Cảm ơn Pika đã giúp tôi!",
    "Tôi muốn tiếp tục.",
    "Được rồi, tôi hiểu rồi.",
    "Wow, thú vị quá!",
    "Tôi muốn làm lại.",
    "Có vẻ như khó quá.",
    "Tôi sẽ cố gắng thêm.",
    "Tuyệt vời, tôi đã làm được!",
    "Pika giúp tôi nhé!",
    "Tôi đang chờ đợi.",
    "Được, bắt đầu thôi!",
]

# Sample queries cho Search API
SAMPLE_QUERIES = [
    "Sở thích",
    "Cuối tuần",
    "Trò chơi",
    "Âm nhạc",
    "Học tập",
    "Hoạt động",
    "Thể thao",
    "Phim ảnh",
    "Đọc sách",
    "Du lịch",
]


class MemoriesPayloadGenerator:
    """Class chịu trách nhiệm generate payload cho POST /memories API."""
    
    @staticmethod
    def generate_user_id() -> str:
        """Generate user ID ngẫu nhiên từ sample list hoặc random."""
        if random.random() < 0.7:  # 70% chance dùng sample IDs
            return random.choice(Config.SAMPLE_USER_IDS)
        else:
            return f"user_{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def generate_run_id() -> str:
        """Generate run ID với format run_{timestamp}_{random}."""
        timestamp = int(time.time())
        random_suffix = uuid.uuid4().hex[:6]
        return f"run_{timestamp}_{random_suffix}"
    
    @staticmethod
    def generate_messages(min_turns: int = None, max_turns: int = None) -> List[Dict[str, str]]:
        """
        Generate messages array cho payload với số lượng turns ngẫu nhiên.
        
        Args:
            min_turns: Số turns tối thiểu (nếu None sẽ dùng Config.MIN_MESSAGES_TURNS)
            max_turns: Số turns tối đa (nếu None sẽ dùng Config.MAX_MESSAGES_TURNS)
        
        Returns:
            List các dictionary chứa messages với role và content (100-200 turns)
        """
        # Sử dụng config nếu không truyền vào
        min_turns = min_turns if min_turns is not None else Config.MIN_MESSAGES_TURNS
        max_turns = max_turns if max_turns is not None else Config.MAX_MESSAGES_TURNS
        
        messages = []
        num_turns = random.randint(min_turns, max_turns)
        
        # Pattern: luân phiên assistant và user messages
        # Bắt đầu với assistant (giống conversation thực tế)
        for i in range(num_turns):
            # Assistant message
            assistant_content = random.choice(SAMPLE_ASSISTANT_MESSAGES)
            messages.append({
                "content": assistant_content,
                "role": "assistant"
            })
            
            # User message (trừ lượt cuối có thể không có user response)
            if i < num_turns - 1:
                user_content = random.choice(SAMPLE_USER_MESSAGES)
                messages.append({
                    "content": user_content,
                    "role": "user"
                })
            # Lượt cuối có thể kết thúc bằng assistant message (không có user response)
        
        return messages
    
    @staticmethod
    def generate_payload() -> Dict[str, Any]:
        """
        Generate payload hoàn chỉnh cho POST /memories API.
        
        Returns:
            Dictionary chứa user_id, run_id, và messages array
        """
        return {
            "user_id": MemoriesPayloadGenerator.generate_user_id(),
            "run_id": MemoriesPayloadGenerator.generate_run_id(),
            "messages": MemoriesPayloadGenerator.generate_messages()
        }


class SearchPayloadGenerator:
    """Class chịu trách nhiệm generate payload cho POST /search API."""
    
    @staticmethod
    def generate_user_id() -> str:
        """Generate user ID ngẫu nhiên từ sample list hoặc random."""
        if random.random() < 0.7:  # 70% chance dùng sample IDs
            return random.choice(Config.SAMPLE_USER_IDS)
        else:
            return f"user_{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def generate_query() -> str:
        """Generate query ngẫu nhiên từ sample queries."""
        return random.choice(SAMPLE_QUERIES)
    
    @staticmethod
    def generate_payload(
        top_k: int = None,
        limit: int = None,
        score_threshold: float = None
    ) -> Dict[str, Any]:
        """
        Generate payload hoàn chỉnh cho POST /search API.
        
        Args:
            top_k: Số kết quả top k (nếu None sẽ dùng Config.SEARCH_TOP_K)
            limit: Giới hạn số kết quả (nếu None sẽ dùng Config.SEARCH_LIMIT)
            score_threshold: Ngưỡng điểm (nếu None sẽ dùng Config.SEARCH_SCORE_THRESHOLD)
            
        Returns:
            Dictionary chứa query, user_id, top_k, limit, và score_threshold
        """
        return {
            "query": SearchPayloadGenerator.generate_query(),
            "user_id": SearchPayloadGenerator.generate_user_id(),
            "top_k": top_k if top_k is not None else Config.SEARCH_TOP_K,
            "limit": limit if limit is not None else Config.SEARCH_LIMIT,
            "score_threshold": score_threshold if score_threshold is not None else Config.SEARCH_SCORE_THRESHOLD
        }

