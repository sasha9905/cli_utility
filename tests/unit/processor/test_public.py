from unittest.mock import patch
from src.processor import BranchProcessor
from tests.fixtures.package_factory import create_package_object

class TestPublicMethods:
    """
    Тестирование публичных методов через мокинг внутренних.
    """

    def test_version_release_comparison_result_aggregation(self, tmp_path):
        """Проверяет, что результаты правильно агрегируются."""
        # Создаем несколько пакетов с разными результатами сравнения
        pkg1_s = create_package_object(name="pkg1", version="1.0.0")
        pkg1_p = create_package_object(name="pkg1", version="1.0.0")  # равны

        pkg2_s = create_package_object(name="pkg2", version="2.0.0")
        pkg2_p = create_package_object(name="pkg2", version="1.0.0")  # разные

        pkg3_s = create_package_object(name="pkg3", version="1.0.0")
        pkg3_p = create_package_object(name="pkg3", version="2.0.0")  # разные

        sisyphus = {"x86_64": {"pkg1": pkg1_s, "pkg2": pkg2_s, "pkg3": pkg3_s}}
        p11 = {"x86_64": {"pkg1": pkg1_p, "pkg2": pkg2_p, "pkg3": pkg3_p}}
        names = {"x86_64": {"pkg1", "pkg2", "pkg3"}}

        processor = BranchProcessor(sisyphus, p11, names, names)

        result = processor.version_release_comparison()

        assert result == 1

    def test_convert_packages_to_json_called(self, processor_with_different_versions):
        """Проверяет, что convert_packages_to_json вызывается для сохранения результатов."""
        with patch.object(BranchProcessor, 'convert_packages_to_json') as mock_convert:
            processor_with_different_versions.version_release_comparison()

            mock_convert.assert_called_once()
            args, kwargs = mock_convert.call_args

            assert isinstance(args[0], list)  # список пакетов
            assert args[1] == "version-release_compare"

    def test_methods_can_be_called_multiple_times(self, processor_with_data):
        """Методы можно вызывать несколько раз."""
        count1 = processor_with_data.p11_not_in_sisyphus()
        # Второй вызов должен работать так же
        count2 = processor_with_data.p11_not_in_sisyphus()

        assert count1 == count2
