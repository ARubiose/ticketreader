"""Mercadona schemas."""
from datetime import datetime
from pydantic import Field, field_validator
from ticketreader.schemas import SuperMarket, SuperMarketType, Ticket

class Mercadona(SuperMarket):
    """Mercadona model"""
    id: SuperMarketType = Field(SuperMarketType.MERCADONA, title="Supermarket id")
    cif: str = Field("A-46103834", title="Supermarket CIF")

class MercadonaTicket(Ticket):
    """Mercadona ticket model"""
    supermarket: Mercadona = Field(..., title="Supermarket")

    @field_validator('purchase_datetime', mode='before')
    def cast_purchase_datetime(cls, value: str) -> datetime:
        """Cast purchase datetime"""
        return datetime.strptime(value, "%d/%m/%Y %H:%M")