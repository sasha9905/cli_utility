from unittest.mock import MagicMock, patch

from conftest import BaseAPITest
from tests.fixtures.package_factory import create_package_dict


class TestPackageProcessing(BaseAPITest):
    """
        Тестирование обработки пакетов через explore_api.
    """

    @staticmethod
    def _mock_api_response(packages):
        """Вспомогательный метод для мока API ответа."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "packages": packages,
            "length": len(packages)
        }
        mock_response.raise_for_status.return_value = None
        return mock_response

    def test_packages_grouped_by_architecture(self):
        """
            Проверка, что пакеты правильно группируются по архитектурам.
        """
        # Подготовка
        sisyphus_data = {
            "packages": [
                create_package_dict(name="firefox", arch="x86_64", version="116.0"),
                create_package_dict(name="firefox", arch="aarch64", version="116.0"),
                create_package_dict(name="chromium", arch="x86_64", version="120.0"),
            ],
            "length": 3
        }

        p11_data = {
            "packages": [],
            "length": 0
        }

        with patch.object(self.explorer, 'get_data_from_url') as mock_get_data:
            mock_get_data.side_effect = [sisyphus_data, p11_data]
            self.explorer.explore_api()

        assert 'x86_64' in self.explorer.sisyphus_packages_by_arch
        assert 'aarch64' in self.explorer.sisyphus_packages_by_arch

        x86_packages = self.explorer.sisyphus_packages_by_arch["x86_64"]
        assert 'firefox' in x86_packages
        assert 'chromium' in x86_packages

    def test_both_branches_processed_correctly(self):
        """
        Проверка, что обе ветки обрабатываются.
        """
        # Разные данные для разных веток
        sisyphus_data = {
            "packages": [
                create_package_dict(name="firefox", version="116.0"),
            ],
            "length": 1
        }

        p11_data = {
            "packages": [
                create_package_dict(name="firefox", version="115.0"),
            ],
            "length": 1
        }

        with patch.object(self.explorer, 'get_data_from_url') as mock_get_data:
            mock_get_data.side_effect = [sisyphus_data, p11_data]
            self.explorer.explore_api()

        assert  self.explorer.sisyphus_packages_by_arch["x86_64"]["firefox"].version == "116.0"
        assert  self.explorer.p11_packages_by_arch["x86_64"]["firefox"].version == "115.0"

