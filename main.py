import json
import os
from dataclasses import asdict
import time
from pathlib import Path
import requests
import shutil
import logging

from Paden.paden import HP_CERM_CONN, hp_cerm_conv_pad, DOWNLOAD_PAD_VILA_TO_ESKO
from conversions.helloprint_conversion import convert_helloprint_address_to_contact, \
    convert_helloprint_json_into_orderinfo
from conversions.helloprint_sku import translate_sku
from conversions.pdc_conversion import save_json
from models_helloprint.main_testing_hp_json import read_order_from_file, download_file_from_url, zip_folder


logpad= Path(r'C:\Users\Bgsystem\PycharmProjects_send_SWITCH_helloprint_cerm\pythonProject\logs\helloprint.log')
# Setup logging
logging.basicConfig(level=logging.INFO,filename=logpad, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('helloprint log')
# [Your function definitions here]

def contains_sku_off(order):
    for order_line in order.orderLines:
        if order_line.sku == 'OFF':
            return True
    return False

if __name__ == "__main__":
    json_dir = HP_CERM_CONN

    while True:
        json_files = sorted(json_dir.glob('*.json'))
        logging.info(f"Found JSON files: {json_files}")

        for original_json_file in json_files:
            try:
                logging.info(f"Starting processing file: {original_json_file.name}")
                root_object = read_order_from_file(original_json_file)
                if root_object is None:
                    logging.warning(f"No data in file {original_json_file}, skipping.")
                    continue

                # Check if any order contains 'SKU OFF' and delete such files
                if any(contains_sku_off(order) for order in root_object.orders):
                    logging.warning(f"File {original_json_file} contains 'SKU OFF', deleting.")
                    original_json_file.unlink()
                    continue

                sku_s = []
                root_object = read_order_from_file(original_json_file)
                if root_object is not None:
                    print("-------root object-------")
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
                    logging.info(f"Helloprint Artwork PDF: {art_pdf}")

                    pdf_dest = f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}/{art_pdf}'
                    print(pdf_dest)
                    logging.info(f"Helloprint Artwork PDF destination: {pdf_dest}")

                    print(root_object.orders[0].orderLines[0].files_to_download.packingSlipUrl)
                    url_jobsheet_pdf = root_object.orders[0].orderLines[0].files_to_download.packingSlipUrl
                    jobsheet_pdf = f'Jobsheet_{root_orderline.orderId}_{root_orderline.orderDetailId}.pdf'
                    print(jobsheet_pdf)
                    logging.info(f"Helloprint Jobsheet PDF: {jobsheet_pdf}")

                    jobsheet_dest = f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}/{jobsheet_pdf}'
                    print(jobsheet_dest)
                    logging.info(f"Helloprint Jobsheet PDF destination: {jobsheet_dest}")

                    # pdf_data = process_pdf_files(Path(jobsheet_dest),Path(pdf_dest))
                    # collect shape rolwikkeling from jobsheet
                    # collect width and height from artwork
                    # if data != in cermjson dan ....

                    download_file_from_url(url_art_pdf, Path(pdf_dest))
                    download_file_from_url(url_jobsheet_pdf, Path(jobsheet_dest))

                    padzip_src = Path(f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}')
                    padzip_dest = Path(
                        f'{DOWNLOAD_PAD_VILA_TO_ESKO}/{root_orderline.orderId}_{root_orderline.orderDetailId}')
                    zip_folder(padzip_src, padzip_dest)

                logging.info(f"Finished processing file: {original_json_file.name}")
                # Delete the processed JSON file
                try:
                    original_json_file.unlink()
                    logging.info(f"Successfully deleted file: {original_json_file}")
                except Exception as e:
                    logging.error(f"Error deleting file {original_json_file}: {e}")

            except Exception as e:
                logging.error(f"Exception occurred while processing file {original_json_file}: {e}")

        logging.info("Completed processing all files. Waiting for next check.")
        time.sleep(300)  # Wait for 5 minutes before next iteration
