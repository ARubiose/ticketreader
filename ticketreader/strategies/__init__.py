"""Strategies for reading tickets."""
from .statestrategy import StateParserStrategy

# Using PyPDF - https://pypi.org/project/pypdf/
from .pypdfstrategy import PyPDFParseContext, PyPDFParseState

# Using Tabula - https://pypi.org/project/tabula-py/
from .tabulastrategy import TabulaParserStrategy
