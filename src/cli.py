import argparse


def setup_argparse() -> argparse.ArgumentParser:
    """Настройка парсера аргументов"""
    parser = argparse.ArgumentParser(
        description='Сравнение пакетов между ветками Sisyphus и p11 ALT Linux',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s compare-versions
  %(prog)s p11-not-in-sisyphus
  %(prog)s sisyphus-not-in-p11
  %(prog)s compare-versions
        """
    )
    subparsers = parser.add_subparsers(
        dest='command',
        help='Доступные команды',
        required=True
    )

    # Команда 1: Сравнение версий
    compare_parser = subparsers.add_parser(
        'compare-versions',
        help='Сравнить версии пакетов между ветками'
    )

    # Команда 2: Пакеты только в p11
    p11_parser = subparsers.add_parser(
        'p11-not-in-sisyphus',
        help='Показать пакеты, которые есть в p11, но нет в Sisyphus'
    )

    # Команда 3: Пакеты только в Sisyphus
    sisyphus_parser = subparsers.add_parser(
        'sisyphus-not-in-p11',
        help='Показать пакеты, которые есть в Sisyphus, но нет в p11'
    )

    return parser
