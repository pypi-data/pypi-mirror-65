from collections import Iterable
from typing import Optional, List

from .xls_formats import XlsParserFormat


class XlsSheetReport:
    # Заполняются при инициализации
    file_path: str
    xls_format: XlsParserFormat
    sheet_name: str
    sheet_order: int
    rows_cnt: int
    # Заполняются после инициализации
    rows_processed: int
    rows_ignored: int

    def __init__(self, file_path, xls_format, sheet_name, sheet_order, rows_cnt):
        self.file_path = file_path
        self.xls_format = xls_format
        self.sheet_name = sheet_name
        self.sheet_order = sheet_order
        self.rows_cnt = rows_cnt
        self.rows_processed = 0
        self.rows_ignored = 0

    def __str__(self):
        return f"\tНазвание листа: {self.sheet_name} \n" \
               f"\tНомер листа: {self.sheet_order}\n" \
               f"\tСтрок обработано: {self.rows_processed}\n" \
               f"\tСтрок проигнорировано: {self.rows_ignored}\n" \
               f"\tСтрок всего: {self.rows_cnt}"


class XlsReport:
    file_path: str
    xls_format: XlsParserFormat
    sheet_reports: List[XlsSheetReport]
    error_msg: Optional[str]

    def __init__(self, file_path: str, xls_format: XlsParserFormat, sheet_reports: List[XlsSheetReport]):
        self.file_path = file_path
        self.xls_format = xls_format
        self.sheet_reports = sheet_reports
        self.error_msg = None

    def __str__(self):
        s = f"Имя: {self.file_path}\n" \
        f"Формат: {self.xls_format.value}\n"
        if self.error_msg:
            s += f"Ошибка: {self.error_msg if self.error_msg else ''}\n"
        s += f"Строки:\n" + '\n\t########\n'.join(map(str, self.sheet_reports))
        return s