from fastapi.testclient import TestClient

from httpx import Response


class APIClient:
    health_url = '/health'

    def __init__(self, client: TestClient) -> None:
        self._client = client

    def send_check_health(self) -> Response:
        return self._client.get(self.health_url)
