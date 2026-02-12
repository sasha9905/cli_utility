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

        self.sisyphus_packages_names: Dict[str, set[str]] = defaultdict(set)
        self.p11_packages_names: Dict[str, set[str]] = defaultdict(set)

        self.sisyphus_packages_by_arch: Dict[str, Dict[str, Package]] = defaultdict(dict)
        self.p11_packages_by_arch: Dict[str, Dict[str, Package]] = defaultdict(dict)

    @staticmethod
    def get_data_from_url(branch):
        url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data

        except requests.exceptions.Timeout:
            logger.error(f"Таймаут при запросе {branch}")
        except requests.exceptions.ConnectionError:
            logger.error(f"Ошибка соединения {branch}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP ошибка {e.response.status_code} {branch}")
        except json.JSONDecodeError:
            logger.error(f"Некорректный JSON {branch}")
        except Exception:
            logger.error(f"Неожиданная ошибка {branch}", exc_info=True)


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
            success = True
            for branch in self.branches:
                data = self.get_data_from_url(branch)
                if data is None:
                    logger.info(f"No data in file {branch}.json")
                    success = False
                    continue

                logger.info(f"Branch: {branch}")
                self.data[branch] = data.get("packages")
                logger.info(f"Branch {branch}, length {data.get('length')}")

            self._process_branch_packages("sisyphus", self.sisyphus_packages_by_arch, self.sisyphus_packages_names)
            self._process_branch_packages("p11", self.p11_packages_by_arch, self.p11_packages_names)
            return success

        except Exception:
            logger.error(f"Непредвиденная ошибка", exc_info=True)

    def _process_branch_packages(
            self, branch_name: str, packages_by_arch: Dict[str, Dict[str, Package]],
            packages_names: Dict[str, set[str]]
    ):
        """Общий метод обработки пакетов для любой ветки"""
        branch_raw: List[Dict[str, Any]] | None = self.data.get(branch_name)
        if branch_raw:
            for pkg_dict in branch_raw:
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
                packages_by_arch[arch][name] = package
                packages_names[arch].add(name)
