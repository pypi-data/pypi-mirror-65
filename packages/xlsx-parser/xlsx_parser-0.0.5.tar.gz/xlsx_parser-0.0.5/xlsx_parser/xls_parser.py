import itertools
from enum import Enum, auto, unique

from typing import Optional, Iterable
from collections import namedtuple

from xlrd.biffh import XLRDError
from pyexcel_xlsxr import get_data

from .exceptions import XlsParseException


@unique
class XlsParserFormat(Enum):
    first_format = 1
    second_format = auto()


XlsParseResult = namedtuple(
    'Point', [
        'last_name',
        'document_series',
        'document_number',
        'date_of_birth',
        'entity_name',
        'entity_inn',
    ])


class XlsParser:
    xls_path: str
    xls_format: XlsParserFormat

    def __init__(self, xls_path: str, xls_format: XlsParserFormat):
        self.xls_path = xls_path
        self.xls_format = xls_format

    def process_row_v1(self, row) -> Optional[XlsParseResult]:
        # Обработка строки, где указаны фамилия и год рождения
        if len(row) < 7:
            print(f"ФАЙЛ НЕ СООТВЕСТВУЕТ ФОРМАТУ {XlsParserFormat.first_format.value} - {self.xls_path}, СТРОКА: {row}")
            return
        last_name = row[1]
        document_series = str(row[2])
        document_number = str(row[3])
        date_of_birth = row[4]
        try:
            entity_name = row[5].replace('\r\n', '').strip()
        except IndexError:
            print(f"ВНИМАНИЕ! {self.xls_path} - не указано наименование организации ")
            entity_name = f"ОШИБКА НЕ УКАЗАНО НАЗВАНИЕ ОРГАНИЗАЦИИ {self.xls_path}"
        try:
            entity_inn = row[6]
        except IndexError:
            print(f"ВНИМАНИЕ! {self.xls_path} - не указан ИНН организации ")
            entity_inn = f"ОШИБКА НЕ УКАЗАН ИНН ОРГАНИЗАЦИИ {self.xls_path}"
        return self.create_result(last_name=last_name, document_series=document_series, document_number=document_number,
                                  date_of_birth=date_of_birth, entity_name=entity_name, entity_inn=entity_inn)

    def process_row_v2(self, row) -> Optional[XlsParseResult]:
        # Обработка строки, где не указаны фамилия и год рождения
        if len(row) != 5:
            print(f"ФАЙЛ НЕ СООТВЕСТВУЕТ ФОРМАТУ {XlsParserFormat.second_format.value} - {self.xls_path}, СТРОКА: {row}")
            return None
        document_series = str(row[1])
        document_number = str(row[2])
        try:
            entity_name = row[3].replace('\r\n', '').strip()
        except IndexError:
            print(f"ВНИМАНИЕ! {self.xls_path} - не указано наименование организации ")
            entity_name = f"ОШИБКА НЕ УКАЗАНО НАЗВАНИЕ ОРГАНИЗАЦИИ {self.xls_path}"
        try:
            entity_inn = row[4]
        except IndexError:
            print(f"ВНИМАНИЕ! {self.xls_path} - не указан ИНН организации ")
            entity_inn = f"ОШИБКА НЕ УКАЗАН ИНН ОРГАНИЗАЦИИ {self.xls_path}"
        return self.create_result(document_series=document_series, document_number=document_number,
                                  entity_name=entity_name, entity_inn=entity_inn)

    def create_result(self, **params):
        # Обязательный параметры
        document_series = params['document_series']
        document_number = params['document_number']
        entity_name = params['entity_name']
        entity_inn = params['entity_inn']
        # Необязательные параметры
        last_name = params.get('last_name')
        date_of_birth = params.get('date_of_birth')
        # удаляем шапку
        if 'серия' in document_series.lower() and 'номер' in document_number.lower():
            return None
        # Удаляет пробелы и табуляции в колонках C и D
        document_series = document_series.replace(' ', '').replace('\t', '').strip()
        document_number = document_number.replace(' ', '').replace('\t', '').strip()
        # проверяет что в столбце C все данные 4 символа, колонке D - 6 символов, в случае если цифр меньше, заполняет недостающие нулями спереди ('0 или '00 или '000)
        document_series = document_series.rjust(4, '0')
        document_number = document_number.rjust(6, '0')
        # В колонке F заменяет все /r/n на пробел
        entity_name = entity_name.replace('\r\n', '').strip()
        return XlsParseResult(
            last_name=last_name,
            document_series=document_series,
            document_number=document_number,
            date_of_birth=date_of_birth,
            entity_name=entity_name,
            entity_inn=entity_inn,
        )

    def process_row(self, row) -> Optional[XlsParseResult]:
        if self.xls_format == XlsParserFormat.first_format:
            return self.process_row_v1(row)
        elif self.xls_format == XlsParserFormat.second_format:
            return self.process_row_v2(row)
        else:
            raise Exception(f"Неизвестный формат файла: {self.xls_format}")

    def parse(self) -> Iterable[Optional[XlsParseResult]]:
        try:
            records = get_data(self.xls_path)
        except XLRDError:
            print(f"{self.xls_path} is corrupted")
        else:
            merged_data_by_sheets = itertools.chain.from_iterable(records.values())
            # Удаляем пустые строки
            rows = filter(lambda l: len(l) > 0, filter(lambda v: bool(v), merged_data_by_sheets))
            # Обабатываем кажду строку
            for row in rows:
                result_row = self.process_row(row)
                if result_row is None:
                    continue
                yield result_row
