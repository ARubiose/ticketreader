"""State strategy module.  https://refactoring.guru/design-patterns/state"""
import abc
import logging
from typing import Type

from pypdf import PdfReader, PageObject

from ticketreader.parser import ParserStrategy
from ticketreader.utils import FileHandlerMixin

logger = logging.getLogger(__name__)


class StateParserStrategy(ParserStrategy):
    """Parser strategy based on state pattern."""

    def parse(self, context: "ParseContext", *args, **kwargs) -> None:
        """Parse file using the current state"""
        self.current_context = context
        self.current_context.parse(*args, **kwargs)

    @property
    def current_context(self) -> "ParseContext":
        """Current context"""
        if not hasattr(self, "_current_context"):
            raise AttributeError("Current context not set")
        return self._current_context

    @current_context.setter
    def current_context(self, context: "ParseContext") -> None:
        """Current context"""
        if not isinstance(context, ParseContext):
            raise TypeError(f"Context must be a {ParseContext.__name__}")
        self._current_context = context

    @property
    def current_state(self) -> "ParseState":
        """Current state"""
        return self.current_context.state


class ParseState(abc.ABC):
    """Parse state"""

    @abc.abstractmethod
    def parse(self, *args, **kwargs) -> None:
        """Parse file"""
        raise NotImplementedError("Method not implemented")

    @property
    def context(self) -> "ParseContext":
        """Parse context"""
        return self._context

    @context.setter
    def context(self, context: "ParseContext") -> None:
        """Parse context"""
        if not isinstance(context, ParseContext):
            raise TypeError(f"Context must be a {ParseContext.__name__}")
        self._context = context


class ParseContext(abc.ABC):
    """Parse context"""

    INITIAL_STATE: Type[ParseState]

    def __init__(self, *args, **kwargs) -> None:
        self.change_state(self.INITIAL_STATE)

    @property
    def state(self) -> ParseState:
        """Parse state"""
        return self._state

    def change_state(self, state_type: Type[ParseState]) -> None:
        """Change state"""

        if not issubclass(state_type, ParseState):
            raise TypeError(f"State must be a {ParseState.__name__}")

        self._state = state_type()
        self.state.context = self

    def parse(self, *args, **kwargs) -> None:
        """Parse file"""
        raise NotImplementedError("Method not implemented")


class PyPDFParseContext(ParseContext, FileHandlerMixin):
    """PyPDF parse context"""

    def parse(self, *args, **kwargs) -> None:
        """Parse file"""
        reader = PdfReader(self.file_path)
        for page_num, page in enumerate(reader.pages):
            self._parse_page(page_num=page_num, page=page)

    def _parse_page(self, page_num: int, page: PageObject) -> None:
        """Parse page"""

        text = page.extract_text(space_width=0.5)
        lines = text.split("\n")

        logger.debug(f"parsing page {page_num} with {len(lines)} lines")

        for line_num, line in enumerate(lines):
            self.state.parse(line=line, line_num=line_num)
