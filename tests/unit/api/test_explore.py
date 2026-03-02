from unittest.mock import patch

from .conftest import BaseAPITest


class TestExploreApi(BaseAPITest):

    def test_explore_api_returns_true_on_success(self):
        """Проверка, что при успехе возвращается True."""
        with patch.object(self.explorer, 'get_data_from_url') as mock_get:
            mock_get.return_value = {"packages": [], "length": 0}

            result = self.explorer.explore_api()

        assert result is True


    def test_when_get_data_returns_none(self):
        """
        Проверка, что если get_data_from_url вернул None, ветка пропускается.
        """
        with patch.object(self.explorer, 'get_data_from_url') as mock_get_data:
            # Первая ветка вернула None, вторая - данные
            mock_get_data.side_effect = [None, {"packages": [], "length": 0}]
            result = self.explorer.explore_api()

        assert result is False
        assert "p11" in self.explorer.data


    def test_explore_api_handles_exceptions(self, explorer):
        """Проверка, что метод не падает при исключениях."""
        with patch.object(explorer, 'get_data_from_url') as mock_get:
            mock_get.side_effect = Exception("Network error")

            result = explorer.explore_api()

        assert result is None

        # Данные должны остаться нетронутыми
        assert len(explorer.data) == 0



