"""Main script for ticketreader"""
import os
import pathlib
from ticketreader import config

from ticketreader import mercadona
from ticketreader import output


def parse_one_mercadona_ticket(ticket_path: pathlib.Path, destination: pathlib.Path) -> None:
    """Parse one ticket"""
    ticket = mercadona.parse_mercadona_ticket_tabula(file_path=ticket_path)
    excel_handler = output.ExcelHandler(file_name=destination)
    excel_handler.save_ticket(ticket)
    excel_handler.save_workbook()


def parse_mercadona_directory(ticket_directory: pathlib.Path, destination: pathlib.Path) -> None:
    """Parse directory"""
    tickets = mercadona.parse_mercadona_tickets(
        directory_path=ticket_directory)
    for ticket in tickets:
        excel_handler = output.ExcelHandler(file_name=destination)
        excel_handler.save_ticket(ticket)
        excel_handler.save_workbook()
