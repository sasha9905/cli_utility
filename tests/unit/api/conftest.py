from unittest.mock import patch

import pytest

from src import DataExplorer


@pytest.fixture
def explorer():
    """Базовая фикстура, создающая экземпляр DataExplorer."""
    return DataExplorer()

@pytest.fixture
def mock_requests():
    """Фикстура, возвращающая замоканный requests.get."""
    with patch('requests.get') as mock:
        yield mock
