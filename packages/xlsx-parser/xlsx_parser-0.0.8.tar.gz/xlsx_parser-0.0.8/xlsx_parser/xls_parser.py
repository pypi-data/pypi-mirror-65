from typing import Optional, Iterable, List
from collections import namedtuple

import pyexcel
from xlrd.biffh import XLRDError

from .report import XlsSheetReport, XlsReport
from .xls_formats import XlsParserFormat


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
            return None
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
        if len(row) < 5:
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

    def parse(self, xls_reports_list: List[XlsReport] = None) -> Iterable[Optional[XlsParseResult]]:
        sheet_reports = []
        xls_report = XlsReport(self.xls_path, self.xls_format, sheet_reports)
        xls_reports_list.append(xls_report)
        try:
            book = pyexcel.get_book(file_name=self.xls_path)
        except XLRDError:
            xls_report.error_msg = f"Ошибка парсинга файла {self.xls_path}"
            raise
        sheet_numbers = book.number_of_sheets()
        for sheet_number in range(sheet_numbers):
            sheet = book.sheet_by_index(sheet_number)
            report = XlsSheetReport(
                self.xls_path,
                self.xls_format,
                sheet.name,
                sheet_number,
                sheet.number_of_rows(),
            )
            for row in sheet:
                result_row = self.process_row(row)
                if result_row is None:
                    report.rows_ignored += 1
                    continue
                report.rows_processed += 1
                yield result_row
            sheet_reports.append(report)