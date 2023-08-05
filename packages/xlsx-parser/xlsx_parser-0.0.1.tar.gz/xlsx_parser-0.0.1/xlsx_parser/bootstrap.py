import os
from pyexcel_xlsx import save_data
from typing import Iterable

from . import arg_parse
from xlsx_parser.xls_finder import XlsFinder
from xlsx_parser.xls_parser import XlsParser, XlsParseResult


def get_parsed_rows(xls_dir_path):
    for xls_file in XlsFinder(xls_dir_path).get_files():
        for row in XlsParser(xls_file).parse():
            yield row


def save_rows(output_file, rows: Iterable[XlsParseResult]):
    save_data(output_file, rows)


def run():
    output_result_file_name = 'report.xlsx'
    xls_dir, output_dir = arg_parse.parse()
    current_dir = os.path.abspath(os.path.normpath(os.getcwd()))
    if xls_dir is None:
        xls_dir = current_dir
    if output_dir is None:
        default_done_dir_name = "done"
        output_dir = os.path.join(current_dir, default_done_dir_name)
    output_result_file_full_path = os.path.join(output_dir, output_result_file_name)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if os.path.exists(output_result_file_full_path):
        os.remove(output_result_file_full_path)
    rows = get_parsed_rows(xls_dir)
    save_rows(output_result_file_full_path, rows)
    print(f"Data save to {output_result_file_full_path}")