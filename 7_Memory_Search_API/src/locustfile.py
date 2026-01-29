"""
Locust stress test file cho Search API.
Test endpoint:
1. POST /search - Tìm kiếm với query, user_id, top_k, limit, score_threshold.
"""

import json
from locust import HttpUser, task, between

from config import Config
from data_generators import SearchPayloadGenerator


class SearchUser(HttpUser):
    """
    Locust User class định nghĩa task test cho Search API.
    
    Tuân thủ Single Responsibility: Class này chỉ chịu trách nhiệm định nghĩa
    các task và thực thi HTTP requests.
    """
    
    # Thời gian chờ giữa các task (1-3 giây)
    wait_time = between(Config.WAIT_TIME_MIN, Config.WAIT_TIME_MAX)
    
    # Các status codes được coi là success
    # 200: OK
    # 201: Created
    SUCCESS_STATUS_CODES = [200, 201]
    
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
            response.success()
            return True
        else:
            response.failure(
                f"Unexpected status code: {response.status_code}. "
                f"Response: {response.text[:500]}"  # Giới hạn độ dài để tránh log quá dài
            )
            return False
    
    @task(Config.WEIGHT_SEARCH)
    def test_search(self):
        """
        Task test API POST /search.
        
        Test việc gửi request tìm kiếm với query, user_id, top_k, limit, score_threshold.
        """
        try:
            # Generate payload động
            payload = SearchPayloadGenerator.generate_payload()
        except Exception as e:
            # Nếu có lỗi khi generate payload, đánh dấu là failure
            self.client.post(
                Config.ENDPOINT_SEARCH,
                json={},
                headers=Config.DEFAULT_HEADERS,
                catch_response=True,
                name="POST /search"
            ).failure(f"Error generating payload: {str(e)}")
            return
        
        # Gửi POST request
        with self.client.post(
            Config.ENDPOINT_SEARCH,
            json=payload,
            headers=Config.DEFAULT_HEADERS,
            catch_response=True,
            name="POST /search"
        ) as response:
            # Kiểm tra response
            self._check_response_success(response)

