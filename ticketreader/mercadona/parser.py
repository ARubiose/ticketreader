"""File parser for Mercadona tickets"""
import os
from typing import List

# Base classes
from ticketreader.parser import FileParser
from ticketreader.strategies import PyPDFParseContext, StateParserStrategy

# Data models
from ticketreader.mercadona.schemas import MercadonaTicket, Mercadona
from ticketreader.schemas import Address, UnitProduct, BulkProduct, IVA

# Initial state
from ticketreader.mercadona.states import CaptureAddress

class MercadonaParseContext(PyPDFParseContext):
    """Mercadona parse context"""

    INITIAL_STATE = CaptureAddress
    VALID_EXTENSIONS = ['.pdf', '.PDF']

    @property
    def ticket(self) -> MercadonaTicket:
        """Ticket"""
        return self._create_ticket()
    
    def _create_ticket(self) -> MercadonaTicket:
        """Create ticket"""
        return MercadonaTicket(
            invoice_id=self.tmp['invoice_id'],
            supermarket=self._create_supermarket(),
            purchase_datetime=self.tmp['purchase_datetime'],
            products=self._create_unit_products() + self._create_bulk_products(),
            iva=self.tmp['iva'],
            total=self.tmp['total'],
        )

    def _create_supermarket(self) -> Mercadona:
        """Create supermarket"""
        return Mercadona(
            address=self._create_address(),
            phone=self.tmp['phone'],
        )
    
    def _create_address(self) -> Address:
        """Create address"""
        return Address(
            street=self.tmp['address']['street'],
            postal_code=self.tmp['address']['postal_code'],
            city=self.tmp['address']['city']
        )
    
    def _create_unit_products(self) -> List[UnitProduct]:
        """Create unit products"""
        return [
            UnitProduct(
                name=product['name'],
                quantity=product['quantity'],
                price_per_item=product['price_per_item']
            )
            for product in self.tmp['unit_products']
        ]
    
    def _create_bulk_products(self) -> List[BulkProduct]:
        """Create bulk products"""
        return [
            BulkProduct(
                name=product['name'],
                quantity=product['quantity'],
                unit_of_measure=product['unit_of_measure'],
                price_per_unit=product['price_per_unit']
            )
            for product in self.tmp['bulk_products']
        ]
    
    def _create_iva(self) -> List[IVA]:
        """Create IVA"""
        return [
            IVA(
                type=iva['type'],
                taxable_base=iva['taxable_base'],
                fee=iva['fee']
            )
            for iva in self.tmp['iva']
        ]

class MercadonaFileParser(FileParser):
    """Mercadona file parser"""

    def __init__(self) -> None:
        strategy = StateParserStrategy()
        super().__init__(parse_strategy=strategy)
    