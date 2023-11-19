"""Mercadona schemas."""
from enum import StrEnum
from datetime import datetime
from pydantic import Field, field_validator
from ticketreader.schemas import SuperMarket, SuperMarketType, Ticket


class Mercadona(SuperMarket):
    """Mercadona model"""
    id: SuperMarketType = Field(
        title="Supermarket id", default=SuperMarketType.MERCADONA)
    cif: str = Field(title="Supermarket CIF", default="A-46103834")


class MercadonaTicket(Ticket):
    """Mercadona ticket model"""
    supermarket: Mercadona = Field(..., title="Supermarket")

    @field_validator('purchase_datetime', mode='before')
    def cast_purchase_datetime(cls, value: str) -> datetime:
        """Cast purchase datetime"""
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y %H:%M")
        elif isinstance(value, datetime):
            return value
        raise TypeError("Wrong type for purchase datetime")


class PatternsEnum(StrEnum):
    """Mercadona ticket patterns"""
    ADDRESS = r'(\d{5})\s(.*)'
    PHONE = r'(\d{9})'
    PURCHASE_DATETIME = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2})'
    INVOICE_NUMBER = r'(\d{4}-\d{3}-\d{6})'
