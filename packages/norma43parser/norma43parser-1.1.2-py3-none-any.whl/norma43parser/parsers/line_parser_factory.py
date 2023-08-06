from typing import Dict, Type

from .end_of_file_parser import EndOfFileParser
from .footer_parser import FooterParser
from .header_parser import HeaderParser
from .line_parser import LineParser
from .line_type import LineType
from .movement_line_extra_information_parser import MovementLineExtraInformationParser
from .movement_line_parser import MovementLineParser

_TYPE_TO_PARSER_MAP: Dict[LineType, Type[LineParser]] = {
    LineType.HEADER: HeaderParser,
    LineType.MOVEMENT_LINE: MovementLineParser,
    LineType.MOVEMENT_LINE_EXTRA_INFORMATION: MovementLineExtraInformationParser,
    LineType.FOOTER: FooterParser,
    LineType.END_OF_FILE: EndOfFileParser,
}


class LineParserFactory:
    @staticmethod
    def get_instance(type: LineType) -> Type[LineParser]:
        return _TYPE_TO_PARSER_MAP[type]
