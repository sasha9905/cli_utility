import json
from collections import defaultdict
from typing import List, Dict, Any

import requests

from src.logging_config import logger
from src.models import Package


class DataExplorer:
    branches = ['sisyphus', 'p11']

    def __init__(self):
        self.data = {}
        self.sisyphus_raw: List[Dict[str, Any]] | None = None
        self.p11_raw: List[Dict[str, Any]] | None = None

        self.sisyphus_packages_names: Dict[str, set[str]] | Dict[Any, Any] = defaultdict(set)
        self.p11_packages_names: Dict[str, set[str]] | Dict[Any, Any] = defaultdict(set)

        self.sisyphus_packages_by_arch: Dict[str, Dict[str, Package]] | Dict[Any, Any] = defaultdict(dict)
        self.p11_packages_by_arch: Dict[str, Dict[str, Package]]| Dict[Any, Any] = defaultdict(dict)

    @staticmethod
    def get_data_from_url(branch):
        url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
        try:
            response = requests.get(url)
            data = response.json()
            return data
        except Exception:
            logger.error(f"Непредвиденная ошибка при попытке получения данных по url в ветке {branch}", exc_info=True)

    @staticmethod
    def get_data_from_file(branch):
        try:
            with open(f'{branch}.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except Exception:
            logger.error(f"Непредвиденная ошибка при попытке получения данных из файла {branch}.json", exc_info=True)

    def explore_api(self):
        try:
            for branch in self.branches:
                data = self.get_data_from_url(branch)
                if data is None:
                    logger.info(f"No data in file {branch}.json")
                    return

                logger.info(f"Branch: {branch}")
                self.data[branch] = data.get("packages")
                logger.info(f"Branch {branch}, length {data.get('length')}")

            self.data_processor()

        except Exception:
            logger.error(f"Непредвиденная ошибка", exc_info=True)

    def data_processor(self):
        self.sisyphus_raw = self.data.get("sisyphus")
        self.p11_raw = self.data.get("p11")

        # Преобразуем словари в объекты Package
        if self.sisyphus_raw:
            for pkg_dict in self.sisyphus_raw:
                name = pkg_dict.get("name", "")
                arch = pkg_dict.get("arch", "")
                package = Package(
                        name=name,
                        epoch=pkg_dict.get("epoch", 0),
                        version=pkg_dict.get("version", ""),
                        release=pkg_dict.get("release", ""),
                        arch=arch,
                        buildtime=pkg_dict.get("buildtime", 0),
                        source=pkg_dict.get("source", "")
                    )
                self.sisyphus_packages_by_arch[arch][name] = package
                self.sisyphus_packages_names[arch].add(name)


        if self.p11_raw:
            for pkg_dict in self.p11_raw:
                name = pkg_dict.get("name", "")
                arch = pkg_dict.get("arch", "")
                package = Package(
                    name=name,
                    epoch=pkg_dict.get("epoch", 0),
                    version=pkg_dict.get("version", ""),
                    release=pkg_dict.get("release", ""),
                    arch=arch,
                    buildtime=pkg_dict.get("buildtime", 0),
                    source=pkg_dict.get("source", "")
                )
                self.p11_packages_by_arch[arch][name] = package
                self.p11_packages_names[arch].add(name)

