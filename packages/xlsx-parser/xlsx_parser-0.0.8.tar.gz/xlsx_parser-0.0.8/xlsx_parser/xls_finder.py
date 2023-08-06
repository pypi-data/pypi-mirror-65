import glob
from typing import Generator

from . import consts


class XlsFinder:
    source_dir: str

    files_extensions = (
        '.xlsx',
        '.xls',
    )

    def __init__(self, source_dir: str):
        self.source_dir = source_dir

    def get_files(self) -> Generator[str, None, None]:
        for ext in self.files_extensions:
            for path in glob.iglob(self.source_dir + f'/**/*{ext}', recursive=True):
                if consts.output_result_file_name in path:
                    continue
                yield path
