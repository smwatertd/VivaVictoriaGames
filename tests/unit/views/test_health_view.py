from tests.test_case import TestCase


class TestHealthView(TestCase):
    def test_check_health_success_response(self) -> None:
        response = self.client.get('/health')

        assert 200 == response.status_code
        assert {'status': 'ok'} == response.json()
