from enum import Enum


class LineType(Enum):
    HEADER = 11
    MOVEMENT_LINE = 22
    MOVEMENT_LINE_EXTRA_INFORMATION = 23
    FOOTER = 33
    END_OF_FILE = 88

    @staticmethod
    def get_line_type(line: str) -> "LineType":
        identifier = int(line[:2])
        return LineType(identifier)
