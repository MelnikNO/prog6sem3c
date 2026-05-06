from locust import HttpUser, task, between
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerfTestUser(HttpUser):
    wait_time = between(0, 0)

    def on_start(self):
        try:
            self.client.get("/health", timeout=2)
            logger.info(f"Health check passed for {self.host}")
        except Exception as e:
            logger.error(f"Health check failed: {e}")

    @task(1)
    def cpu_blocking(self):
        with self.client.get("/cpu?n=15000000", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Status code: {response.status_code}")
            else:
                try:
                    data = response.json()
                    if 'result' not in data:
                        response.failure("Missing 'result' in response")
                except Exception as e:
                    response.failure(f"Invalid JSON: {e}")

    @task(1)
    def cpu_non_blocking(self):
        with self.client.get("/cpu_fixed", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Status code: {response.status_code}")
            else:
                try:
                    data = response.json()
                    if 'mode' not in data:
                        response.failure("Missing 'mode' in response")
                except Exception as e:
                    response.failure(f"Invalid JSON: {e}")

