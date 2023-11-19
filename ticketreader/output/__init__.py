"""Output package for ticketreader."""
import logging
from .excel import ExcelHandler

from ticketreader import config
from ticketreader.schemas import Ticket

logger = logging.getLogger(__name__)


def save_ticket(ticket: Ticket, destination: str = 'tickets.xlsx') -> None:
    """Save ticket to Excel file."""
    excel_handler = ExcelHandler(config.DATA_DIR / destination)
    logging.info(f"Saving ticket {ticket.invoice_id}")
    excel_handler.save_ticket(ticket)
    excel_handler.save_workbook()
