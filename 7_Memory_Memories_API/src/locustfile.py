"""
Locust stress test file cho Memories API:
- API POST /memories - Lưu trữ messages với user_id, run_id, và messages array.
"""

from locust import HttpUser, task, between

from config import Config
from data_generators import MemoriesPayloadGenerator


class MemoriesUser(HttpUser):
    """
    Locust User class định nghĩa task test cho Memories API.

    Tuân thủ Single Responsibility: Class này chỉ chịu trách nhiệm định nghĩa
    task và thực thi HTTP requests cho /memories.
    """

    host = Config.BASE_URL
    wait_time = between(Config.WAIT_TIME_MIN, Config.WAIT_TIME_MAX)

    # Các status codes được coi là success
    # 200: OK
    # 201: Created
    SUCCESS_STATUS_CODES = [200, 201]

    def _check_response_success(self, response) -> bool:
        """
        Helper method để kiểm tra response có thành công không.
        """
        if response.status_code in self.SUCCESS_STATUS_CODES:
            response.success()
            return True

        response.failure(
            f"Unexpected status code: {response.status_code}. "
            f"Response: {response.text[:500]}"
        )
        return False

    @task(Config.WEIGHT_MEMORIES)
    def test_memories(self):
        """
        Task test API POST /memories.

        Test việc gửi request lưu trữ messages với user_id, run_id, và messages array.
        """
        try:
            payload = MemoriesPayloadGenerator.generate_payload()
        except Exception as exc:  # pragma: no cover - defensive
            with self.client.post(
                Config.ENDPOINT_MEMORIES,
                json={},
                headers=Config.DEFAULT_HEADERS,
                catch_response=True,
                name="POST /memories",
            ) as response:
                response.failure(f"Error generating payload: {exc!r}")
            return

        with self.client.post(
            Config.ENDPOINT_MEMORIES,
            json=payload,
            headers=Config.DEFAULT_HEADERS,
            catch_response=True,
            name="POST /memories",
        ) as response:
            self._check_response_success(response)



