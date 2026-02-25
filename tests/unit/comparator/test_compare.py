"""
Параметризованные тесты для compare_versions.

Что тестируется:
- Все возможные случаи сравнения версий (базовые, числовые, тильда, epoch и т.д.)
- Каждый тест проверяет одну группу случаев
"""

import pytest

from src.comparator import RPMVersionComparator

from tests.fixtures.version_cases import (
    BASIC_CASES,
    NUMERIC_CASES,
    TILDE_CASES,
    EPOCH_CASES,
    EMPTY_RELEASE_CASES,
    REAL_WORLD_CASES, ALL_CASES
)


def _run_comparison_test(e1, v1, r1, e2, v2, r2, expected, desc):
    """
    Вспомогательная функция для запуска сравнения.
    """
    result = RPMVersionComparator.compare_versions(e1, v1, r1, e2, v2, r2)
    assert result == expected, (
        f"{desc}\n"
        f"  {e1}:{v1}-{r1} vs {e2}:{v2}-{r2}\n"
        f"  expected {expected}, got {result}"
    )


@pytest.mark.parametrize("e1,v1,r1, e2,v2,r2, expected, desc", BASIC_CASES)
def test_basic_comparison(e1, v1, r1, e2, v2, r2, expected, desc):
    """Базовое сравнение без epoch."""
    _run_comparison_test(e1, v1, r1, e2, v2, r2, expected, desc)


@pytest.mark.parametrize("e1,v1,r1, e2,v2,r2, expected, desc", NUMERIC_CASES)
def test_numeric_comparison(e1, v1, r1, e2, v2, r2, expected, desc):
    """Числовое сравнение (10 > 2 как числа, а не строки)."""
    _run_comparison_test(e1, v1, r1, e2, v2, r2, expected, desc)


@pytest.mark.parametrize("e1,v1,r1, e2,v2,r2, expected, desc", TILDE_CASES)
def test_tilde_comparison(e1, v1, r1, e2, v2, r2, expected, desc):
    """Сравнение с тильдой (pre-release версии)."""
    _run_comparison_test(e1, v1, r1, e2, v2, r2, expected, desc)


@pytest.mark.parametrize("e1,v1,r1, e2,v2,r2, expected, desc", EPOCH_CASES)
def test_epoch_comparison(e1, v1, r1, e2, v2, r2, expected, desc):
    """Приоритет epoch над version."""
    _run_comparison_test(e1, v1, r1, e2, v2, r2, expected, desc)


@pytest.mark.parametrize("e1,v1,r1, e2,v2,r2, expected, desc", EMPTY_RELEASE_CASES)
def test_empty_release_comparison(e1, v1, r1, e2, v2, r2, expected, desc):
    """Сравнение с пустым release."""
    _run_comparison_test(e1, v1, r1, e2, v2, r2, expected, desc)


@pytest.mark.parametrize("e1,v1,r1, e2,v2,r2, expected, desc", REAL_WORLD_CASES)
def test_real_world_comparison(e1, v1, r1, e2, v2, r2, expected, desc):
    """Реальные примеры из ALT Linux."""
    _run_comparison_test(e1, v1, r1, e2, v2, r2, expected, desc)
