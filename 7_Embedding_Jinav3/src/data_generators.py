"""
Data generators module cho Locust test.
Chịu trách nhiệm tạo dữ liệu test động theo nguyên tắc Single Responsibility.
"""

import random
from typing import List, Dict, Any
from config import Config


# Sample input texts cho embeddings API
SAMPLE_INPUTS = [
    "hello world",
    "This is a test sentence.",
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning is fascinating.",
    "Natural language processing enables computers to understand human language.",
    "Embeddings convert text into numerical vectors.",
    "Python is a popular programming language.",
    "Deep learning models can process large amounts of data.",
    "Artificial intelligence is transforming industries.",
    "Text embeddings help with semantic search.",
    "Vector databases store and retrieve embeddings efficiently.",
    "Semantic similarity can be measured using cosine distance.",
    "Large language models have revolutionized NLP.",
    "Transformers architecture powers modern AI systems.",
    "Transfer learning allows models to adapt to new tasks.",
    "Fine-tuning improves model performance on specific domains.",
    "Attention mechanisms help models focus on relevant parts.",
    "Neural networks learn patterns from data.",
    "Gradient descent optimizes model parameters.",
    "Backpropagation calculates gradients for training.",
    "Xin chào thế giới",
    "Đây là một câu test.",
    "Học máy rất thú vị.",
    "Xử lý ngôn ngữ tự nhiên giúp máy tính hiểu ngôn ngữ con người.",
    "Python là ngôn ngữ lập trình phổ biến.",
    "Trí tuệ nhân tạo đang biến đổi các ngành công nghiệp.",
    "Vector database lưu trữ và truy xuất embeddings hiệu quả.",
    "Mô hình ngôn ngữ lớn đã cách mạng hóa NLP.",
    "Kiến trúc Transformers cung cấp năng lượng cho các hệ thống AI hiện đại.",
    "Học chuyển tiếp cho phép mô hình thích ứng với các tác vụ mới.",
]


class EmbeddingsPayloadGenerator:
    """Class chịu trách nhiệm generate payload cho POST /v1/embeddings API."""
    
    @staticmethod
    def generate_input() -> str:
        """
        Generate input text ngẫu nhiên từ sample list.
        
        Returns:
            String input text
        """
        return random.choice(SAMPLE_INPUTS)
    
    @staticmethod
    def generate_payload(input_text: str = None, model: str = None) -> Dict[str, Any]:
        """
        Generate payload hoàn chỉnh cho POST /v1/embeddings API.
        
        Args:
            input_text: Input text (nếu None sẽ generate ngẫu nhiên)
            model: Model name (nếu None sẽ dùng Config.MODEL_NAME)
            
        Returns:
            Dictionary chứa model và input
        """
        return {
            "model": model if model is not None else Config.MODEL_NAME,
            "input": input_text if input_text is not None else EmbeddingsPayloadGenerator.generate_input()
        }



