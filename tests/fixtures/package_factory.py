"""
Содержит функции для создания объектов Package
с возможностью переопределения параметров по умолчанию.
"""
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

    package.update(kwargs)

    return package


def create_package_object(**kwargs):
    """
    Создает объект Package.
    """
    pkg_dict = create_package_dict(**kwargs)

    return Package(
        name=pkg_dict["name"],
        epoch=pkg_dict["epoch"],
        version=pkg_dict["version"],
        release=pkg_dict["release"],
        arch=pkg_dict["arch"],
        buildtime=pkg_dict["buildtime"],
        source=pkg_dict["source"]
    )
