from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Description:
    """Class for storing descriptions."""
    full: Optional[str] = field(default=None)
    size: Optional[str] = field(default=None)
    printing: Optional[str] = field(default=None)
    material: Optional[str] = field(default=None)
    designs: Optional[str] = field(default=None)
    finishing: Optional[str] = field(default=None)
    shipping: Optional[str] = field(default=None)


@dataclass
class Address:
    """Class for storing address information."""
    firstName: Optional[str] = field(default=None)
    lastName: Optional[str] = field(default=None)
    companyName: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    telephone: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)
    fullstreet: Optional[str] = field(default=None)
    city: Optional[str] = field(default=None)
    country: Optional[str] = field(default=None)
    postcode: Optional[str] = field(default=None)
    street: Optional[str] = field(default=None)
    houseNumber: Optional[str] = field(default=None)


@dataclass
class Shipment:
    """Class for storing shipment information."""
    shipmentId: Optional[str] = field(default=None)
    addressId: Optional[str] = field(default=None)
    copies: Optional[str] = field(default=None)
    deliveryDate: Optional[str] = field(default=None)
    latestDeliveryDate: Optional[str] = field(default=None)
    method: Optional[str] = field(default=None)
    productDiscount: Optional[str] = field(default=None)
    shippingDiscount: Optional[str] = field(default=None)
    normalPrice: Optional[str] = field(default=None)
    address: Optional[Address] = field(default=None)
    tax: Optional[str] = field(default=None)
    combinedShipmentDiscount: Optional[str] = field(default=None)
    printCustomLabel: Optional[str] = field(default=None)
    shippingLabelUrl: Optional[Any] = field(default=None)
    orderItemsWithSameShippingAddress: Optional[Any] = field(default=None)
    designs: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class Design:
    """Class for storing design information."""
    id: Optional[str] = field(default=None)
    copies: Optional[str] = field(default=None)
    href: Optional[str] = field(default=None)
    shipments: Optional[Dict[str, Shipment]] = field(default_factory=dict)


@dataclass
class Options:
    """Class for storing options."""
    copies: Optional[str] = field(default=None)
    urgency: Optional[str] = field(default=None)
    numberOfSheets: Optional[str] = field(default=None)
    sheetWidth: Optional[str] = field(default=None)
    planoHeight: Optional[str] = field(default=None)
    squareMM: Optional[str] = field(default=None)
    output_direction: Optional[str] = field(default=None)
    printtype: Optional[str] = field(default=None)
    roll_diameter: Optional[str] = field(default=None)
    finish: Optional[str] = field(default=None)
    total_length: Optional[str] = field(default=None)
    number_of_rolls: Optional[str] = field(default=None)
    height: Optional[str] = field(default=None)
    roll_length: Optional[str] = field(default=None)
    shape: Optional[str] = field(default=None)
    planoWidth: Optional[str] = field(default=None)
    copies_per_roll: Optional[str] = field(default=None)
    squareMMTotal: Optional[str] = field(default=None)
    printingmethod: Optional[str] = field(default=None)
    handling_costs: Optional[str] = field(default=None)
    size: Optional[str] = field(default=None)
    material: Optional[str] = field(default=None)
    type_glue: Optional[str] = field(default=None)
    width: Optional[str] = field(default=None)
    sheetHeight: Optional[str] = field(default=None)
    bleed: Optional[str] = field(default=None)
    numberOfDesigns: Optional[str] = field(default=None)


@dataclass
class Links:
    """Class for storing links."""
    self: Optional[Dict[str, str]] = field(default_factory=dict)
    jobsheet: Optional[Dict[str, str]] = field(default_factory=dict)
    productionFile: Optional[Dict[str, str]] = field(default_factory=dict)
    design_1: Optional[Dict[str, str]] = field(default_factory=dict)


@dataclass
class OrderItem:
    """Class for storing order item information."""
    created: Optional[str] = field(default=None)
    deliveryPromise: Optional[str] = field(default=None)
    deliveryPromiseCost: Optional[str] = field(default=None)
    descriptions: Optional[Description] = field(default=None)
    designs: Optional[Dict[str, Design]] = field(default_factory=dict)
    designsHasSameAmount: Optional[str] = field(default=None)
    layouts: Optional[Any] = field(default=None)
    name: Optional[str] = field(default=None)
    options: Optional[Options] = field(default=None)
    orderId: Optional[str] = field(default=None)
    orderItemId: Optional[str] = field(default=None)
    orderItemNumber: Optional[str] = field(default=None)
    orderNumber: Optional[str] = field(default=None)
    pantoneColors: Optional[Any] = field(default=None)
    pickupDate: Optional[str] = field(default=None)
    printjobId: Optional[str] = field(default=None)
    purchasePrice: Optional[str] = field(default=None)
    quantity: Optional[str] = field(default=None)
    reprintCreditDeliveryPromise: Optional[str] = field(default=None)
    reprintCreditUrgency: Optional[str] = field(default=None)
    reprintOrderItemNumber: Optional[Any] = field(default=None)
    shipments: Optional[Dict[str, Shipment]] = field(default_factory=dict)
    sku: Optional[str] = field(default=None)
    status: Optional[str] = field(default=None)
    submissionDate: Optional[str] = field(default=None)
    supplierChecklist: Optional[Any] = field(default=None)
    supplierCode: Optional[str] = field(default=None)
    urgencyCost: Optional[str] = field(default=None)
    variants: Optional[Any] = field(default=None)
    childItems: Optional[Any] = field(default=None)
    _links: Optional[Links] = field(default=None)
    preferredLanguage: Optional[str] = field(default=None)
    note: Optional[str] = field(default=None)
