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

    @task(2)
    def interpret(self):
        # Load-test the interpret endpoint
        self.client.post(
            "/interpret/",
            json={"text": "Load test for NLU interpret"},
            headers={"Content-Type": "application/json"},
        )

    @task(1)
    def complex_query(self):
        # Load-test the advanced complex query endpoint
        self.client.post(
            "/complex_query/",
            json={"query": "What is the weather tomorrow?", "context": {}},
            headers={"Content-Type": "application/json"},
        )

# To run incremental tests:
# locust -f locustfile.py --host http://localhost:8000
# Start with small user count, then increase to desired load.