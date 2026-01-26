import sys

from src import logger, setup_argparse, DataExplorer, BranchProcessor


def main():
    """Точка входа CLI"""
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        # Инициализация DataExplorer
        logger.info(f"Инициализация DataExplorer")
        data_explorer = DataExplorer()
        data_explorer.explore_api()

        processor = BranchProcessor(data_explorer)

        # Выполнение команды
        logger.info(f"Выполнение команды: {args.command}")

        if args.command == 'p11-not-in-sisyphus':
            result = processor.p11_not_in_sisyphus()

        elif args.command == 'sisyphus-not-in-p11':
            result = processor.sisyphus_not_in_p11()

        elif args.command == 'compare-versions':
            result = processor.version_release_comparison()
        else:
            result = "Unexpected command"

        if result:
            logger.info(f"Результат команды {args.command}: {result}")

    except KeyboardInterrupt:
        print("\n\nПрервано пользователем", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()