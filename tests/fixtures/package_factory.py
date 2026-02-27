"""
Содержит функции для создания объектов Package
с возможностью переопределения параметров по умолчанию.
"""
import pytest

from src.models import Package


def create_package_dict(**kwargs):
    """
    Создает словарь пакета в формате API ответа.
    """
    package = {
        "name": "test-package",
        "epoch": 0,
        "version": "1.0.0",
        "release": "alt1",
        "arch": "x86_64",
        "disttag": "p11+test",
        "buildtime": 1234567890,
        "source": "test-source"
    }

    # Обновляем значениями, которые передал пользователь
    package.update(kwargs)

    return package


def create_package_object(**kwargs):
    """
    Создает объект Package.
    """
    pkg_dict = create_package_dict(**kwargs)

    # Создаем объект Package из словаря
    return Package(
        name=pkg_dict["name"],
        epoch=pkg_dict["epoch"],
        version=pkg_dict["version"],
        release=pkg_dict["release"],
        arch=pkg_dict["arch"],
        buildtime=pkg_dict["buildtime"],
        source=pkg_dict["source"]
    )

@pytest.fixture
def sisyphus_response_data():
    """Фикстура, возвращающая полный ответ API"""
    return {
        "request_args": {
            "arch": 'null'
        },
        "length": 2,
        "packages": [
            create_package_dict(name="0ad", version="116.0"),
            create_package_dict(name="0ad-debuginfo", version="120.0"),
        ],
    }

@pytest.fixture
def p11_response_data():
    """Фикстура, возвращающая полный ответ API"""
    return {
        "request_args": {
            "arch": 'null'
        },
        "length": 2,
        "packages": [
            create_package_dict(name="0ad", version="115.0"),
            create_package_dict(name="0ad-debuginfo", version="121.0"),
        ],
    }
