import json
from unittest.mock import MagicMock

import pytest
import requests

from tests.fixtures.package_factory import create_package_dict


class TestGetDataFromUrl:
    """
    Тестирование метода get_data_from_url.
    """
    @pytest.fixture(autouse=True)
    def _setup(self, explorer, mock_requests):
        """Этот метод будет вызываться автоматически перед каждым тестом."""
        self.explorer = explorer
        self.mock_requests = mock_requests

    @staticmethod
    def _assert_called_with_correct_url(mock_requests, branch="sisyphus"):
        """Проверяет, что requests.get вызван с правильным URL."""
        mock_requests.assert_called_once_with(
            f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}",
            timeout=30
        )

    def _assert_result_is_none_with_correct_call(self, result, mock_requests, branch="sisyphus"):
        """Комбинированная проверка для случаев с None."""
        assert result is None
        self._assert_called_with_correct_url(mock_requests, branch)

    def test_successful_request_returns_data(self):
        """
        Успешный запрос должен возвращать распарсенный JSON.
        """
        mock_response = MagicMock()
        expected_data = {
            "length": 2,
            "packages": [
                create_package_dict(name="firefox", version="116.0"),
                create_package_dict(name="chromium", version="120.0")
            ]
        }

        mock_response.json.return_value = expected_data
        mock_response.raise_for_status.return_value = None

        self.mock_requests.return_value = mock_response
        result = self.explorer.get_data_from_url("sisyphus")

        assert result == expected_data
        self._assert_called_with_correct_url(self.mock_requests)

    def test_timeout_returns_none(self):
        """При таймауте метод должен возвращать None."""
        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.Timeout()

        self.mock_requests.return_value = mock_response
        result = self.explorer.get_data_from_url("sisyphus")

        self._assert_result_is_none_with_correct_call(result, self.mock_requests)

    def test_connection_error_returns_none(self):
        """При ошибке соединения метод должен возвращать None."""
        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.ConnectionError()

        self.mock_requests.return_value = mock_response
        result = self.explorer.get_data_from_url("sisyphus")

        self._assert_result_is_none_with_correct_call(result, self.mock_requests)

    @pytest.mark.parametrize("status_code", [404, 500, 502, 503])
    def test_http_errors_return_none(self, status_code):
        """
        При HTTP ошибках метод должен возвращать None.
        """
        mock_response = MagicMock()

        # Создаем исключение с response
        http_error = requests.exceptions.HTTPError(f"{status_code} Error")
        http_error.response = MagicMock()
        http_error.response.status_code = status_code

        mock_response.raise_for_status.side_effect = http_error
        self.mock_requests.return_value = mock_response

        result = self.explorer.get_data_from_url("sisyphus")

        self._assert_result_is_none_with_correct_call(result, self.mock_requests)

    def test_invalid_json_returns_none(self):
        """При битом JSON метод должен возвращать None."""
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.raise_for_status.return_value = None

        self.mock_requests.return_value = mock_response

        result = self.explorer.get_data_from_url("sisyphus")

        self._assert_result_is_none_with_correct_call(result, self.mock_requests)

