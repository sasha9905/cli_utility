"""
Общие фикстуры для всех тестов.
"""
import pytest

from src import DataExplorer


@pytest.fixture
def explorer():
    """Базовая фикстура, создающая экземпляр DataExplorer."""
    return DataExplorer()

def pytest_configure(config):
    """Конфигурация pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
