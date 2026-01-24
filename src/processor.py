from typing import List, Dict

from src.api_client import DataExplorer
from src.models import Package


class BranchProcessor:

    def __init__(self, data_explorer: DataExplorer):
        self.data_explorer = data_explorer

        self.sisyphus_packages_by_arch: Dict[str, List[Package]] = self.data_explorer.sisyphus_packages_by_arch
        self.p11_packages_by_arch: Dict[str, List[Package]] = self.data_explorer.p11_packages_by_arch

        self.sisyphus_packages_names: Dict[str, set[str]] = self.data_explorer.sisyphus_packages_names
        self.p11_packages_names: Dict[str, set[str]] = self.data_explorer.p11_packages_names


    def p11_not_in_sisyphus(self):
        counter = 0
        counter_2 = 0
        for arch_type in self.p11_packages_by_arch.keys():
            for package in self.p11_packages_by_arch[arch_type]:
                if package.name not in self.sisyphus_packages_names[arch_type]:
                    counter += 1

        return counter


    def sisyphus_not_in_p11(self):
        counter = 0
        counter_2 = 0
        for arch_type in self.sisyphus_packages_by_arch.keys():
            for package in self.sisyphus_packages_by_arch[arch_type]:
                if package.name not in self.p11_packages_names[arch_type]:
                    counter += 1

        return counter

    def version_release_comparison(self):
        ...
