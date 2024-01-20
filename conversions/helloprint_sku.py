#!/usr/bin/env python3
from typing import Dict


# Dictionary to map material codes to their descriptions
# MATERIAL_TRANSLATIONS = {
#     '65NFC': '65NFC',   #'4351 natureflex transparant, permanent',
#     '75PWW': '75PWW',   #'4581 paperwise suikerriet white, permanent',
#     '75PWN': '75PWN',   #'4581 paperwise suikerriet natural, permanent',
#     '65NFW': '4781 natureflex white, permanent',
#     'SC': '4601 paperwise suikerriet natural, permanent',
#     'FLUORMA': '4621 fluor magenta, permanent',
#     'FLUORYE': '4721 fluor geel, permanent',
#     'FLUORGR': '4731 fluor groen, permanent',
#     'FLUOROR': '4741 fluor oranje, permanent',
#     'FLUORRE': '4751 fluor rood, permanent',
#     '90KR': '4771 kraft bruin, permanent',
#     '73ST': '4801 mat wit, permanent',
#     '80GG': '4811 glans wit, permanent',
#     '90PVC': '4871 pp wit, permanent',
#     '90TPVC': '4891 pp transparant, permanent',
#     '90SLVR': '4911 glans zilver, permanent',
# }
# i need to get the  trimbox values of the artwork and the shape from the jobsheet

def extract_dimensions(dim: str, prefix: str) -> Dict[str, str]:
    """
    Extract dimensions based on helloprint_converted_dataclass prefix like 'RE' or 'OV'.

    Args:
        dim (str): The dimension string, e.g., "RE10100" or "OV4060".
        !!!!!whatif 10060 10 060 is not possible but 10260 is possible both ways 10 260 and 102 60
        prefix (str): The prefix to look for, e.g., "RE" or "OV".

    Returns:
        Dict[str, str]: A dictionary containing the extracted width and height.
    """
    dims = dim.replace(prefix, '')
    length = len(dims)
    dimensions = {}

    if length == 4:
        dimensions['width'] = dims[:2]
        dimensions['height'] = dims[2:]

    elif length == 5:
        dimensions['width'] = dims[:2]
        dimensions['height'] = dims[2:]
    elif length == 6:
        dimensions['width'] = dims[:3]
        dimensions['height'] = dims[3:]
    else:
        # Handle this as an exception or set them as None or some default value
        dimensions['width'] = None
        dimensions['height'] = None
        dimensions['shape'] = 'Irregular'

    return dimensions


def translate_sku(sku: str) -> Dict[str, str]:
    """
    Translates an SKU string into its constituent parts.

    Args:
        sku (str): The SKU string, e.g., "ET-73ST-60x40-2500-40-6[ROLW2]"

    Returns:
        Dict[str, str]: A dictionary containing the translated parts of the SKU.
    """

    if sku == 'OFF':
        # Handle the 'OFF' case
        translation = {
        'product_type': "quote",
        'materiaal': '',
        'dimensions': '',
        'quantity': '',
        'kern': ''
                }
        return translation

    # Split the SKU based on the "-" delimiter
    parts = sku.split('-')


    # Translate each part (modify this based on your business logic)
    translation = {
        'product_type': parts[0] if len(parts) > 0 else None,
        'materiaal': parts[1] if len(parts) > 1 else None,
        'dimensions': parts[2] if len(parts) > 2 else None,
        'quantity': parts[3] if len(parts) > 3 else None,
        'kern': parts[4] if len(parts) > 4 else None,

    }

    # # Translate the material code to its description
    # if 'materiaal' in translation and translation['materiaal']:
    #     translation['materiaal_description'] = MATERIAL_TRANSLATIONS.get(translation['materiaal'], 'Unknown')

    # Determine the shape and dimensions based on the 'dimensions' field
    if 'dimensions' in translation and translation['dimensions']:
        dim = translation['dimensions']

        if 'VK' in dim:
            translation['shape'] = 'Rectangle'
            translation['width'] = translation['height'] = dim.replace('VK', '')
        elif 'RO' in dim:
            translation['shape'] = 'Circle'
            translation['width'] = translation['height'] = dim.replace('RO', '')
        elif 'RE' in dim:
            translation['shape'] = 'Rectangle'
            dimensions = extract_dimensions(dim, 'RE')
            translation.update(dimensions)
        elif 'OV' in dim:
            translation['shape'] = 'Oval'
            dimensions = extract_dimensions(dim, 'OV')
            translation.update(dimensions)
        elif "m" in dim:
            translation['shape'] = 'Irregular'
            translation['width'] = translation['height'] = 0.0

    if 'dimensions' in translation and 'x' in translation['dimensions']:
        width, height = translation['dimensions'].split('x')
        translation['width'] = width
        translation['height'] = height
        translation['shape'] = 'Rectangle'

    # Split the last part based on the "[" delimiter for additional information
    if len(parts) > 5:
        additional_info = parts[5].split('[')
        translation['other_info'] = additional_info[0]
        if len(additional_info) > 1:
            extra_info = additional_info[1].rstrip(']')
            translation['additional_info'] = extra_info

            translation['rolwikkeling'] = 2
            translation['Dekwit'] = 'N'

            # Split extra_info by the "+" symbol and process each part
            for info_part in extra_info.split('+'):
                if 'ROLW' in info_part:
                    translation['rolwikkeling'] = int(info_part.replace('ROLW', ''))
                if 'CO' in info_part:
                    translation['shape'] = 'Irregular'
                if '200W' in info_part:
                    translation['Dekwit'] = 'Y'
                if '100FC100W' in info_part:
                    translation['Dekwit'] = 'Y'



    return translation


# Test the function
sku = "ET-73ST-60x40-2500-40-6[ROLW3+100FC100W]"
translated_sku = translate_sku(sku)
print(translated_sku)
