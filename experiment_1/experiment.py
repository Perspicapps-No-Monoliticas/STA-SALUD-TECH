import json
import uuid

from locust import HttpUser, TaskSet, task, between, run_single_user

from config import BFF_HOST

JSON_HEADER = {"Content-Type": "application/json"}

all_tokens = []


class UserBehavior(TaskSet):
    token: str

    @task
    def login_and_ingest(self):
        # Login and get token
        response = self.client.get(
            f"{BFF_HOST}/auth/generate_token", headers=JSON_HEADER
        )
        token = response.json().get("token")
        self.tokens.append(token)

        # Set authorization header
        headers = {"Authorization": f"Bearer {token}"}
        headers.update(JSON_HEADER)

        # Call ingestion endpoint
        correlation_id = str(uuid.uuid4())
        self.client.post(
            f"{BFF_HOST}/ingestion/data-intakes",
            headers=headers,
            data=json.dumps({"correlation_id": correlation_id, "provider_id": token}),
        )

    @task
    def check_ingestion_status(self):
        for token in self.tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = self.client.get(
                f"{BFF_HOST}/ingestion/data-intakes?provider_id={token}&limit=1",
                headers=headers,
            )
            assert response.status_code == 200
            status = response.json()[0].get("status")
            assert status in ["IN_PROGRESS", "COMPLETED"]


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(30, 31)
    host = BFF_HOST

    def on_stop(self):
        # Final check to ensure the count of tokens matches the number of IN_PROGRESS or COMPLETED responses
        in_progress_or_completed_count = 0
        for token in self.tasks[0].tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = self.client.get(
                f"{BFF_HOST}/ingestion/data-intakes?provider_id={token}&limit=1",
                headers=headers,
            )
            if response.status_code == 200 and response.json().get("status") in [
                "IN_PROGRESS",
                "COMPLETED",
            ]:
                in_progress_or_completed_count += 1
        assert in_progress_or_completed_count == len(self.tasks[0].tokens)


if __name__ == "__main__":
    run_single_user(WebsiteUser)
