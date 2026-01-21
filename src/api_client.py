import json

import requests
from requests.packages import package

from src.logging_config import logger

def get_data_from_url(branch):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception:
        logger.error(f"Непредвиденная ошибка при попытке получения данных по url в ветке {branch}", exc_info=True)

def get_data_from_file(branch):
    try:
        with open(f'{branch}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception:
        logger.error(f"Непредвиденная ошибка при попытке получения данных из файла {branch}.json", exc_info=True)

def explore_api():
    branches = ['sisyphus', 'p11']
    for branch in branches:
        try:
            data = get_data_from_file(branch)
            if data is None:
                logger.info(f"No data in file {branch}.json")
                return

            # Исследуйте:
            logger.info(f"Branch: {branch}")
            logger.info(f"Total keys of data: {len(data)}")

            request_args = data.get("request_args")
            length = data.get("length")
            packages = data.get("packages")

            logger.info(f"Request args: {request_args}")
            logger.info(f"Total length of packages: {length}")
            logger.info(f"Packages keys: {packages[0].keys()}")

            for key in packages[0].keys():
                logger.info(f"The type of value for key {key}: {type(packages[0].get(key))}")
                logger.info(f"The value for key {key}: {packages[0].get(key)}")

            logger.info(packages[0].keys())

        except Exception:
            logger.error(f"Непредвиденная ошибка", exc_info=True)
