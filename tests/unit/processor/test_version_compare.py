import pytest
import json
from pathlib import Path

from src.processor import BranchProcessor
from tests.fixtures.package_factory import create_package_object


class TestVersionComparison:
    """
    Тестирование сравнения версий.
    """

    def test_finds_packages_with_different_versions(self, processor_with_different_versions):
        """Находит пакеты с разными версиями."""
        result = processor_with_different_versions.version_release_comparison()

        assert result == 1  # только firefox с разными версиями
        assert Path("version-release_compare.json").exists()

    def test_ignores_packages_with_same_versions(self, processor_with_different_versions):
        """Игнорирует пакеты с одинаковыми версиями."""
        processor_with_different_versions.version_release_comparison()

        with open("version-release_compare.json", 'r') as f:
            data = json.load(f)

        # Только firefox должен быть в результатах
        assert len(data) == 1
        assert data[0]["name"] == "firefox"

    @pytest.mark.parametrize("direction,should_differ", [
        ("newer_in_sisyphus", 1),
        ("older_in_sisyphus", 0),
        ("equal", 0)
    ])
    def test_comparison_directions(self, direction, should_differ, tmp_path):
        """Тестирует разные направления сравнения."""
        if direction == "newer_in_sisyphus":
            sisyphus = create_package_object(name="firefox", version="117.0")
            p11 = create_package_object(name="firefox", version="116.0")
        elif direction == "older_in_sisyphus":
            sisyphus = create_package_object(name="firefox", version="116.0")
            p11 = create_package_object(name="firefox", version="117.0")
        else:  # equal
            sisyphus = create_package_object(name="firefox", version="116.0")
            p11 = create_package_object(name="firefox", version="116.0")

        packages = {"x86_64": {"firefox": sisyphus}}
        p11_packages = {"x86_64": {"firefox": p11}}
        names = {"x86_64": {"firefox"}}

        processor = BranchProcessor(packages, p11_packages, names, names)
        result = processor.version_release_comparison()

        assert result == should_differ

    def test_json_structure(self, processor_with_different_versions):
        """Проверка структуры JSON файла с результатами."""
        processor_with_different_versions.version_release_comparison()

        with open("version-release_compare.json", 'r') as f:
            data = json.load(f)

        # Проверяем структуру каждого пакета
        for package in data:
            assert "name" in package
            assert "epoch" in package
            assert "version" in package
            assert "release" in package
            assert "arch" in package
            assert "buildtime" in package
            assert "source" in package

    def test_empty_result_creates_empty_json(self, tmp_path):
        """Когда нет различий, создается пустой JSON."""
        pkg = create_package_object(version="1.0.0")
        packages = {"x86_64": {"pkg": pkg}}
        names = {"x86_64": {"pkg"}}

        processor = BranchProcessor(packages, packages, names, names)
        result = processor.version_release_comparison()

        assert result == 0
        with open("version-release_compare.json", 'r') as f:
            data = json.load(f)
            assert data == []
