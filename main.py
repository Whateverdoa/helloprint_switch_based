import json
import os
from dataclasses import asdict
import time
from pathlib import Path
import requests
import shutil

from Paden.paden import HP_CERM_CONN, HP_CERM_CONN_TEST, hp_cerm_conv_pad, DOWNLOAD_PAD_VILA_TO_ESKO,logpad_test
from conversions.helloprint_conversion import convert_helloprint_address_to_contact, \
    convert_helloprint_json_into_orderinfo
from conversions.helloprint_sku import translate_sku
from conversions.pdc_conversion import save_json
from models_helloprint.main_testing_hp_json import read_order_from_file, download_file_from_url, zip_folder

from loguru import logger
from pynotifier import Notification

# Intercept standard logging messages
logger.remove()
logger.add(logpad_test, format="{time} {level} {message}", level="INFO")

def contains_sku_off(order):
    for order_line in order.orderLines:
        if order_line.sku == 'OFF':
            return True
    return False

if __name__ == "__main__":
    json_dir = HP_CERM_CONN_TEST

    while True:
        json_files = sorted(json_dir.glob('*.json'))
        logger.info(f"Found JSON files: {json_files}")

        for original_json_file in json_files:
            try:
                logger.info(f"Starting processing file: {original_json_file.name}")
                root_object = read_order_from_file(original_json_file)
                if root_object is None:
                    logger.warning(f"No data in file {original_json_file}, skipping.")
                    continue

                # Check if any order contains 'SKU OFF' and delete such files
                if any(contains_sku_off(order) for order in root_object.orders):
                    logger.warning(f"File {original_json_file} contains 'SKU OFF', deleting.")
                    original_json_file.unlink()
                    continue

                sku_s = []
                root_object = read_order_from_file(original_json_file)
                if root_object is not None:
                    logger.debug("-------root object-------")
                    logger.debug(root_object)

                    root_orderline = root_object.orders[0].orderLines[0]

                    logger.debug("-------")

                    json_file = f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}/{root_orderline.orderId}_{root_orderline.orderDetailId}.json'
                    logger.debug('________')
                    contacts = convert_helloprint_address_to_contact(root_orderline.address)
                    sku_s.append((root_orderline.sku, translate_sku(root_orderline.sku)))
                    helloprint_converted_dataclass = convert_helloprint_json_into_orderinfo(root_orderline)
                    logger.debug(helloprint_converted_dataclass)

                    save_json(asdict(helloprint_converted_dataclass),
                              Path(json_file))

                    logger.debug(root_object.orders[0].orderLines[0].files_to_download.filename)
                    url_art_pdf = root_object.orders[0].orderLines[0].files_to_download.filename
                    art_pdf = f'Artwork_{root_orderline.orderId}_{root_orderline.orderDetailId}.pdf'
                    logger.info(f"Helloprint Artwork PDF: {art_pdf}")

                    pdf_dest = f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}/{art_pdf}'
                    logger.info(f"Helloprint Artwork PDF destination: {pdf_dest}")

                    logger.debug(root_object.orders[0].orderLines[0].files_to_download.packingSlipUrl)
                    url_jobsheet_pdf = root_object.orders[0].orderLines[0].files_to_download.packingSlipUrl
                    jobsheet_pdf = f'Jobsheet_{root_orderline.orderId}_{root_orderline.orderDetailId}.pdf'
                    logger.info(f"Helloprint Jobsheet PDF: {jobsheet_pdf}")

                    jobsheet_dest = f'{hp_cerm_conv_pad}/{root_orderline.orderId}_{root_orderline.orderDetailId}/{jobsheet_pdf}'
                    logger.info(f"Helloprint Jobsheet PDF destination: {jobsheet_dest}")

                    try:
                        download_file_from_url(url_art_pdf, Path(pdf_dest))
                        download_file_from_url(url_jobsheet_pdf, Path(jobsheet_dest))
                    except Exception as e:
                        logger.error(f"Error downloading file: {e}")

                logger.info(f"Finished processing file: {original_json_file.name}")
                # Delete the processed JSON file
                try:
                    original_json_file.unlink()
                    logger.info(f"Successfully deleted file: {original_json_file}")
                except Exception as e:
                    logger.error(f"Error deleting file {original_json_file}: {e}")

            except Exception as e:
                logger.error(f"Exception occurred while processing file {original_json_file}: {e}")

        logger.info("Completed processing all files. Waiting for next check.")
        time.sleep(5*60)  
        logger.info('Wait for 5 minutes before next iteration')