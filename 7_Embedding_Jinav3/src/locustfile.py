"""
Locust stress test file cho Jina Embeddings v3 API.
Test endpoint: POST /v1/embeddings
"""

import json
from locust import HttpUser, task, between

from config import Config
from data_generators import EmbeddingsPayloadGenerator


class EmbeddingsUser(HttpUser):
    """
    Locust User class định nghĩa task test cho Embeddings API.
    
    Tuân thủ Single Responsibility: Class này chỉ chịu trách nhiệm định nghĩa
    task và thực thi HTTP requests.
    """
    
    # Thời gian chờ giữa các task (0.5-2 giây)
    wait_time = between(Config.WAIT_TIME_MIN, Config.WAIT_TIME_MAX)
    
    # Các status codes được coi là success
    SUCCESS_STATUS_CODES = [200]
    
    def on_start(self):
        """
        Method được gọi khi một user instance bắt đầu.
        Có thể dùng để setup initial state nếu cần.
        """
        pass
    
    def _check_response_success(self, response):
        """
        Helper method để kiểm tra response có thành công không.
        
        Args:
            response: Locust response object
            
        Returns:
            bool: True nếu response thành công, False nếu không
        """
        if response.status_code in self.SUCCESS_STATUS_CODES:
            try:
                # Kiểm tra response có phải JSON hợp lệ không
                data = response.json()
                # Kiểm tra có field 'data' trong response (format của embeddings API)
                if "data" in data and len(data["data"]) > 0:
                    response.success()
                    return True
                else:
                    response.failure(
                        f"Response missing 'data' field or empty. Response: {response.text[:500]}"
                    )
                    return False
            except json.JSONDecodeError:
                response.failure(f"Invalid JSON response: {response.text[:500]}")
                return False
        else:
            response.failure(
                f"Unexpected status code: {response.status_code}. "
                f"Response: {response.text[:500]}"
            )
            return False
    
    @task
    def test_embeddings(self):
        """
        Task test API POST /v1/embeddings.
        
        Test việc gửi request tạo embeddings với model và input text.
        """
        try:
            # Generate payload động
            payload = EmbeddingsPayloadGenerator.generate_payload()
        except Exception as e:
            # Nếu có lỗi khi generate payload, đánh dấu là failure
            self.client.post(
                Config.EMBEDDINGS_ENDPOINT,
                json={},
                headers=Config.DEFAULT_HEADERS,
                catch_response=True,
                name="POST /v1/embeddings"
            ).failure(f"Error generating payload: {str(e)}")
            return
        
        # Gửi POST request
        with self.client.post(
            Config.EMBEDDINGS_ENDPOINT,
            json=payload,
            headers=Config.DEFAULT_HEADERS,
            catch_response=True,
            name="POST /v1/embeddings"
        ) as response:
            # Kiểm tra response
            self._check_response_success(response)



