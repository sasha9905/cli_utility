import json
import os
import subprocess
import time
from pathlib import Path

import pytest

from src.api_client import DataExplorer
from src.processor import BranchProcessor
from src.logging_config import logger


class TestEndToEnd:
    """
    Сквозные тесты, проверяющие работу всего приложения.
    """

    @pytest.mark.slow
    def test_real_api_data_loading(self):
        """
        Проверка, что API реально отвечает и данные загружаются.
        """
        explorer = DataExplorer()

        # Реальный запрос к API
        sisyphus_data = explorer.get_data_from_url("sisyphus")
        p11_data = explorer.get_data_from_url("p11")

        # Проверки
        assert sisyphus_data is not None
        assert p11_data is not None
        assert "packages" in sisyphus_data
        assert "packages" in p11_data
        assert len(sisyphus_data["packages"]) > 0
        assert len(p11_data["packages"]) > 0

        logger.info(f"Sisyphus: {sisyphus_data['length']} пакетов")
        logger.info(f"P11: {p11_data['length']} пакетов\n")

    @pytest.mark.slow
    def test_full_comparison_workflow(self, tmp_path):
        """
        Полный цикл работы приложения.
        """
        # Переходим во временную директорию для JSON файлов
        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            explorer = DataExplorer()
            result = explorer.explore_api()

            assert result is True, "API должен успешно загрузиться"

            # Проверяем, что данные загружены
            assert len(explorer.sisyphus_packages_by_arch) > 0
            assert len(explorer.p11_packages_by_arch) > 0

            logger.info(f"Загружено архитектур в sisyphus: {len(explorer.sisyphus_packages_by_arch)}")
            for arch in explorer.sisyphus_packages_by_arch:
                logger.info(f"  {arch}: {len(explorer.sisyphus_packages_by_arch[arch])} пакетов")

            processor = BranchProcessor(
                sisyphus_packages=explorer.sisyphus_packages_by_arch,
                p11_packages=explorer.p11_packages_by_arch,
                sisyphus_names=explorer.sisyphus_packages_names,
                p11_names=explorer.p11_packages_names
            )

            unique_in_p11_count = processor.p11_not_in_sisyphus()
            unique_in_sisyphus_count = processor.sisyphus_not_in_p11()
            version_diff_count = processor.version_release_comparison()

            expected_files = [
                "in_p11_not_in_sisyphus.json",
                "in_sisyphus_not_in_p11.json",
                "version-release_compare.json"
            ]

            for filename in expected_files:
                file_path = Path(filename)
                assert file_path.exists(), f"Файл {filename} не создан"

                # Проверяем, что файл не пустой и содержит валидный JSON
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    assert isinstance(data, list), f"{filename} должен содержать список"

                logger.info(f"Файл {filename} создан, размер: {file_path.stat().st_size} байт")

            logger.info(f"Уникальных пакетов в p11: {unique_in_p11_count}")
            logger.info(f"Уникальных пакетов в sisyphus: {unique_in_sisyphus_count}")
            logger.info(f"Пакетов с разными версиями: {version_diff_count}\n")

            # Проверяем, что результаты имеют смысл
            total_packages = (
                    sum(len(pkgs) for pkgs in explorer.sisyphus_packages_by_arch.values()) +
                    sum(len(pkgs) for pkgs in explorer.p11_packages_by_arch.values())
            )

            # Сумма уникальных не должна превышать общее количество
            assert unique_in_p11_count + unique_in_sisyphus_count <= total_packages

        finally:
            os.chdir(original_dir)

    @pytest.mark.slow
    def test_known_packages_comparison(self, tmp_path):
        """
        Загружаем данные и проверяем состояние известных пакетов.
        """
        original_dir = os.getcwd()
        os.chdir(tmp_path)

        try:
            explorer = DataExplorer()
            explorer.explore_api()

            processor = BranchProcessor(
                sisyphus_packages=explorer.sisyphus_packages_by_arch,
                p11_packages=explorer.p11_packages_by_arch,
                sisyphus_names=explorer.sisyphus_packages_names,
                p11_names=explorer.p11_packages_names
            )

            # Проверяем популярные пакеты в aarch64
            arch = "aarch64"
            if arch in explorer.sisyphus_packages_by_arch:
                popular_packages = ["0ad", "0ad-debuginfo", "389-ds-base-devel"]

                logger.info(f"Проверка пакетов в архитектуре {arch}:")
                for pkg_name in popular_packages:
                    in_sisyphus = pkg_name in explorer.sisyphus_packages_names.get(arch, set())
                    in_p11 = pkg_name in explorer.p11_packages_names.get(arch, set())

                    status = []
                    if in_sisyphus:
                        pkg = explorer.sisyphus_packages_by_arch[arch][pkg_name]
                        status.append(f"S:{pkg.version}")
                    if in_p11:
                        pkg = explorer.p11_packages_by_arch[arch][pkg_name]
                        status.append(f"P11:{pkg.version}")

                    logger.info(f"  {pkg_name}: {' '.join(status) if status else 'отсутствует'}")

                    # Если пакет есть в обеих ветках, проверим версии
                    if in_sisyphus and in_p11:
                        sisyphus_pkg = explorer.sisyphus_packages_by_arch[arch][pkg_name]
                        p11_pkg = explorer.p11_packages_by_arch[arch][pkg_name]

                        if sisyphus_pkg.version != p11_pkg.version:
                            logger.info(f"    Разные версии: {sisyphus_pkg.version} vs {p11_pkg.version}")

            # Выполним сравнение версий для всех пакетов
            diff_count = processor.version_release_comparison()
            logger.info(f"Всего пакетов с разными версиями: {diff_count}\n")

        finally:
            os.chdir(original_dir)

    @pytest.mark.slow
    def test_cli_interface(self, tmp_path):
        """
        Запускаем программу как subprocess и проверяем вывод.
        """
        original_dir = os.getcwd()
        main_script = Path(__file__).parent.parent.parent / "main.py"
        assert main_script.exists(), f"main.py не найден по пути: {main_script}"

        # Переходим во временную директорию для файлов
        os.chdir(tmp_path)

        try:
            # Тестируем каждую команду
            commands = [
                "p11-not-in-sisyphus",
                "sisyphus-not-in-p11",
                "compare-versions"
            ]

            for cmd in commands:
                logger.info(f"Тестируем команду: {cmd}")

                # Запускаем с конкретной командой
                result = subprocess.run(
                    ["python", "-m", "main", cmd],
                    capture_output=True,
                    text=True
                )

                # Проверяем, что программа завершилась успешно
                assert result.returncode == 0, f"Command {cmd} failed: {result.stderr}"

                # Проверяем, что файлы созданы
                expected_files = {
                    "p11-not-in-sisyphus": "in_p11_not_in_sisyphus.json",
                    "sisyphus-not-in-p11": "in_sisyphus_not_in_p11.json",
                    "compare-versions": "version-release_compare.json"
                }

                filename = expected_files[cmd]
                file_path = Path(filename)
                assert file_path.exists(), f"Файл {filename} не создан"

                # Проверяем, что файл содержит JSON
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"{filename}: {len(data)} записей")

        finally:
            os.chdir(original_dir)

    @pytest.mark.slow
    def test_performance(self):
        """
        Замеряем время загрузки и обработки.
        """
        explorer = DataExplorer()

        # Замеряем только загрузку и первичную обработку
        start = time.time()
        explorer.explore_api()
        load_time = time.time() - start

        logger.info(f"Время загрузки и обработки: {load_time:.2f} секунд")

        # Создаем processor и замеряем сравнения
        processor = BranchProcessor(
            sisyphus_packages=explorer.sisyphus_packages_by_arch,
            p11_packages=explorer.p11_packages_by_arch,
            sisyphus_names=explorer.sisyphus_packages_names,
            p11_names=explorer.p11_packages_names
        )

        start = time.time()
        unique_p11 = processor.p11_not_in_sisyphus()
        unique_sisyphus = processor.sisyphus_not_in_p11()
        version_diffs = processor.version_release_comparison()
        compare_time = time.time() - start

        logger.info(f"Время сравнения: {compare_time:.2f} секунд")
        logger.info(f"Всего времени: {load_time + compare_time:.2f} секунд")

        # Проверяем, что все операции выполнились
        assert unique_p11 >= 0
        assert unique_sisyphus >= 0
        assert version_diffs >= 0

        # Проверяем, что время в разумных пределах
        total_time = load_time + compare_time
        assert total_time < 60, f"Слишком долго: {total_time:.2f} секунд"
