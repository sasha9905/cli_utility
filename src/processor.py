import json
from dataclasses import asdict
from typing import Dict, List

from src.api_client import DataExplorer
from src.models import Package
from src.comporator import RPMVersionComparator


class BranchProcessor:

    def __init__(self, data_explorer: DataExplorer):
        self.data_explorer = data_explorer

        self.sisyphus_packages_by_arch: Dict[str, Dict[str, Package]] = self.data_explorer.sisyphus_packages_by_arch
        self.p11_packages_by_arch: Dict[str, Dict[str, Package]] = self.data_explorer.p11_packages_by_arch

        self.sisyphus_packages_names: Dict[str, set[str]] = self.data_explorer.sisyphus_packages_names
        self.p11_packages_names: Dict[str, set[str]] = self.data_explorer.p11_packages_names

    def p11_not_in_sisyphus(self):
        packages_array: List[Package] = []
        counter = 0
        for arch_type in self.p11_packages_by_arch.keys():
            for name, package in self.p11_packages_by_arch[arch_type].items():
                if package.name not in self.sisyphus_packages_names[arch_type]:
                    counter += 1
                    packages_array.append(package)
        self.convert_packages_to_json(packages_array, "in_p11_not_in_sisyphus")
        return counter

    def sisyphus_not_in_p11(self):
        packages_array: List[Package] = []
        counter = 0
        for arch_type in self.sisyphus_packages_by_arch.keys():
            for name, package in self.sisyphus_packages_by_arch[arch_type].items():
                if package.name not in self.p11_packages_names[arch_type]:
                    counter += 1
                    packages_array.append(package)
        self.convert_packages_to_json(packages_array, "in_sisyphus_not_in_p11")
        return counter

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
        self.convert_packages_to_json(packages_array, "version-release_compare")
        return counter

    @staticmethod
    def convert_packages_to_json(packages: List[Package], filename: str) -> str:
        if not filename.endswith('.json'):
            filename = f"{filename}.json"

        # Просто преобразуем dataclass в словари и сохраняем
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([asdict(pkg) for pkg in packages], f, indent=2)

        return filename
