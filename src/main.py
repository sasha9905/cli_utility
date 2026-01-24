from src.logging_config import logger
from src.api_client import DataExplorer
from src.processor import BranchProcessor


def main():
    """Entry point for CLI."""
    data_explorer = DataExplorer()
    data_explorer.explore_api()

    processor = BranchProcessor(data_explorer)
    logger.info(processor.p11_not_in_sisyphus())
    logger.info(processor.sisyphus_not_in_p11())


if __name__ == '__main__':
    main()