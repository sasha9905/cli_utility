from unittest.mock import MagicMock, patch

import requests

from tests.fixtures.package_factory import create_package_dict


def test_explore_api_triggers_processing(explorer):
    """
    Проверяем, что explore_api правильно вызывает get_data_from_url
    и затем данные обрабатываются.
    """
    # Подготовка
    test_data = {
        "packages": [create_package_dict(name="firefox")],
        "length": 1
    }
    mock_response = MagicMock()
    mock_response.json.return_value = test_data
    mock_response.raise_for_status.return_value = None

    with patch('requests.get') as mock_requests:
        mock_requests.return_value = mock_response
        result = explorer.explore_api()

    assert result is True
    assert "sisyphus" in explorer.data
    assert "p11" in explorer.data

    assert "x86_64" in explorer.sisyphus_packages_by_arch
    assert "firefox" in explorer.sisyphus_packages_by_arch["x86_64"]
    assert "x86_64" in explorer.p11_packages_by_arch


def test_error_bubble_up(explorer):
    """
    Проверяем, что ошибка в get_data_from_url правильно обрабатывается
    и влияет на результат explore_api.
    """
    # Первая ветка падает с ошибкой
    error_response = MagicMock()
    error_response.raise_for_status.side_effect = requests.exceptions.Timeout()

    # Вторая ветка успешна
    success_response = MagicMock()
    success_response.json.return_value = {
        "packages": [create_package_dict(name="firefox")],
        "length": 1
    }
    success_response.raise_for_status.return_value = None

    with patch('requests.get', side_effect=[error_response, success_response]):
        result = explorer.explore_api()

    assert result is False

    assert "p11" in explorer.data
    assert "x86_64" in explorer.p11_packages_by_arch
    assert "firefox" in explorer.p11_packages_by_arch["x86_64"]

    assert len(explorer.sisyphus_packages_by_arch) == 0


def test_multiple_calls_state(explorer):
    """
    Проверяем, что при повторных вызовах explore_api данные
    правильно обновляются, а не накапливаются.
    """
    # Первый вызов
    response1 = MagicMock()
    response1.json.return_value = {
        "packages": [create_package_dict(name="firefox", version="116.0")],
        "length": 1
    }
    response1.raise_for_status.return_value = None

    with patch('requests.get', return_value=response1):
        explorer.explore_api()

    assert explorer.sisyphus_packages_by_arch["x86_64"]["firefox"].version == "116.0"

    # Второй вызов с другими данными
    response2 = MagicMock()
    response2.json.return_value = {
        "packages": [create_package_dict(name="firefox", version="117.0")],
        "length": 1
    }
    response2.raise_for_status.return_value = None

    with patch('requests.get', return_value=response2):
        explorer.explore_api()

    # Должна быть новая версия
    assert len(explorer.sisyphus_packages_by_arch["x86_64"]) == 1
    assert explorer.sisyphus_packages_by_arch["x86_64"]["firefox"].version == "117.0"
