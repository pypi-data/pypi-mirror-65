import itertools
from typing import Optional, Iterable
from collections import namedtuple

from xlrd.biffh import XLRDError
from pyexcel_xlsxr import get_data


XlsParseResult = namedtuple('Point', ['order', 'last_name',
                                      'document_series', 'document_number', 'date_of_birth',
                                      'entity_name', 'entity_inn'])


class XlsParser:
    xls_path: str

    def __init__(self, xls_path):
        self.xls_path = xls_path

    def process_row(self, row) -> Optional[XlsParseResult]:
        order: str = row[0]
        if not isinstance(order, int):
            return None
        document_series = str(row[2])
        document_number = str(row[3])
        # Удаляет пробелы и табуляции в колонках C и D
        document_series = document_series.replace(' ', '').replace('\t', '').strip()
        document_number = document_number.replace(' ', '').replace('\t', '').strip()
        # проверяет что в столбце C все данные 4 символа, колонке D - 6 символов, в случае если цифр меньше, заполняет недостающие нулями спереди ('0 или '00 или '000)
        document_series = document_series.rjust(4, '0')
        document_number = document_number.rjust(6, '0')
        # В колонке F заменяет все /r/n на пробел
        entity_name = row[5].replace('\r\n', '').strip()
        return XlsParseResult(
            order=order,
            last_name=row[1],
            document_series=document_series,
            document_number=document_number,
            date_of_birth=row[4],
            entity_name=entity_name,
            entity_inn=row[6],
        )

    def parse(self) -> Iterable[Optional[XlsParseResult]]:
        try:
            records = get_data(self.xls_path)
        except XLRDError:
            print(f"{self.xls_path} is corrupted")
        else:
            merged_data_by_sheets = itertools.chain.from_iterable(records.values())
            # Удаляем пустые строки
            rows = filter(lambda l: len(l) == 7, filter(lambda v: bool(v), merged_data_by_sheets))
            # Обабатываем кажду строку
            for row in rows:
                result_row = self.process_row(row)
                if result_row is None:
                    continue
                yield result_row
