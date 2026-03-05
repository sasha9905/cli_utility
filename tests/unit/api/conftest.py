from unittest.mock import patch

import pytest


@pytest.fixture
def mock_requests():
    """Фикстура, возвращающая замоканный requests.get."""
    with patch('requests.get') as mock:
        yield mock


class BaseAPITest:
    """Базовый класс для всех API тестов."""

    @pytest.fixture(autouse=True)
    def _setup(self, explorer):
        """Автоматически устанавливает explorer для всех тестов."""
        self.explorer = explorer


class BaseAPITestWithRequests(BaseAPITest):
    """Базовый класс для тестов, которым нужен mock_requests."""

    @pytest.fixture(autouse=True)
    def _setup_with_requests(self, mock_requests):
        self.mock_requests = mock_requests
