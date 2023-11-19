"""Strategies for reading tickets."""

# State strategy. PyPDF context
from .statestrategy import StateParserStrategy, PyPDFParseContext

# Using Tabula - https://pypi.org/project/tabula-py/
from .tabulastrategy import TabulaParserStrategy
