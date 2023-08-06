from enum import unique, Enum, auto


@unique
class XlsParserFormat(Enum):
    first_format = 1
    second_format = auto()
