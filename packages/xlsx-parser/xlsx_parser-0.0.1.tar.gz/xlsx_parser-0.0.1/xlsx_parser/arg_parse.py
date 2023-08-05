from typing import Tuple

import argparse


def parse() -> Tuple[str, str]:
    parser = argparse.ArgumentParser(
        description="Парсер xls/xlsx-файлов для загрузки в реестр",
    )
    parser.add_argument("--folder", "-f", type=str, help="Директория с xls/xlsx-файлами",
                        required=False, default=None)
    parser.add_argument("--output", "-o", type=str,
                        help="Путь к директории с выводом",
                        required=False, default=None)
    options = parser.parse_args()
    return options.folder, options.output
