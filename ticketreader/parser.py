"""File parser module. It contains the FileParser class and the ParserStrategy interface."""
import os
import abc
import logging
from typing import TypeVar, Generic

from ticketreader.schemas import Ticket

logger = logging.getLogger(__name__)

TicketType = TypeVar("TicketType", bound=Ticket)


class ParserStrategy(abc.ABC, Generic[TicketType]):
    """Parser strategy interface"""

    @abc.abstractmethod
    def parse(self, *args, **kwargs) -> TicketType:
        """Parse file"""
        raise NotImplementedError("Method not implemented")


class FileParser(abc.ABC, Generic[TicketType]):
    """Main file manager class. It uses a parse strategy to parse the file."""

    def __init__(self, parse_strategy: ParserStrategy) -> None:
        self._strategy = parse_strategy

    @property
    def strategy(self) -> ParserStrategy[TicketType]:
        """Parse strategy"""
        return self._strategy

    def parse(self, *args, **kwargs) -> TicketType:
        """Parse ticket"""
        return self.strategy.parse(*args, **kwargs)
