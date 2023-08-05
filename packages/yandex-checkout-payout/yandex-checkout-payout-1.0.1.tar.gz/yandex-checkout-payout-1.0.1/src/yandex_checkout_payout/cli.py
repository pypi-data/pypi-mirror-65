# -*- coding: utf-8 -*-
import argparse
import sys

import yandex_checkout_payout
from yandex_checkout_payout.domain.common.cli_client import CliClient


def main():

    parser = argparse.ArgumentParser(
        add_help=False,
        description='Консольный скрипт пакета yandex_checkout_payout.',
        epilog='Author: {}\nE-mail: {}\nVersion: {}'.format(yandex_checkout_payout.__author__,
                                                            yandex_checkout_payout.__email__,
                                                            yandex_checkout_payout.__version__)
    )

    parser.version = yandex_checkout_payout.__version__
    parser.add_argument('-getcsr', action='store_const', const=True, help='Генерация сертификата и ключей')
    parser.add_argument('-v', '--version', action='version', help='Показать версию программы и выйти')
    parser.add_argument('-h', '--help', action='help', help='Показать текст справки и выйти')
    args = parser.parse_args()

    if args.getcsr is not None:
        cli = CliClient()
        cli.generate()
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
