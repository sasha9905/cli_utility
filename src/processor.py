import json
from dataclasses import asdict
from typing import Dict, List

from src.models import Package
from src.comparator import RPMVersionComparator

P11_NOT_IN_SISYPHUS = "in_p11_not_in_sisyphus"
SISYPHUS_NOT_IN_P11 = "in_sisyphus_not_in_p11"
VERSION_COMPARE = "version-release_compare"


class BranchProcessor:

    def __init__(self,
                 sisyphus_packages: Dict,
                 p11_packages: Dict,
                 sisyphus_names: Dict,
                 p11_names: Dict,
        ):
        self.sisyphus_packages_by_arch: Dict[str, Dict[str, Package]] = sisyphus_packages
        self.p11_packages_by_arch: Dict[str, Dict[str, Package]] = p11_packages

        self.sisyphus_packages_names: Dict[str, set[str]] = sisyphus_names
        self.p11_packages_names: Dict[str, set[str]] = p11_names

    def p11_not_in_sisyphus(self):
        return self._find_unique_packages(
            self.p11_packages_by_arch, self.sisyphus_packages_names, P11_NOT_IN_SISYPHUS)

    def sisyphus_not_in_p11(self):
        return self._find_unique_packages(
            self.sisyphus_packages_by_arch, self.p11_packages_names, SISYPHUS_NOT_IN_P11)

    def version_release_comparison(self):
        packages_array: List[Package] = []
        counter = 0
        for arch_type in self.sisyphus_packages_by_arch.keys():
            for name, package in self.sisyphus_packages_by_arch[arch_type].items():
                if package.name in self.p11_packages_names[arch_type]:
                    sisyphus_epoch = package.epoch
                    sisyphus_version, sisyphus_release = package.version, package.release

                    p11_package = self.p11_packages_by_arch[arch_type][name]
                    p11_epoch = p11_package.epoch
                    p11_version, p11_release = p11_package.version, p11_package.release

                    result = RPMVersionComparator.compare_versions(sisyphus_epoch, sisyphus_version,
                            sisyphus_release, p11_epoch, p11_version, p11_release
                    )
                    if result == 1:
                        packages_array.append(package)
                        counter += 1
        self.convert_packages_to_json(packages_array, VERSION_COMPARE)
        return counter

    @staticmethod
    def _find_unique_packages(
            source_packages: Dict[str, Dict[str, Package]],
            target_names: Dict[str, set[str]], filename: str
    ):
        """Находит пакеты, которые есть в source, но нет в target"""
        packages: List[Package] = []
        counter = 0
        for arch_type in source_packages.keys():
            for name, package in source_packages[arch_type].items():
                if package.name not in target_names[arch_type]:
                    counter += 1
                    packages.append(package)
        BranchProcessor.convert_packages_to_json(packages, filename)
        return counter

    @staticmethod
    def convert_packages_to_json(packages: List[Package], filename: str) -> str:
        if not filename.endswith('.json'):
            filename = f"{filename}.json"

        # Просто преобразуем dataclass в словари и сохраняем
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([asdict(pkg) for pkg in packages], f, indent=2)

        return filename
