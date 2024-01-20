import json
import os
from dataclasses import asdict
import time
from pathlib import Path
import requests
import shutil

from Paden.paden import DOWNLOAD_PAD_VILA_TO_ESKO, HP_CERM_CONN, hp_cerm_conv_pad
from conversions.calculations import process_pdf_files
from conversions.helloprint_conversion import convert_helloprint_address_to_contact, \
    convert_helloprint_json_into_orderinfo
from conversions.pdc_conversion import save_json
from conversions.helloprint_sku import translate_sku
from models_helloprint.model_helloprint import (Root,
                                                Address,
                                                Product,
                                                FilesToDownload,
                                                OrderLine,
                                                Order)

# json_file_path = Path(r'testfile/4203201-6243251_Helloprint_JSON_2023-11-15.json')


def read_order_from_file(file_path: Path) -> Root:
    """
    Reads helloprint_converted_dataclass JSON file and returns helloprint_converted_dataclass populated Root object.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Root: A populated Root object.
    """
    """
     Reads helloprint_converted_dataclass JSON file and returns helloprint_converted_dataclass populated Root object.

     Args:
         file_path (str): The path to the JSON file.

     Returns:
         Root: A populated Root object.
     """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    with open(file_path, 'r') as f:
        # Read the file content
        file_content = f.read().strip()

        # Check if the file is empty
        if not file_content:
            print("File is empty")
            return None

        # Parse the JSON data
        try:
            json_data = json.loads(file_content)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            return None

    with open(file_path, 'r') as f:
        json_data = json.load(f)

    # Manually creating the Root object from the dictionary
    orders = []
    for order_dict in json_data.get('orders', []):
        order_lines = []
        for line_dict in order_dict.get('orderLines', []):
            address = Address(**line_dict['address']['to'])
            product = Product(**line_dict.get('product', {}))
            files_to_download = FilesToDownload(
                **{k: line_dict.get(k, None) for k in ['packingSlipUrl', 'shippingLabelUrl', 'filename']}
            )

            # Create helloprint_converted_dataclass new dictionary excluding keys that are explicitly set
            line_dict_copy = {k: v for k, v in line_dict.items() if
                              k not in ['address', 'product', 'packingSlipUrl', 'shippingLabelUrl', 'filename']}

            order_line = OrderLine(address=address, product=product, files_to_download=files_to_download,
                                   **line_dict_copy)
            order_lines.append(order_line)

        order = Order(orderId=order_dict.get('orderId', None), orderLines=order_lines)
        orders.append(order)

    root = Root(orders=orders)

    return root


def zip_folder(src_folder: Path, dest_zip: Path):
    """
    Zips a folder.

    Args:
        src_folder (Path): The path to the source folder you want to zip.
        dest_zip (Path): The path to the destination zip file.

    Returns:
        Path: The path to the created zip file.
    """
    shutil.make_archive(dest_zip, 'zip', src_folder)
    print(f"Folder zipped at {dest_zip}")
    return dest_zip.with_suffix('.zip')


def download_file_from_url(url: str, destination_path: Path):
    """
    Download a file from a URL and save it to a destination path.

    Args:
        url (str): The URL of the file to download.
        destination_path (Path): The Path object where the file will be saved.

    Returns:
        None
    """
    response = requests.get(url)
    if response.status_code == 200:
        with destination_path.open("wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download the file. HTTP Status Code: {response.status_code}")


if __name__ == "__main__":


    json_dir = HP_CERM_CONN

    while True:  # Start of the infinite loop

        json_files = sorted(json_dir.glob('*.json'))
        print(json_files)
        sku_s = []
        for json_file in json_files:
            if json_file.exists():
                print(json_file.name)
                root_object = read_order_from_file(json_file)
                if root_object is not None:
                    print(root_object)

                    root_orderline = root_object.orders[0].orderLines[0]

                    print("-------")

                    json_file = f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}/{root_orderline.orderId}_{root_orderline.orderDetailId}.json'
                    # print(root_orderline.address)
                    print('________')
                    contacts = convert_helloprint_address_to_contact(root_orderline.address)
                    # print(root_orderline.sku)
                    sku_s.append((root_orderline.sku, translate_sku(root_orderline.sku)))
                    # print(translate_sku(root_orderline.sku))
                    helloprint_converted_dataclass = convert_helloprint_json_into_orderinfo(root_orderline)
                    print(helloprint_converted_dataclass)

                    save_json(asdict(helloprint_converted_dataclass),
                              Path(json_file))

                    print(root_object.orders[0].orderLines[0].files_to_download.filename)
                    url_art_pdf = root_object.orders[0].orderLines[0].files_to_download.filename
                    art_pdf = f'Artwork_{root_orderline.orderId}_{root_orderline.orderDetailId}.pdf'
                    print(art_pdf)

                    pdf_dest = f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}/{art_pdf}'
                    print(pdf_dest)

                    print(root_object.orders[0].orderLines[0].files_to_download.packingSlipUrl)
                    url_jobsheet_pdf = root_object.orders[0].orderLines[0].files_to_download.packingSlipUrl
                    jobsheet_pdf = f'Jobsheet_{root_orderline.orderId}_{root_orderline.orderDetailId}.pdf'
                    print(jobsheet_pdf)

                    jobsheet_dest = f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}/{jobsheet_pdf}'
                    print(jobsheet_dest)

                    # pdf_data = process_pdf_files(Path(jobsheet_dest),Path(pdf_dest))
                    # collect shape rolwikkeling from jobsheet
                    # collect width and height from artwork
                    # if data != in cermjson dan ....


                    download_file_from_url(url_art_pdf, Path(pdf_dest))
                    download_file_from_url(url_jobsheet_pdf, Path(jobsheet_dest))

                    padzip_src = Path(f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}')
                    padzip_dest = Path(f'{DOWNLOAD_PAD_VILA_TO_ESKO}/{root_orderline.orderId}_{root_orderline.orderDetailId}')

                    zip_folder(padzip_src, padzip_dest)




                else:
                    print(f"The file {json_file} does not exist.")

        tobe_deleted_json_files = sorted(json_dir.glob('*.json'))
        for used_file in tobe_deleted_json_files:
            Path(used_file).unlink()
            print(f"File {used_file} deleted successfully.")

        time.sleep(300) # wait 5 minutes before checking again
