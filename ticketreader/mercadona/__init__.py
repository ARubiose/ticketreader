"""Package for Mercadona ticket reader."""
import os
import logging

from ticketreader import utils
from ticketreader.parser import FileParser

from .schemas import MercadonaTicket
from .tabula import MercadonaTabulaStrategy

logger = logging.getLogger(__name__)


@utils.log_time(logger_name=__name__)
def parse_mercadona_ticket_tabula(file_path: os.PathLike) -> MercadonaTicket:
    """Parse Mercadona tickets"""
    logger.info(f"Parsing Mercadona ticket {file_path}")

    # Stablish strategy and file path
    strategy = MercadonaTabulaStrategy()
    strategy.file_path = file_path

    parser = FileParser(parse_strategy=strategy)

    return parser.parse()
