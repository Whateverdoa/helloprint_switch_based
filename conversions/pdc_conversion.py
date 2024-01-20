from dataclasses import asdict
from pathlib import Path
from typing import List, Dict, Any
import logging
import json

from extractions.pdc_extractions import extract_design_info
from models.esko_models import OrderInfo, Delivery, Contact
from models.pdc_models import OrderItem, Shipment, Address

# Initialize logging
logging.basicConfig(level=logging.INFO)


def load_json(filepath: Path) -> Dict[str, Any]:
    """Load helloprint_converted_dataclass JSON file and return its contents
        as helloprint_converted_dataclass Python dictionary.

    Args:
        filepath (Path): The path to the JSON file.

    Returns:
        Dict[str, Any]: The contents of the JSON file as helloprint_converted_dataclass dictionary.
    """
    with filepath.open("r") as f:
        return json.load(f)


def save_json(data: Dict[str, Any], filepath: Path) -> None:
    """Save helloprint_converted_dataclass Python dictionary as helloprint_converted_dataclass JSON file.

    Args:
        data (Dict[str, Any]): The data to save.
        filepath (Path): The path to the JSON file to save.
        
     # Create the directory if it doesn't exist"""
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w") as f:
        json.dump(data, f, indent=4)


def convert_address_to_contact(address: Address) -> Contact:
    """Converts an Address object to helloprint_converted_dataclass Contact object.

    Args:
        address (Address): The Address object to convert.

    Returns:
        Contact: The converted Contact object.
    """
    return Contact(
        LastName=address.lastName,
        FirstName=address.firstName,
        Initials=address.firstName[0],
        Title='Mr./Mevr.',
        PhoneNumber=address.telephone,
        FaxNumber='',
        GSMNumber='',
        Email=address.email,
        Function=''
    )


def convert_shipment_to_delivery(shipment: Shipment) -> Delivery:
    """Converts helloprint_converted_dataclass Shipment object to helloprint_converted_dataclass Delivery object.

    Args:
        shipment (Shipment): The Shipment object to convert.

    Returns:
        Delivery: The converted Delivery object.
    """
    return Delivery(
        Type=shipment.method,
        Comment='',
        AddressId=str(shipment.addressId),
        ExpectedDate=shipment.deliveryDate
    )


def convert_order_item_to_order_info(order_item: OrderItem) -> List[OrderInfo]:
    """Converts an OrderItem object to a list of OrderInfo objects.

    Args:
        order_item (OrderItem): The OrderItem object to convert.

    Returns:
        List[OrderInfo]: A list of converted OrderInfo objects.
    """
    all_order_info = []
    shipments = order_item.shipments
    contacts = order_item.shipments[0]['address']
    from_pdc_in_address = Address(**contacts)
    contact_from_first_shipment = convert_address_to_contact(from_pdc_in_address)

    # Additional logic for recalculations can be added here.

    def check_for_white(colors):
        """Check if the color white exists in the given list of colors.

        Args:
            colors (List[str]): List of color names.

        Returns:
            str: 'Y' if white exists, otherwise 'N'.
        """
        for color in colors:
            if "white" or "White" in color:
                return 'Y'
        return 'N'

    def convert_winding_rolwikkeling(rolwikkeling='outer_0'):

        rolwikkel_dict = {
            'outer_0': 2,
            'outer_270': 3
        }
        return rolwikkel_dict[rolwikkeling]

    def convert_shape_into(shape='custom_shape'):
        if shape[0:8] == 'rectangle':
            return 'Rectangle'
        shape_dict = {
            'custom_shape': 'Irregular',
            'rectangle_sticker__2mm_rounded_corners': 'Rectangle',
            'rectangle_sticker_90_degree_angle': 'Rectangle',
            'circle_label': 'Circle'
        }
        try:
            shape = shape_dict[shape]
        except KeyError:
            shape = 'Irregular'

        return shape

    def radius(shape=None):

        var = {
            'rectangle_sticker__2mm_rounded_corners': 2,
            'rectangle_sticker_90_degree_angle': 0
        }
        try:
            radi = var[shape]

        except KeyError:
            radi = None

        return radi

    order_item_dict = asdict(order_item)

    designs = extract_design_info(
        order_item_dict)  # Assuming that the structure of `order_item` is compatible with `extract_design_info`

    for design in designs:
        copies = design["copies"]

        # Create an OrderInfo object for this design with the appropriate OrderQuantity
        order_info = OrderInfo(
            Description=order_item.descriptions['full'][0:30],
            ReferenceAtCustomer=order_item.orderItemNumber,
            LineComment1=order_item.options['printingmethod'],
            Delivery=f"{shipments[0]['deliveryDate']}",
            OrderQuantity=copies,  # Set the OrderQuantity based on the 'copies' value of the current design
            UnitPrice=order_item.purchasePrice,
            SupplierId='Print.com',
            Name=order_item.name,
            Street=from_pdc_in_address.fullstreet,
            Country=from_pdc_in_address.country,
            PostalCode=from_pdc_in_address.postcode,
            City=from_pdc_in_address.city,
            Contacts=[contact_from_first_shipment],
            Width=order_item.options['width'],
            Height=order_item.options['height'],
            Shape=convert_shape_into(order_item.options['shape']),
            Radius=radius(order_item.options['shape']),
            Winding=convert_winding_rolwikkeling(order_item.options['output_direction']),
            Premium_White=check_for_white(order_item.pantoneColors),
            Substrate=order_item.options['material']
        )
        all_order_info.append(order_info)

    return all_order_info


def process_order_info_list(order_info_list: List[OrderInfo]):
    """Processes a list of OrderInfo objects.

    Args:
        order_info_list (List[OrderInfo]): The list of OrderInfo objects to process.

    Returns:
        None: The function performs its operations in-place or outputs to some external system.
    """
    for i, order_info in enumerate(order_info_list, 1):
        # Your processing logic here. For example:
        print(f"Processing order with ReferenceAtCustomer: {order_info.ReferenceAtCustomer}_{i}")
        print(f"  - OrderQuantity: {order_info.OrderQuantity}")
        pad = Path(f'Data_Eager/{order_info.ReferenceAtCustomer}_{i}/{order_info.ReferenceAtCustomer}_{i}.json')
        print(pad)
        save_json(asdict(order_info), Path(pad))

        # Maybe save to a database, send to an API, generate a report, etc.
