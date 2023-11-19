"""Package for Mercadona ticket reader."""
import os
import logging
import pathlib
from typing import List

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


@utils.log_time(logger_name=__name__)
def parse_mercadona_tickets(directory_path: os.PathLike) -> List[MercadonaTicket]:
    """Parse Mercadona tickets"""
    if not os.path.isdir(directory_path):
        raise ValueError(f"File path {directory_path} is not a directory")

    if not os.listdir(directory_path):
        raise ValueError(f"Directory {directory_path} is empty")

    tickets = []
    for file_name in os.listdir(directory_path):
        file_path = pathlib.Path(os.path.join(directory_path, file_name))

        if not file_path.is_file():
            logger.info(f"Skipping directory {file_path}. Not a file")
            continue

        ticket = parse_mercadona_ticket_tabula(file_path=file_path)
        tickets.append(ticket)

    return tickets
