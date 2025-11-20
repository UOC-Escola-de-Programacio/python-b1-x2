from enum import Enum
import datetime
from .entity import *

# Do not change the value of ISD_FACTOR var
ISD_FACTOR = 0.25


class TaxType(Enum):
    # Do not change this enum
    IVA = 1
    ISD = 2


class Tax:
    # Write the parameters in the next line
    def __init__(self, tax_id: str, tax_type: TaxType, percentage: float):
        self.tax_id = tax_id
        self.tax_type = tax_type
        self.percentage = percentage

class Product:
     # Write the parameters in the next line
    def __init__(self, product_id: str, name: str, expiration_date: datetime, bar_code: str, quantity: int, price: float, taxes: list[Tax]):
        self.product_id = product_id
        self.name = name
        self.expiration_date = expiration_date
        self.bar_code = bar_code
        self.quantity = quantity
        self.price = price
        self.taxes = taxes

    def calculate_tax(self, tax: Tax) -> float:
        # Primero veamos cuanto costaria el lote.
        total = self.calculate_total()

        # El impuesto es IVA o ISD?
        if tax.tax_type.value == 1:
            # Es IVA, calculemoslo.
            total = total * tax.percentage
        else:
            # Es ISD, calculemoslo.
            total = total * (tax.percentage * ISD_FACTOR)

        # Enviemos el total del impuesto.
        return total

    def calculate_total_taxes(self) -> float:
        # Primero veamos cuanto costaria el lote.
        total = self.calculate_total()

        # Este producto tiene varios impuestos, calculemoslos y juntemoslos.
        for tax in self.taxes:
            total += self.calculate_tax(tax)

        # Enviemos el total de la factura.
        return total

    def calculate_total(self) -> float:
        # Enviemos el precio total del producto sin impuestos.
        return self.price * self.quantity

    def __eq__(self, another):
        # Do not change this method
        return hasattr(another, 'product_id') and self.product_id == another.product_id

    def __hash__(self):
        # Do not change this method
        return hash(self.product_id)

    def print(self):
        # Do not change this method
        print(
            f"Product Id:{self.product_id} , name:{self.name}, quantity:{self.quantity}, price:{self.price}")
        for tax in self.taxes:
            print(f"Tax:{tax.tax_type} , percentage:{tax.percentage}")


class Bill:
    def __init__(self, bill_id: str, sale_date: datetime, seller: Seller, buyer: Buyer, products: list[Product]):
        self.bill_id = bill_id
        self.sale_date = sale_date
        self.seller = seller
        self.buyer = buyer
        self.products = products
       

    def calculate_total(self) -> float:
        total = 0.0
        
        # Tenemos varios productos en la factura
        for product in self.products:
            # Calculemos el precio con impuestos de cada producto y juntemoslo con el resto.
            total += product.calculate_total_taxes()

        # Enviemos el importe total.
        return total

    def print(self):
        # Do not change this method
        self.buyer.print()
        self.seller.print()
        for product in self.products:
            product.print()