import unicodedata

from conversions.calculations import calculate_dimensions
from conversions.helloprint_sku import translate_sku
from models_esko.esko_models import OrderInfo, Delivery, Contact

from models_helloprint.model_helloprint import OrderLine, Address
from datetime import datetime

datetime_string = "2023-11-15 11:00:00"

# Parse the datetime string
parsed_datetime = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

# Format the datetime to get only the date part
date_string = parsed_datetime.strftime("%Y-%m-%d")

print(date_string)  # Output: 2023-11-15


def price_per_1000(totalprice, quantity):
    if quantity == 0:
        return 0.0
    else:
        return round((totalprice / quantity) * 1000, 2)

def verwijder_speciale_tekens(input_string: str) -> str:
    """
    Removes special characters and diacritic marks from the input string
    by normalizing the unicode characters and replacing certain non-ASCII characters.

    Args:
        input_string (str): The string from which special characters need to be removed.

    Returns:
        str: The string with special characters and diacritic marks removed.
    """
    # Mapping of non-ASCII characters to their closest ASCII equivalents
    char_mapping = {
        'ø': 'o',
        'å': 'a',
        'Ø': 'O',
        'Å': 'A',
        '/': ' ',
        '.': '',
        # Add more mappings as needed
    }

    # Normalize the string and remove diacritic marks
    normalized_string = unicodedata.normalize('NFKD', input_string)
    no_diacritics = "".join([c for c in normalized_string if not unicodedata.combining(c)])

    # Replace non-ASCII characters using the mapping
    result = "".join([char_mapping.get(c, c) for c in no_diacritics])
    return result

def convert_helloprint_address_to_contact(address: Address) -> Contact:
    """Converts an Address object to helloprint_converted_dataclass Contact object.

    Args:
        address (Address): The Address object to convert.

    Returns:
        Contact: The converted Contact object.
    """
    return Contact(
        LastName=verwijder_speciale_tekens(address.lastname),
        FirstName=verwijder_speciale_tekens(address.firstname),
        Initials='',
        Title='Mr./Mevr.',
        PhoneNumber=address.phone,
        FaxNumber='',
        GSMNumber='',
        Email=address.email,
        Function=''
    )


def convert_helloprint_json_into_orderinfo(order_item: OrderLine) -> OrderInfo:
    """
    Converts helloprint_converted_dataclass Helloprint JSON file into an OrderInfo object.

    Args:
        order_item (OrderItem): The OrderItem object to convert.

    Returns:
        OrderInfo: The converted OrderInfo object.
    """
    contacts_in = convert_helloprint_address_to_contact(order_item.address)

    sku_dict = translate_sku(order_item.sku)
    print(f'{sku_dict = }')

    #present width and height for Cerm in relation to winding

    width, height = calculate_dimensions(sku_dict['width'], sku_dict['height'], sku_dict.get('rolwikkeling', 2))

    # collect real width height from artwork
    # get shape en rw from jobsheet

    def get_duedate_str(datetime_string: str) -> str:
        """
        Extracts the date part from a datetime string.

        Args:
            datetime_string (str): A datetime string in the format 'YYYY-MM-DD HH:MM:SS'.

        Returns:
            str: The date part of the datetime string in the format 'YYYY-MM-DD'.
        """
        # Parse the datetime string
        parsed_datetime = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

        # Format the datetime to get only the date part
        date_string = parsed_datetime.strftime("%Y-%m-%d")

        return date_string


    return OrderInfo(

        Description=order_item.sku,
        ReferenceAtCustomer=str(order_item.orderId) + '-' + str(order_item.orderDetailId),
        LineComment1=str(order_item.orderId),
        Shipment_method=order_item.carrierName,
        Delivery=order_item.targetDispatchDate,
        OrderQuantity=order_item.product.quantity,
        Quantity_per_roll='',
        Core='',
        UnitPrice=price_per_1000(float(order_item.purchasePrice),int(order_item.product.quantity)),
        SupplierId='Helloprint',
        Name=order_item.productName,
        Street=verwijder_speciale_tekens(str(order_item.address.address1) + ' ' + str(order_item.address.address2)),
        Country=order_item.address.country,
        PostalCode=order_item.address.postcode,
        City=order_item.address.city,
        Contacts=[contacts_in],
        # Width=sku_dict['width'],
        # Height=sku_dict['height'],
        Width=width,
        Height=height,
        Shape=sku_dict['shape'],
        Radius=float(2),  # @todo radius helloprint
        Winding=sku_dict.get('rolwikkeling', 2), # if keyerror default to 2
        Premium_White=sku_dict.get('Dekwit', 'N'), # if keyerror default to N
        Substrate=sku_dict['materiaal']
    )
