"""
Общие фикстуры для всех тестов.
"""
import pytest

from src import DataExplorer


@pytest.fixture
def explorer():
    """Базовая фикстура, создающая экземпляр DataExplorer."""
    return DataExplorer()
