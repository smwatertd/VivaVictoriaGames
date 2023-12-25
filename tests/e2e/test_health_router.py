from tests.e2e.api_client import APIClient


class TestHealthRouter:
    def test_check_health_status_code(self, client: APIClient) -> None:
        response = client.send_check_health()

        assert response.status_code == 200

    def test_check_health_body(self, client: APIClient) -> None:
        response = client.send_check_health()

        assert response.json() == {'status': 'ok'}
