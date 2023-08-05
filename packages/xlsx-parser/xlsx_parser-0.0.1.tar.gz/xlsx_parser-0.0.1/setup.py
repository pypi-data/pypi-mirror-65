from setuptools import setup, find_packages

import xlsx_parser

setup(
    name='xlsx_parser',
    version=xlsx_parser.__version__,
    author='RuzzyRullezz',
    author_email='ruslan@lemimi.ru',
    packages=find_packages(),
    package_dir={'xlsx_parser': 'xlsx_parser'},
    install_requires=[
        'pyexcel==0.5.15',
        'pyexcel-xls==0.5.8',
        'pyexcel-xlsx==0.5.8',
        'pyexcel-xlsxr==0.5.2',
        'pyexcel-xlsxw==0.4.2',
    ],
)