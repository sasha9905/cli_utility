"""
Property-based тесты (свойства сравнения).

Что тестируется:
- Рефлексивность: a == a
- Антисимметричность: если a > b, то b < a
- Транзитивность: если a > b и b > c, то a > c
"""

import pytest

from src.comparator import RPMVersionComparator
from tests.fixtures.version_cases import TEST_VERSIONS


class TestComparisonProperties:
    """
    Тесты математических свойств сравнения.

    Любое корректное отношение порядка должно удовлетворять:
    1. Рефлексивность: a == a
    2. Антисимметричность: если a > b, то b < a
    3. Транзитивность: если a > b и b > c, то a > c
    """

    @pytest.mark.parametrize("epoch, version, release", TEST_VERSIONS)
    def test_reflexivity(self, epoch, version, release):
        """
        Рефлексивность: версия равна самой себе.

        Это базовое свойство любого сравнения.
        """
        result = RPMVersionComparator.compare_versions(
            epoch, version, release,
            epoch, version, release
        )
        assert result == 0, f"{epoch}:{version}-{release} не равна себе"

    def test_antisymmetry_for_all_pairs(self):
        """
        Антисимметричность для всех пар версий.

        Проверяет, что для любых двух версий sign(a,b) = -sign(b,a).
        Перебирает все возможные пары из TEST_VERSIONS.
        """
        for i, (e1, v1, r1) in enumerate(TEST_VERSIONS):
            for j, (e2, v2, r2) in enumerate(TEST_VERSIONS):
                if i == j:
                    continue  # рефлексивность уже проверили

                result1 = RPMVersionComparator.compare_versions(e1, v1, r1, e2, v2, r2)
                result2 = RPMVersionComparator.compare_versions(e2, v2, r2, e1, v1, r1)

                # Должно выполняться: result1 == -result2
                assert result1 == -result2, (
                    f"Антисимметричность нарушена для:\n"
                    f"  {e1}:{v1}-{r1} vs {e2}:{v2}-{r2}\n"
                    f"  {result1} vs {result2}"
                )

    def test_transitivity(self):
        """
        Транзитивность для трех версий в порядке возрастания.

        Берем версии, которые точно должны быть упорядочены:
        v1 < v2 < v3
        """
        # Версии в порядке возрастания
        v1 = (0, "1.0.0", "alt1")
        v2 = (0, "1.0.0", "alt2")
        v3 = (0, "1.0.1", "alt1")

        e1, v1_str, r1 = v1
        e2, v2_str, r2 = v2
        e3, v3_str, r3 = v3

        # Проверяем, что v1 < v2 < v3
        assert RPMVersionComparator.compare_versions(e1, v1_str, r1, e2, v2_str, r2) == -1
        assert RPMVersionComparator.compare_versions(e2, v2_str, r2, e3, v3_str, r3) == -1

        # Должно быть v1 < v3
        assert RPMVersionComparator.compare_versions(e1, v1_str, r1, e3, v3_str, r3) == -1

    def test_transitivity_with_epoch(self):
        """
        Транзитивность с участием epoch.

        epoch имеет наивысший приоритет, поэтому:
        v1 (epoch=1) > v2 (epoch=0) > v3 (epoch=0, но version меньше)
        """
        v1 = (1, "1.0.0", "alt1")  # epoch 1
        v2 = (0, "2.0.0", "alt1")  # epoch 0, но version выше
        v3 = (0, "1.0.0", "alt2")  # epoch 0, version ниже чем v2

        e1, v1_str, r1 = v1
        e2, v2_str, r2 = v2
        e3, v3_str, r3 = v3

        # Проверяем порядок
        assert RPMVersionComparator.compare_versions(e1, v1_str, r1, e2, v2_str, r2) == 1  # v1 > v2
        assert RPMVersionComparator.compare_versions(e2, v2_str, r2, e3, v3_str, r3) == 1  # v2 > v3

        # Должно быть v1 > v3
        assert RPMVersionComparator.compare_versions(e1, v1_str, r1, e3, v3_str, r3) == 1


def test_comparison_is_total_order():
    """
    Проверка, что сравнение задает полный порядок.

    Для любых двух версий должно быть определено отношение:
    a < b, a = b или a > b.
    """
    for i, (e1, v1, r1) in enumerate(TEST_VERSIONS):
        for j, (e2, v2, r2) in enumerate(TEST_VERSIONS):
            result = RPMVersionComparator.compare_versions(e1, v1, r1, e2, v2, r2)

            # Результат должен быть -1, 0 или 1
            assert result in (-1, 0, 1), (
                f"Сравнение вернуло {result}, ожидалось -1, 0 или 1\n"
                f"  {e1}:{v1}-{r1} vs {e2}:{v2}-{r2}"
            )
