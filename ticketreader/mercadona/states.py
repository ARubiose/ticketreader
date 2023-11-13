"""Mercadona states module"""
import re
import logging
from typing import Tuple, Optional

from ticketreader.strategies import PyPDFParseState

logging = logging.getLogger(__name__)


class CaptureAddress(PyPDFParseState):
    """Capture address state"""

    POSTAL_CODE_PATTERN = r'(\d{5}) (.*)'

    def parse(self, line:str, line_num:int, *args, **kwargs) -> None:
        """Parse file"""
        
        if line_num == 1:
            self.context.tmp['address']['street'] = line
        
        elif line_num == 2:
            postal_code, city = self._capture_pc_nd_city(line)
            self.context.tmp['address']['postal_code'] = postal_code
            self.context.tmp['address']['city'] = city
            self.context.change_state(CapturePhone)

    def _capture_pc_nd_city(self, line:str) -> Tuple[int, str]:
        """Extract postal code and city from line
        Returns: Tuple[int, str] -- postal code and city
        """
        groups = re.search(self.POSTAL_CODE_PATTERN, line)
        if groups:
            return groups.groups()
        raise ValueError("Postal code not found")
    
class CapturePhone(PyPDFParseState):
    """Capture phone state"""

    PHONE_PATTERN = r'(\d{9})'

    def parse(self, line:str, *args, **kwargs) -> None:
        """Parse file"""
        self.context.tmp['phone'] = self._capture_phone(line)
        self.context.change_state(CaptureDatetime)

    def _capture_phone(self, line:str) -> str:
        """Capture phone from line"""
        groups = re.search(self.PHONE_PATTERN, line)
        if groups:
            return groups.group(1)
        raise ValueError("Phone not found")
    
class CaptureDatetime(PyPDFParseState):
    """Capture date state"""

    DATETIME_PATTERN = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2})'

    def parse(self, line:str, *args, **kwargs) -> None:
        """Parse file"""
        self.context.tmp['purchase_datetime'] = self._capture_datetime(line)
        self.context.change_state(CaptureTicketNumber)

    def _capture_datetime(self, line:str) -> str:
        """Capture datetime from line"""
        groups = re.search(self.DATETIME_PATTERN, line)
        if groups:
            return groups.group(1)
        raise ValueError("Datetime not found")
    
class CaptureTicketNumber(PyPDFParseState):

    INVOICE_NUMBER_PATTERN = r'(\d{4}-\d{3}-\d{6})'

    def parse(self, line:str, *args, **kwargs) -> None:
        """Parse file"""
        self.context.tmp['invoice_id'] = self._capture_invoice_number(line)
        self.context.change_state(CaptureProduct)

    def _capture_invoice_number(self, line:str) -> str:
        """Capture invoice number from line"""
        groups = re.search(self.INVOICE_NUMBER_PATTERN, line)
        if groups:
            return groups.group(1)
        raise ValueError("Invoice number not found")
    
class CaptureProduct(PyPDFParseState):
    """Capture product state"""

    UNIT_PRODUCT_PATTERN = r'(\d{1,2})(.*?) (\d{1,2},\d{2})?\s*(\d{1,2},\d{2})'
    BULK_PRODUCT_PATTERN_DESCRIPTION = r'\d(.*)'
    BULK_PRODUCT_PATTERN_AMOUNT = r'(\d{1,2},\d{2,3}) (kg|l) (\d{1,2},\d{2}) €/(?:kg|l) (\d{1,2},\d{2})'

    TOTAL_PATTERN = r'(\d{1,2},\d{2})'

    def parse(self, line:str, *args, **kwargs) -> None:
        """Parse file"""

        if line.startswith("Descripción"):
            self.context.tmp['unit_products'] = []
            self.context.tmp['bulk_products'] = []
        
        elif line.startswith("TOTAL"):
            self.context.tmp['total'] = self._capture_total(line)
            self.context.tmp['iva'] = []
            self.context.change_state(CaptureIVA)

        # Capturing product - order matters
        elif groups := self._is_bulk_product_amount(line):
            self._capture_bulk_product_amount(groups)

        elif groups := self._is_unit_product(line):
            self._capture_unit_product(groups)
        
        elif groups := self._is_bulk_product_description(line):
            self._capture_bulk_product_description(groups)
        


    def _is_unit_product(self, line:str) -> Optional[re.Match]:
        """Check if line is a unit product"""
        return re.search(self.UNIT_PRODUCT_PATTERN, line)
    
    def _is_bulk_product_description(self, line:str) -> Optional[re.Match]:
        """Check if line is a bulk product"""
        return re.search(self.BULK_PRODUCT_PATTERN_DESCRIPTION, line)
    
    def _is_bulk_product_amount(self, line:str) -> Optional[re.Match]:
        """Check if line is a bulk product"""
        return re.search(self.BULK_PRODUCT_PATTERN_AMOUNT, line)
    
    def _capture_unit_product(self, groups:re.Match) -> None:
        """Capture unit product"""
        quantity, name, price_per_item, total_price = groups.groups()
        unit_product = dict(
            name=name,
            quantity=quantity,
            price_per_item=price_per_item or total_price
        )
        self.context.tmp['unit_products'].append(unit_product)

    def _capture_bulk_product_description(self, groups:re.Match) -> None:
        """Capture bulk product"""
        self.context.tmp['bulk_product_description'] = groups.group(1)

    def _capture_bulk_product_amount(self, groups:re.Match) -> None:
        """Capture bulk product"""
        quantity, unit_of_measure, price_per_unit, _ = groups.groups()
        bulk_product = dict(
            name=self.context.tmp['bulk_product_description'],
            quantity=quantity,
            unit_of_measure=unit_of_measure,
            price_per_unit=price_per_unit,
        )
        self.context.tmp['bulk_products'].append(bulk_product)
        
        
    def _capture_total(self, line:str) -> str:
        """Capture total"""
        groups = re.search(self.TOTAL_PATTERN, line)
        if groups:
            return groups.group(1)
        else:
            raise ValueError("Total not found")
        
        
class CaptureIVA(PyPDFParseState):
    """Capture IVA state"""

    IVA_PATTERN = r'(\d{1,2}%) (\d{1,2},\d{2}) (\d{1,2},\d{2})'

    def parse(self, line:str, *args, **kwargs) -> None:
        """Parse file"""

        if line.startswith("TOTAL"):
            self.context.change_state(DoNothing)
        
        elif groups := self._is_iva(line):
            self._capture_iva(groups)


    def _is_iva(self, line:str) -> Optional[re.Match]:
        """Check if line is a IVA"""
        return re.search(self.IVA_PATTERN, line)
    

    def _capture_iva(self, groups:re.Match) -> None:
        """Capture IVA"""
        iva_type, taxable_base, fee = groups.groups()
        iva = dict(
            type=iva_type,
            taxable_base=taxable_base,
            fee=fee
        )
        self.context.tmp['iva'].append(iva)

class DoNothing(PyPDFParseState):
    """Final state. Do nothing"""

    def parse(self, *args, **kwargs) -> None:
        pass
        
