"""File parser module. It contains the FileParser class and the ParserStrategy interface."""
import os
import abc
import logging

logger = logging.getLogger(__name__)

class FileParser(abc.ABC):
    """Main file manager class. It uses a parse strategy to parse the file."""

    def __init__(self, parse_strategy: "ParserStrategy") -> None:
        self._strategy = parse_strategy

    @property
    def strategy(self) -> "ParserStrategy":
        """Parse strategy"""
        return self._strategy

    def parse(self, *args, **kwargs) -> None:
        """Parse file"""
        self.strategy.parse(*args, **kwargs)


class ParserStrategy(abc.ABC):
    """Parser strategy interface"""

    @abc.abstractmethod
    def parse(self, file_path:os.PathLike, *args, **kwargs) -> None:
        """Parse file"""
        raise NotImplementedError("Method not implemented")







    