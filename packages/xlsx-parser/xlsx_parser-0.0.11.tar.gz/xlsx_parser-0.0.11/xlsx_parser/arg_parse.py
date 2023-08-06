from typing import Tuple

import argparse

from .xls_formats import XlsParserFormat


def parse() -> Tuple[str, str, XlsParserFormat]:
    parser = argparse.ArgumentParser(
        description="Парсер xls/xlsx-файлов для загрузки в реестр",
    )
    parser.add_argument("--folder", "-f", type=str, help="Директория с xls/xlsx-файлами",
                        required=False, default=None)
    parser.add_argument("--output", "-o", type=str,
                        help="Путь к директории с выводом",
                        required=False, default=None)
    parser.add_argument("--format", type=int,
                        help="Формат данных",
                        required=False, default=XlsParserFormat.first_format.value)
    options = parser.parse_args()
    return options.folder, options.output, XlsParserFormat(options.format)
