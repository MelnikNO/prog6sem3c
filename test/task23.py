import asyncio
from locust import FastHttpUser, task, between
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

class TeacherUser(FastHttpUser):
    wait_time = between(1, 3)
    @task
    async def load_teachers_page(self):
        try:
            async with self.client.get("/teachers", catch_response=True) as response:
                if response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, "html.parser")
                    
                    teacher_elements = soup.select(".teacher-name, .card-title, .fio")
                    
                    if not teacher_elements:
                        print("No teacher elements found. Check the CSS selector.")
                        response.failure("No teacher elements found")
                        return
                    
                    print(f"Found {len(teacher_elements)} teacher(s)")
                    
                    tasks = [self.process_teacher(elem, idx) for idx, elem in enumerate(teacher_elements)]
                    await asyncio.gather(*tasks)
                    
                    response.success()
                else:
                    print(f"HTTP error: {response.status_code}")
                    response.failure(f"Request failed with status: {response.status_code}")
                    
        except Exception as e:
            print(f"Network or parsing error: {e}")
    
    async def process_teacher(self, element, idx):
        try:
            teacher_name = element.get_text(strip=True)
            if teacher_name:
                print(f"Teacher {idx + 1}: {teacher_name}")
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Error processing teacher {idx}: {e}")
    
    def on_start(self):
        print("Teacher load test started")
    
    def on_stop(self):
        print("Teacher load test finished")
