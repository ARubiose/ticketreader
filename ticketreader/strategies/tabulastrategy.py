"""Module for parsing PDF files using tabula-py."""
import functools
import logging

from typing import Tuple, List, TypeAlias

import pandas as pd
import tabula.io as tabula
from pypdf import PdfReader

from ticketreader.utils import FileHandlerMixin
from ticketreader.parser import ParserStrategy
from ticketreader.utils import log_time

TicketColumns: TypeAlias = Tuple[float, float, float, float]
logger = logging.getLogger(__name__)


class TabulaParserStrategy(ParserStrategy, FileHandlerMixin):
    """Parser strategy based using tabula-py"""

    def __init__(self, columns: List[TicketColumns]) -> None:
        self.columns = columns

    @log_time(logger_name=__name__)
    def get_dataframes(self, **kwargs) -> List[pd.DataFrame]:
        """Get dataframe from PDF file using tabula-py"""
        return [self._get_dataframe(columns=columns, **kwargs) for columns in self.columns]

    def _get_dataframe(self, columns: TicketColumns, **kwargs) -> pd.DataFrame:
        """Get dataframe from PDF file using tabula-py"""
        dataframes = tabula.read_pdf(
            input_path=self.file_path,
            pages='all',
            pandas_options={'header': None},
            multiple_tables=False,
            area=self.get_document_size,
            columns=columns,
            silent=True,
            **kwargs
        )
        if isinstance(dataframes, List):
            return dataframes[0]
        raise ValueError("Dataframe is not a pandas.DataFrame")

    @functools.cached_property
    def get_document_size(self) -> Tuple[float, float, float, float]:
        """Get document size"""
        reader = PdfReader(self.file_path)
        ticket = reader.pages[0]
        box = ticket.mediabox
        return box[1], box[0], box[3], box[2]
