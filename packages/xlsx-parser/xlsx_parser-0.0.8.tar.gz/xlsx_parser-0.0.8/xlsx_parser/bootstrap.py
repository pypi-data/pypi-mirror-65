import os
from pyexcel_xlsx import save_data
from typing import Iterable, Tuple, List

from xlrd import XLRDError

from . import consts
from . import arg_parse
from . import exceptions
from . import report
from xlsx_parser.xls_finder import XlsFinder
from xlsx_parser.xls_parser import XlsParser, XlsParseResult, XlsParserFormat


def get_parsed_rows(xls_dir_path, xls_format: XlsParserFormat, xls_reports_list: List[report.XlsReport]):
    for xls_file in XlsFinder(xls_dir_path).get_files():
        try:
            for row in XlsParser(xls_file, xls_format).parse(xls_reports_list=xls_reports_list):
                yield row
        except XLRDError:
            print(f"Ошибка парсинга файла {xls_file}")


def get_counted_rows(rows: Iterable[XlsParseResult]) -> Iterable[Tuple]:
    counter = 0
    for row in rows:
        counter += 1
        yield (counter,) + row


def save_rows(output_file, rows: Iterable[XlsParseResult]):
    counted_rows = get_counted_rows(rows)
    save_data(output_file, counted_rows)
    print(f"Данные сохранены в файл: {output_file}")


def save_reports(report_file: str, xls_reports_list: List[report.XlsReport]):
    for_write = ""
    for rep in xls_reports_list:
        for_write += str(rep) + "\n\n"
    with open(report_file, 'w') as wf:
        wf.write(for_write)
    print(for_write)
    print(f"Отчет сохранен в файл: {report_file}")


def parse(xls_dir: str, xls_format: XlsParserFormat, result_file: str, report_file: str):
    if os.path.exists(result_file):
        os.remove(result_file)
    if os.path.exists(report_file):
        os.remove(report_file)
    try:
        xls_reports_list = []
        rows = get_parsed_rows(xls_dir, xls_format, xls_reports_list)
        save_rows(result_file, rows)
        save_reports(report_file, xls_reports_list)
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
    output_report_file_full_path = os.path.join(output_dir, consts.output_report_file_name)
    parse(xls_dir, xls_format, output_result_file_full_path, output_report_file_full_path)
