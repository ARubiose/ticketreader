"""Schemas for ticketreader app."""
from enum import Enum, auto
from datetime import datetime
from typing import Optional, List, Annotated, Union
from pydantic.functional_validators import BeforeValidator
from pydantic import BaseModel, Field, computed_field, field_validator

def comma_separated_float(value: str) -> float:
    """Convert comma separated float"""
    value = value.replace(",", ".")
    return float(value)

CommaSeparatedFloat = Annotated[float, BeforeValidator(comma_separated_float)]

class SuperMarketType(Enum):
    """Supermarket type"""
    MERCADONA = auto()

class BaseProduct(BaseModel):
    """Base Product model"""
    name: str = Field(..., title="Product name")
    brand: Optional[str] = Field(None, title="Product brand")

class BulkProduct(BaseProduct):
    """Bulk Product model"""
    price_per_unit: CommaSeparatedFloat = Field(..., title="Price per unit of measure")
    unit_of_measure: str = Field(..., title="Unit of measure (kg, l, etc.)")
    quantity: CommaSeparatedFloat = Field(..., title="Quantity")

    @computed_field
    @property
    def total(self) -> float:
        """Total price"""
        return round(self.price_per_unit * self.quantity, 2) 

class UnitProduct(BaseProduct):
    """Unit Product model"""
    price_per_item: CommaSeparatedFloat = Field(..., title="Price per item")
    quantity: int = Field(..., title="Quantity")

    @computed_field
    @property
    def total(self) -> float:
        """Total price"""
        return self.price_per_item * self.quantity
    
class Address(BaseModel):
    """Address model"""
    street: str = Field(..., title="Street")
    postal_code: int = Field(..., title="Postal code")
    city: str = Field(..., title="City")

class SuperMarket(BaseModel):
    """Supermarket model"""
    id: SuperMarketType = Field(..., title="Supermarket id")
    cif: str = Field(..., title="Supermarket CIF")
    address: Address = Field(..., title="Supermarket address")
    phone: str = Field(..., title="Supermarket phone")

class IVA(BaseModel):
    """IVA model"""
    type: float = Field(..., title="IVA type")
    taxable_base: CommaSeparatedFloat = Field(..., title="IVA taxable base")
    fee: CommaSeparatedFloat = Field(..., title="IVA fee")

    @field_validator('type', mode='before')
    @classmethod
    def cast_type(cls, value:str):
        """Cast type to float"""
        type_amount = value.replace("%", "")
        return round(float(type_amount) / 100, 2)

class Ticket(BaseModel):
    """Ticket model"""
    invoice_id: str = Field(..., title="Invoice id")
    supermarket: SuperMarket = Field(..., title="Supermarket")
    purchase_datetime: datetime = Field(..., title="Purchase time")
    products: List[Union[BulkProduct, UnitProduct]] = Field(..., title="Products", default_factory=list)
    iva: List[IVA] = Field(..., title="IVA")
    total: CommaSeparatedFloat = Field(..., title="Total price")

    @computed_field
    @property
    def total_iva(self) -> float:
        """Total price with IVA"""
        return sum([iva_item.fee for iva_item in self.iva])
