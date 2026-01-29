"""
Configuration module cho Locust test của Jina Embeddings v3 API.
Hỗ trợ đọc cấu hình từ file .env ở thư mục dự án.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Tải .env (nếu tồn tại) ở thư mục cha
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


def _get_float(env_name: str, default: float) -> float:
    """Helper để đọc float từ env (fallback nếu có lỗi)."""
    value = os.getenv(env_name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


class Config:
    """Chứa các thông số cấu hình chính cho bài test."""

    # Base URL của API server
    BASE_URL = os.getenv(
        "EMBEDDINGS_API_BASE_URL",
        "http://103.253.20.30:8080"
    )

    # API Endpoint
    EMBEDDINGS_ENDPOINT = os.getenv(
        "EMBEDDINGS_ENDPOINT",
        "/v1/embeddings"
    )

    # Model name
    MODEL_NAME = os.getenv(
        "EMBEDDINGS_MODEL_NAME",
        "jinaai/jina-embeddings-v3"
    )

    # Wait time giữa các requests (giây)
    WAIT_TIME_MIN = _get_float("EMBEDDINGS_WAIT_MIN", 0.5)
    WAIT_TIME_MAX = _get_float("EMBEDDINGS_WAIT_MAX", 2.0)

    # Headers mặc định
    DEFAULT_HEADERS = {
        "Content-Type": "application/json"
    }



