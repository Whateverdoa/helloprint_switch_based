from dataclasses import dataclass, field, asdict
from typing import Dict


@dataclass
class RemappedOrder:
    Customer_ID: str
    Shape: str
    Width: str
    Height: str
    Winding: str
    Premium_White: str = "N"
    Substrate: Dict[str, str] = field(default_factory=lambda: {"material": "N/A", "thickness": "0.2"})
    Laser_or_Digicon: str = "Laser"
    designs: str = '0'


# Define an Address dataclass to hold the address fields from the provided XML snippet
@dataclass
class DetailedAddress:
    firstName: str
    lastName: str
    companyName: str
    email: str
    telephone: str
    id: str
    fullstreet: str
    city: str
    country: str
    postcode: str
    street: str
    houseNumber: str
