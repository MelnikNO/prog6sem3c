from locust import HttpUser, task

class MyUser(HttpUser):
    @task
    def get_users(self):
        with self.client.get("/api/users", catch_response=True) as response:
            if response.status_code == 200:
                print("Request successful")
                response.success()
            else:
                response.failure(f"Request failed with status: {response.status_code}")
