"""
Configuration module cho Locust stress testing.
Chứa các cấu hình chung cho test suite Memories API.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# Load .env file từ thư mục parent (7_Memories_API/)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def _get_int(env_name: str, default: int) -> int:
    """Helper để đọc int từ env (fallback nếu có lỗi)."""
    value = os.getenv(env_name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


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
    """Class chứa các cấu hình cho Locust test Memories API."""

    # Base URL của API server - đọc từ .env file
    BASE_URL = os.getenv(
        "MEMORIES_API_BASE_URL",
        "http://103.253.20.30:8889",  # Default value nếu không có trong .env
    )

    # API Endpoint
    ENDPOINT_MEMORIES = "/memories"

    # Headers mặc định
    DEFAULT_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    # Wait time giữa các requests (giây) cho Locust
    WAIT_TIME_MIN = _get_float("WAIT_TIME_MIN", 1.0)
    WAIT_TIME_MAX = _get_float("WAIT_TIME_MAX", 3.0)

    # Weight cho task memories (tỷ lệ thực thi)
    WEIGHT_MEMORIES = _get_int("WEIGHT_MEMORIES", 1)

    # Messages turns configuration (cho Memories API)
    # Mặc định: 100-200 turns (để test với conversation dài)
    MIN_MESSAGES_TURNS = _get_int("MIN_MESSAGES_TURNS", 100)
    MAX_MESSAGES_TURNS = _get_int("MAX_MESSAGES_TURNS", 200)

    # Sample user IDs cho test (có thể random hoặc từ list)
    SAMPLE_USER_IDS = [
        "Nguyễn Minh Phúc",
        "Đoàn Ngọc Cường",
        "Michael Buzzell",
    ]


