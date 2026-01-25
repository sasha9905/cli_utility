from typing import List, Dict

from src.api_client import DataExplorer
from src.models import Package


class BranchProcessor:

    def __init__(self, data_explorer: DataExplorer):
        self.data_explorer = data_explorer

        self.sisyphus_packages_by_arch: Dict[str, Dict[str, Package]] = self.data_explorer.sisyphus_packages_by_arch
        self.p11_packages_by_arch: Dict[str, Dict[str, Package]] = self.data_explorer.p11_packages_by_arch

        self.sisyphus_packages_names: Dict[str, set[str]] = self.data_explorer.sisyphus_packages_names
        self.p11_packages_names: Dict[str, set[str]] = self.data_explorer.p11_packages_names

    def p11_not_in_sisyphus(self):
        counter = 0
        for arch_type in self.p11_packages_by_arch.keys():
            for name, package in self.p11_packages_by_arch[arch_type].items():
                if package.name not in self.sisyphus_packages_names[arch_type]:
                    counter += 1

        return counter

    def sisyphus_not_in_p11(self):
        counter = 0
        for arch_type in self.sisyphus_packages_by_arch.keys():
            for name, package in self.sisyphus_packages_by_arch[arch_type].items():
                if package.name not in self.p11_packages_names[arch_type]:
                    counter += 1

        return counter

    def version_release_comparison(self):
        counter = 0
        for arch_type in self.sisyphus_packages_by_arch.keys():
            for name, package in self.sisyphus_packages_by_arch[arch_type].items():
                if package.name in self.p11_packages_names[arch_type]:
                    sisyphus_version, sisyphus_release = package.version, package.release
                    p11_package = self.p11_packages_by_arch[arch_type][name]
                    p11_version, p11_release = p11_package.version, p11_package.release

                    result = self._version_release(
                        sisyphus_version, sisyphus_release, p11_version, p11_release
                    )
                    if result:
                        counter += 1

        return counter

    def _version_release(self, sisyphus_version: str, sisyphus_release: str,
                         p11_version: str, p11_release: str):

        return True
