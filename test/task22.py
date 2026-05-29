from locust import HttpUser, task, between
import logging

logging.basicConfig(level=logging.INFO)

class HabrUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        print("Habr load test started")
    
    def on_stop(self):
        print("Habr load test finished")
    
    @task
    def load_main_page(self):
        with self.client.get("/ru", catch_response=True) as response:
            if response.status_code == 200:
                print("Page loaded: /ru")
                response.success()
            else:
                response.failure(f"Failed with status: {response.status_code}")
