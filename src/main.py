from src.logging_config import logger
from src.api_client import explore_api


def main():
    """Entry point for CLI."""
    explore_api()


if __name__ == '__main__':
    main()