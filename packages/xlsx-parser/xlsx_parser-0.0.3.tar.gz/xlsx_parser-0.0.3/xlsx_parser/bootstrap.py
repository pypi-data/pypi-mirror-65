import os
from pyexcel_xlsx import save_data
from typing import Iterable, Tuple

from . import consts
from . import arg_parse
from . import exceptions
from xlsx_parser.xls_finder import XlsFinder
from xlsx_parser.xls_parser import XlsParser, XlsParseResult, XlsParserFormat


def get_parsed_rows(xls_dir_path, xls_format: XlsParserFormat):
    for xls_file in XlsFinder(xls_dir_path).get_files():
        for row in XlsParser(xls_file, xls_format).parse():
            yield row


def get_counted_rows(rows: Iterable[XlsParseResult]) -> Iterable[Tuple]:
    counter = 0
    for row in rows:
        counter += 1
        yield (counter,) + row


def save_rows(output_file, rows: Iterable[XlsParseResult]):
    counted_rows = get_counted_rows(rows)
    save_data(output_file, counted_rows)


def parse(xls_dir: str, output_file: str, xls_format: XlsParserFormat):
    if os.path.exists(output_file):
        os.remove(output_file)
    try:
        rows = get_parsed_rows(xls_dir, xls_format)
        save_rows(output_file, rows)
        print(f"Данные сохранены в файл: {output_file}")
    except exceptions.XlsParseException as exc:
        print(exc.message)
        return


def run():
    xls_dir, output_dir, xls_format = arg_parse.parse()
    current_dir = os.path.abspath(os.path.normpath(os.getcwd()))
    if xls_dir is None:
        xls_dir = current_dir
    if output_dir is None:
        output_dir = os.path.join(current_dir, consts.default_result_dir_name)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_result_file_full_path = os.path.join(output_dir, consts.output_result_file_name)
    parse(xls_dir, output_result_file_full_path, xls_format)
