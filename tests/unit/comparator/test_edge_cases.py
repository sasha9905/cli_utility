"""
Тесты для крайних случаев, которые сложно параметризовать.

Что тестируется:
- Очень большие числа
- Очень длинные строки
- Unicode символы
- Смешанные буквенно-цифровые сегменты
"""

from src.comparator import RPMVersionComparator


def test_large_numbers():
    """
    Сравнение очень больших чисел в release.
    """
    result = RPMVersionComparator.compare_versions(
        0, "1.0", f"alt{10**6}",
        0, "1.0", f"alt{10**6 - 1}",
    )
    assert result == 1  # 1,000,000 > 999,999


def test_very_long_strings():
    """
    Сравнение очень длинных строк.
    """
    long_str = "a" * 10000

    # Сравнение с самим собой
    result = RPMVersionComparator.compare_versions(
        0, long_str, "alt1",
        0, long_str, "alt1"
    )
    assert result == 0

    # Сравнение с чуть более длинной строкой
    longer_str = "a" * 10001
    result = RPMVersionComparator.compare_versions(
        0, long_str, "alt1",
        0, longer_str, "alt1"
    )
    assert result == -1


def test_mixed_alphanumeric_segments():
    """
    Смешанные буквенно-цифровые сегменты.

    Проверяет правильность разбиения на сегменты:
    "abc123" должно разбиться на ["abc", "123"], а не на ["abc123"]
    """
    result = RPMVersionComparator.compare_versions(
        0, "abc123", "alt1",
        0, "abc456", "alt1"
    )
    assert result == -1

    result = RPMVersionComparator.compare_versions(
        0, "abc456", "alt1",
        0, "abc123", "alt1"
    )
    assert result == 1


def test_unicode_consistency():
    """
    Проверка работы с Unicode символами.

    Тест гарантирует, что сравнение антисимметрично:
    если a > b, то b < a, даже для Unicode.
    Не проверяет конкретное значение, только свойство.
    """
    # Сравниваем кириллицу и латиницу
    result1 = RPMVersionComparator.compare_versions(
        0, "а", "alt1",  # кириллица
        0, "a", "alt1"   # латиница
    )

    result2 = RPMVersionComparator.compare_versions(
        0, "a", "alt1",
        0, "а", "alt1"
    )

    # Свойство антисимметричности должно выполняться
    assert result1 == -result2, f"Сравнение не антисимметрично: {result1} vs {result2}"


def test_empty_version_strings():
    """
    Обработка пустых строк в version.

    Проверяет, что компаратор не падает при пустых входных данных.
    """
    # Все параметры пустые
    result = RPMVersionComparator.compare_versions(0, "", "", 0, "", "")
    assert result == 0

    # Только version пустая
    result = RPMVersionComparator.compare_versions(0, "", "alt1", 0, "1.0", "alt1")
    assert result == -1  # пустая version < непустой


def test_special_characters():
    """
    Обработка специальных символов в версиях.
    """
    test_cases = [
        # Подчеркивание
        (0, "1.0", "alt1_2", 0, "1.0", "alt1_1", 1, "_2 > _1"),
        # Точка в release
        (0, "1.0", "git.abc123", 0, "1.0", "git.abc122", 1, "git.abc123 > git.abc122"),
        # Дефис
        (0, "1.0", "pre-release", 0, "1.0", "pre", -1, "pre-release < pre"),
        # Дефис в начале
        (0, "1.0", "-rc1", 0, "1.0", "rc1", -1, "-rc1 < rc1"),
        # Множественные дефисы
        (0, "1.0", "a-b-c", 0, "1.0", "a-b", -1, "a-b-c > a-b (длиннее)"),
    ]

    for e1, v1, r1, e2, v2, r2, expected, desc in test_cases:
        result = RPMVersionComparator.compare_versions(e1, v1, r1, e2, v2, r2)
        assert result == expected, (
            f"{desc}\n"
            f"  {e1}:{v1}-{r1} vs {e2}:{v2}-{r2}\n"
            f"  expected {expected}, got {result}"
        )
