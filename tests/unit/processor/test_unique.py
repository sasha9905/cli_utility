import json
from pathlib import Path

from src import BranchProcessor


class TestPublicUniqueMethods:
    """
    Тестирование публичных методов p11_not_in_sisyphus и sisyphus_not_in_p11.
    """

    def test_p11_not_in_sisyphus_finds_unique(self, processor_with_data):
        """p11_not_in_sisyphus находит пакеты из p11, которых нет в sisyphus."""
        result = processor_with_data.p11_not_in_sisyphus()

        assert result == 1  # vim уникален для p11
        assert Path("in_p11_not_in_sisyphus.json").exists()

    def test_sisyphus_not_in_p11_finds_unique(self, processor_with_data):
        """sisyphus_not_in_p11 находит пакеты из sisyphus, которых нет в p11."""
        result = processor_with_data.sisyphus_not_in_p11()

        assert result == 1  # chromium уникален для sisyphus
        assert Path("in_sisyphus_not_in_p11.json").exists()

    def test_when_no_unique_packages(self, tmp_path, package_firefox):
        """Когда нет уникальных пакетов, методы возвращают 0."""
        # Одинаковые данные в обеих ветках
        packages = {"x86_64": {"firefox": package_firefox}}
        names = {"x86_64": {"firefox"}}

        processor = BranchProcessor(packages, packages, names, names)

        assert processor.p11_not_in_sisyphus() == 0
        assert processor.sisyphus_not_in_p11() == 0

    def test_methods_create_json_with_correct_structure(self, processor_with_data):
        """Проверка структуры создаваемых JSON файлов."""
        processor_with_data.p11_not_in_sisyphus()

        with open("in_p11_not_in_sisyphus.json", 'r') as f:
            data = json.load(f)
            # Должен быть список словарей
            assert isinstance(data, list)
            if data:
                assert "name" in data[0]
                assert "version" in data[0]
                assert "arch" in data[0]
