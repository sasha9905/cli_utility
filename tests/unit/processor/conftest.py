import os

import pytest

from src import BranchProcessor
from tests.fixtures.package_factory import create_package_object


@pytest.fixture
def package_firefox():
    """Базовый пакет firefox."""
    return create_package_object(name="firefox", version="116.0")


@pytest.fixture
def package_firefox_newer():
    """Более новая версия firefox."""
    return create_package_object(name="firefox", version="117.0")

@pytest.fixture
def package_chromium():
    """Пакет chromium."""
    return create_package_object(name="chromium", version="120.0")


@pytest.fixture
def package_vim():
    """Пакет vim."""
    return create_package_object(name="vim", version="9.0")


@pytest.fixture
def processor_with_data(tmp_path, package_firefox, package_chromium, package_vim):
    """Processor с тестовыми данными."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    processor = BranchProcessor(
        sisyphus_packages={
            "x86_64": {
                "firefox": package_firefox,
                "chromium": package_chromium
            }
        },
        p11_packages={
            "x86_64": {
                "firefox": package_firefox,
                "vim": package_vim
            }
        },
        sisyphus_names={"x86_64": {"firefox", "chromium"}},
        p11_names={"x86_64": {"firefox", "vim"}}
    )

    yield processor
    os.chdir(original_dir)


@pytest.fixture
def processor_with_different_versions(tmp_path, package_firefox, package_firefox_newer, package_chromium):
    """Processor с разными версиями."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    processor = BranchProcessor(
        sisyphus_packages={
            "x86_64": {
                "firefox": package_firefox_newer,
                "chromium": package_chromium
            }
        },
        p11_packages={
            "x86_64": {
                "firefox": package_firefox,
                "chromium": package_chromium
            }
        },
        sisyphus_names={"x86_64": {"firefox", "chromium"}},
        p11_names={"x86_64": {"firefox", "chromium"}}
    )

    yield processor
    os.chdir(original_dir)
