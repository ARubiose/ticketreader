"""Package for Mercadona ticket reader."""
import os
import logging

from .parser import MercadonaFileParser, MercadonaParseContext
from .schemas import MercadonaTicket

from ticketreader import utils

logger = logging.getLogger(__name__)

@utils.log_time(logger=logger)
def parse_mercadona_ticket(file_path:os.PathLike) -> MercadonaTicket:
    """Parse Mercadona ticket"""   

    logger.info(f"Parsing Mercadona ticket {file_path}")
    
    mercadona_parser = MercadonaFileParser()
    ticket_context = MercadonaParseContext(file_path=file_path)

    mercadona_parser.parse(context=ticket_context)
    
    return ticket_context.ticket

@utils.log_time(logger=logger)
def parse_mercadona_tickets(file_paths:list[os.PathLike]) -> list[MercadonaTicket]:
    """Parse Mercadona tickets"""
    tickets = []
    for file_path in file_paths:
        tickets.append(parse_mercadona_ticket(file_path=file_path))
    return tickets
