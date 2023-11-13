"""Strategies for reading tickets."""
from .statestrategy import StateParserStrategy

# Using PyPDF - https://pypi.org/project/pypdf/
from .statestrategy import PyPDFParseContext, PyPDFParseState