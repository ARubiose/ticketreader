"""Package for Mercadona ticket reader."""
import os
from .parser import MercadonaFileParser, MercadonaParseContext
from .schemas import MercadonaTicket

def parse_mercadona_ticket(file_path:os.PathLike) -> MercadonaTicket:
    """Parse Mercadona ticket"""
    mercadona_parser = MercadonaFileParser()
    ticket_context = MercadonaParseContext(file_path=file_path)
    mercadona_parser.parse(context=ticket_context)
    return ticket_context.ticket

def parse_mercadona_tickets(file_paths:list[os.PathLike]) -> list[MercadonaTicket]:
    """Parse Mercadona tickets"""
    tickets = []
    for file_path in file_paths:
        tickets.append(parse_mercadona_ticket(file_path=file_path))
    return tickets
