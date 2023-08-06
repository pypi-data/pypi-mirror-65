import os

from xlsx_parser import bootstrap
from xlsx_parser.xls_parser import XlsParserFormat

current_dir = os.path.abspath(os.path.normpath(os.path.dirname(__file__)))


def test_format_v1():
    samples_v1_dir = os.path.join(current_dir, 'input', 'samples_format_1')
    output_v1_file = os.path.join(current_dir, 'output', 'format_v1', 'results.xlsx')
    output_v1_report = os.path.join(current_dir, 'output', 'format_v1', 'report.txt')
    bootstrap.parse(samples_v1_dir, XlsParserFormat.first_format, output_v1_file, output_v1_report)


def test_format_v2():
    samples_v2_dir = os.path.join(current_dir, 'input', 'samples_format_2')
    output_v2_file = os.path.join(current_dir, 'output', 'format_v2', 'results.xlsx')
    output_v2_report = os.path.join(current_dir, 'output', 'format_v2', 'report.txt')
    bootstrap.parse(samples_v2_dir, XlsParserFormat.second_format, output_v2_file, output_v2_report)


def run():
    test_format_v1()
    test_format_v2()


if __name__ == '__main__':
    run()
