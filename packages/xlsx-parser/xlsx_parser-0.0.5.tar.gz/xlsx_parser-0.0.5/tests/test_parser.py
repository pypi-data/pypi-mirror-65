import os

from xlsx_parser import bootstrap
from xlsx_parser.xls_parser import XlsParserFormat

current_dir = os.path.abspath(os.path.normpath(os.path.dirname(__file__)))


def test_format_v1():
    samples_v1_dir = os.path.join(current_dir, 'input', 'samples_format_1')
    output_v1_file = os.path.join(current_dir, 'output', 'format_v1', 'results.xlsx')
    bootstrap.parse(samples_v1_dir, output_v1_file, XlsParserFormat.first_format)


def test_format_v2():
    samples_v2_dir = os.path.join(current_dir, 'input', 'samples_format_2')
    output_v2_file = os.path.join(current_dir, 'output', 'format_v2', 'results.xlsx')
    bootstrap.parse(samples_v2_dir, output_v2_file, XlsParserFormat.second_format)


def run():
    test_format_v1()
    test_format_v2()


if __name__ == '__main__':
    run()
