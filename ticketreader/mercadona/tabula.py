"""Tabula PDF reader for Mercadona tickets"""
import re
import math
import logging
from typing import List
from datetime import datetime

from pandas import Series

from ticketreader.schemas import Address, UnitProduct, BulkProduct, IVA
from ticketreader.strategies import TabulaParserStrategy
from ticketreader.mercadona.schemas import Mercadona, PatternsEnum, MercadonaTicket

logger = logging.getLogger(__name__)


class MercadonaTabulaStrategy(TabulaParserStrategy):

    VALID_EXTENSIONS = [".pdf", ".PDF"]

    def __init__(self):
        columns = [
            [612],
            [64, 345, 508, 612],
            [205.5, 405.5, 612],
        ]
        super().__init__(columns=columns)

        self.tmp = dict()
        """Temporary data"""

    def parse(self, *args, **kwargs) -> MercadonaTicket:

        self.dataframes = self.get_dataframes()
        try:
            return MercadonaTicket(
                supermarket=self._capture_supermarket_info(),
                invoice_id=self._capture_invoice_id(),
                purchase_datetime=self._capture_purchase_datetime(),
                products=self._capture_unit_products() + self._capture_bluk_products(),
                iva=self._capture_iva(),
                total=self._capture_total(),  # type: ignore
            )
        except Exception as e:
            logger.error(f"Error parsing ticket.", exc_info=True)
            raise e

    def _capture_supermarket_info(self) -> Mercadona:
        """Capture supermarket info"""
        return Mercadona(
            address=self._capture_address(),
            phone=self._capture_phone(),
        )

    def _capture_address(self) -> Address:
        """Capture address."""
        fragment = self.dataframes[0].iloc[2, 0]
        street = self.dataframes[0].iloc[1, 0]

        if isinstance(fragment, str) and isinstance(street, str):
            matches = re.search(PatternsEnum.ADDRESS, fragment)
            if matches:
                return Address(
                    street=street,
                    postal_code=int(matches.groups()[0]),
                    city=matches.groups()[1],
                )
            raise ValueError("Address does not match pattern")
        raise TypeError("Wrong type for address")

    def _capture_supermarket_info_item(self, fragment: str, pattern: str) -> str:
        """Capture supermarket info item"""
        if isinstance(fragment, str):
            match = re.search(pattern, fragment)
            if match:
                return match.groups()[0]
            raise ValueError("Fragment does not match pattern")
        raise TypeError("Wrong type for fragment")

    def _capture_phone(self) -> str:
        """Capture phone"""
        return self._capture_supermarket_info_item(
            fragment=str(self.dataframes[0].iloc[3, 0]),
            pattern=PatternsEnum.PHONE
        )

    def _capture_purchase_datetime(self) -> datetime:
        """Capture purchase datetime"""
        purchase_datetime = self._capture_supermarket_info_item(
            fragment=str(self.dataframes[0].iloc[4, 0]),
            pattern=PatternsEnum.PURCHASE_DATETIME
        )
        return datetime.strptime(purchase_datetime, "%d/%m/%Y %H:%M")

    def _capture_invoice_id(self) -> str:
        """Capture invoice id"""
        return self._capture_supermarket_info_item(
            fragment=str(self.dataframes[0].iloc[5, 0]),
            pattern=PatternsEnum.INVOICE_NUMBER
        )

    def _capture_unit_products(self) -> List[UnitProduct]:
        """Capture unit products"""
        unit_products = []
        for index, row in self.dataframes[1][7:].iterrows():

            if isinstance(row[3], float) and math.isnan(row[3]):
                self.tmp['bulk_products_start_index'] = index
                break

            product = self._capture_uproduct(row)
            unit_products.append(product)

        logger.info(f'Captured {len(unit_products)} unit products')
        return unit_products

    def _capture_uproduct(self, row: Series) -> UnitProduct:
        """Capture unit product"""
        return UnitProduct(
            quantity=row[0],
            name=row[1],
            price_per_item=row[3] if isinstance(row[2], float) else row[2],
        )

    def _capture_bluk_products(self) -> List[BulkProduct]:
        """Capture bulk products"""

        bulk_products = []
        for index, row in self.dataframes[1][self.tmp['bulk_products_start_index']:].iterrows():

            if isinstance(row[2], str) and row[2] == 'TOTAL (€)':
                self.tmp['total_row_index'] = index
                break

            if isinstance(row[2], float) and math.isnan(row[2]):
                self._capture_bprouct_description(row)
            else:
                product = self._capture_bproduct_details(row)
                bulk_products.append(product)

        logger.info(f'Captured {len(bulk_products)} bulk products')
        return bulk_products

    def _capture_bprouct_description(self, row: Series) -> None:
        """Capture bulk product description"""
        self.tmp['tmp_bulk_product_name'] = row[1]

    def _capture_bproduct_details(self, row: Series) -> BulkProduct:
        """Capture bulk product details"""
        quantity, unit = row[1].split(" ")
        return BulkProduct(
            name=self.tmp['tmp_bulk_product_name'],
            quantity=quantity,
            unit_of_measure=unit,
            price_per_unit=row[2].split(" ")[0],
        )

    def _capture_total(self) -> str:
        """Capture total"""
        total = self.dataframes[1].iloc[self.tmp['total_row_index'], 3]
        if isinstance(total, str):
            return total
        raise TypeError("Wrong type for total")

    def _capture_iva(self) -> List[IVA]:
        """Capture IVA"""
        iva_start_row_index = self.tmp['total_row_index'] + 3
        iva_items = []

        for _, row in self.dataframes[2][iva_start_row_index:].iterrows():
            iva_type_item = self._capture_iva_item(row)
            iva_items.append(iva_type_item)

            if row[0] == 'TOTAL':
                break

        logger.info(f'Captured {len(iva_items)} IVA items')
        return iva_items

    def _capture_iva_item(self, row: Series) -> IVA:
        """Capture IVA item"""
        return IVA(
            type=row[0],
            taxable_base=row[1],
            fee=row[2]
        )
