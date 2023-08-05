import os

from xlsx_parser import bootstrap

current_dir = os.path.abspath(os.path.normpath(os.path.dirname(__file__)))
samples_dir = os.path.join(current_dir, 'samples')
output_file = os.path.join(current_dir, 'output', 'results.xlsx')


def run():
    bootstrap.parse(samples_dir, output_file)


if __name__ == '__main__':
    run()
