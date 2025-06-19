"""Locust load testing for Sonny platform."""
from locust import HttpUser, task, between

class SonnyUser(HttpUser):
    """Simulates user interactions with Sonny API and UI."""
    wait_time = between(1, 3)

    @task(3)
    def process_api(self):
        # Test symbolic processing endpoint
        self.client.post(
            "/process/",
            json={"text": "Test load interaction"},
            headers={"Content-Type": "application/json"},
        )

    @task(1)
    def access_ui(self):
        # Test Streamlit UI root
        self.client.get("/")

# To run incremental tests:
# locust -f locustfile.py --host http://localhost:8000
# Start with small user count, then increase to desired load.