#!/usr/bin/env python3
import re
from typing import Dict, Any
from pathlib import Path
import PyPDF2
import pdfplumber
from datetime import datetime
wdir = Path.cwd().parent
print(wdir)

# job_pdf_pad = wdir.joinpath('data/cerm_helloprint_conversions/4142804_6140156/Jobsheet_4142804_6140156.pdf')
job_pdf_pad = wdir.joinpath('data/cerm_helloprint_conversions/4203521_6243800/Jobsheet_4203521_6243800.pdf')
artwork_pdf_pad = wdir.joinpath('data/cerm_helloprint_conversions/4203521_6243800/Artwork_4203521_6243800.pdf')



def calculate_dimensions(width, height, winding):
    if winding in (1, 2, 5, 6):
        return width, height
    elif winding in (3, 4, 7, 8):
        return height, width
    else:
        raise ValueError("Invalid winding value. Winding must be 1, 2, 3, 4, 5, 6, 7, or 8.")



def get_today_date_str():
    """
    Get the current date as a formatted string.

    Returns:
        str: The current local date in "YYYY-MM-DD" format.
    """
    return datetime.today().strftime('%Y-%m-%d-%H-%M-%S')


def extract_text_with_pdfplumber(pdf_path: Path) -> str:
    """
    Extract text from a PDF file using pdfplumber.

    Args:
        pdf_path (Path): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""

    # Check if the given path is a PDF file
    if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"The provided path {pdf_path} is not a valid PDF file.")

    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Loop through each page and extract text
        for page in pdf.pages:
            text += page.extract_text()

    return text


import re
from typing import List, Dict, Union


def extract_text_details(text: str, patterns: List[str]) -> Dict[str, Union[str, List[str]]]:
    """
    Extracts multiple details from a given text using a list of regex patterns.

    Args:
        text (str): The text to search.
        patterns (List[str]): A list of regex patterns to apply.

    Returns:
        Dict[str, Union[str, List[str]]]: A dictionary containing the extracted information.
                                         The keys are the patterns, and the values are the extracted data.
    """
    extracted_details = {}

    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            if len(matches) == 1:
                extracted_details[pattern] = matches[0]
            else:
                extracted_details[pattern] = matches
        else:
            extracted_details[pattern] = "Not found"

    return extracted_details


def extract_dimensions(text: str, pattern: str = r"\b\d{1,4} x \d{1,4} mm\b") -> List[str]:
    """
    Extract dimensions from text using a regular expression pattern.

    Args:
        text (str): The input text.
        pattern (str, optional): The regex pattern for extracting dimensions. Defaults to r"\b\d{1,4} x \d{1,4} mm\b".

    Returns:
        List[str]: A list of all dimensions found.
    """
    return re.findall(pattern, text)


def extract_trimbox_with_pypdf2(pdf_path: Path) -> [str, Dict[str, float]]:
    """
    Extract the trim box dimensions from a PDF file using PyPDF2.

    Args:
        pdf_path (Path): The path to the PDF file.

    Returns:
        str: The trim box dimensions as a string, if available.
    """

    # Check if the given path is a PDF file
    if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"The provided path {pdf_path} is not a valid PDF file.")

    # Open the PDF file
    with open(pdf_path, "rb") as f:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(f)

        # Get the first page (assuming the trim box is the same for all pages)
        pypdf2_page = pdf_reader.pages[0]

        # Get the trim box, if available
        try:
            trimbox = pypdf2_page['/TrimBox']
        except KeyError:
            return "TrimBox not found in PDF."

    return trimbox


def extract_all_boxes_with_pypdf2(pdf_path: Path) -> dict:
    """
    Extract all the box dimensions from the first page of a PDF file using PyPDF2.

    Args:
        pdf_path (Path): The path to the PDF file.

    Returns:
        dict: A dictionary containing the dimensions of all available boxes.
    """

    # Check if the given path is a PDF file
    if not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"The provided path {pdf_path} is not a valid PDF file.")

    box_dict = {}

    # Open the PDF file
    with open(pdf_path, "rb") as f:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(f)

        # Get the first page (assuming the boxes are the same for all pages)
        pypdf2_page = pdf_reader.pages[0]

        # Get all the boxes, if available
        for box_type in ['/MediaBox', '/CropBox', '/BleedBox', '/TrimBox', '/ArtBox']:
            try:
                box_dict[box_type] = pypdf2_page[box_type]
            except KeyError:
                box_dict[box_type] = "Not found in PDF."

    return box_dict


def extract_box_details(box_coords: List[float]) -> Dict[str, float]:
    """
    Extracts the details of a PDF box (like TrimBox) given its coordinates.

    Args:
        box_coords (List[float]): The coordinates of the box in points.
                                 Format: [x_ll, y_ll, x_ur, y_ur]

    Returns:
        Dict[str, float]: A dictionary containing the lower-left and upper-right corners,
                          as well as the width and height of the box in millimeters.
    """
    # Conversion factor from points to mm (1 point = 1/72 inch, 1 inch = 25.4 mm)
    conversion_factor = 25.4 / 72

    # Convert the box coordinates to native Python floats, then to mm
    box_mm = [float(coord) * conversion_factor for coord in box_coords]

    # Extract individual coordinates for clarity
    x_ll, y_ll, x_ur, y_ur = box_mm

    # Calculate the width and height of the box
    width = x_ur - x_ll
    height = y_ur - y_ll

    # Create a dictionary to hold the rounded results
    box_details = {
        'Lower_Left_Corner': (round(x_ll, 2), round(y_ll, 2)),
        'Upper_Right_Corner': (round(x_ur, 2), round(y_ur, 2)),
        'Width_mm': round(width, 2),
        'Height_mm': round(height, 2)
    }

    return box_details




def parse_jobsheet_text(text: str) -> Dict[str, Any]:
    parsed_data = {}

    # Extract Form (in multiple languages)
    form_pattern = r"(Vorm|Form|Forme|Forma|Formato|Format):\s*(.*?)\s*-"
    form_match = re.search(form_pattern, text, re.IGNORECASE)
    if form_match:
        parsed_data['shape'] = form_match.group(2).strip()

    # Extract Rolw (Rolw2 as an example)
    rolw_pattern = r"ROLW(\d+)"
    rolw_match = re.search(rolw_pattern, text)
    if rolw_match:
        parsed_data['rolw'] = int(rolw_match.group(1))
    else:
        parsed_data['rolw'] = 2

    return parsed_data

def process_pdf_files(job_pdf_path: Path, artwork_pdf_path: Path): # -> Dict[str, Any]:
    extracted_text = extract_text_with_pdfplumber(job_pdf_path)
    parsed_data = parse_jobsheet_text(extracted_text)

    trimbox = extract_trimbox_with_pypdf2(artwork_pdf_path)
    trimbox_details = extract_box_details(trimbox)

    width, height = trimbox_details['Width_mm'], trimbox_details['Height_mm']

    rolwikkeling = parsed_data.get('rolw', 2)  # Default to 2 if not found
    w, h = calculate_dimensions(width, height, rolwikkeling)

    return {
        'width': w,
        'height': h,
        'rolwikkeling': rolwikkeling,
        'parsed_data': parsed_data
    }


if __name__ == "__main__":
    # pdf_path = job_pdf_pad  # Replace with your PDF path
    # extracted_text = extract_text_with_pdfplumber(pdf_path)
    # # print(extracted_text)
    #
    #
    # # Example usage
    # parsed_data = parse_jobsheet_text(extracted_text)
    # print(parsed_data)
    #
    # pdf_path2 = Path(artwork_pdf_pad)  # Replace with your PDF path
    # trimbox = extract_trimbox_with_pypdf2(pdf_path2)
    # # print(f"Trim Box: {trimbox}")
    #
    # # all_boxes = extract_all_boxes_with_pypdf2(pdf_path2)
    # # # print(f"All Boxes: {all_boxes}")
    #
    # trimbox_details = extract_box_details(trimbox)
    # width = trimbox_details['Width_mm']
    # height = trimbox_details['Height_mm']
    #
    # print(width, height)
    #
    #
    #
    # rolwikkeling = parsed_data['rolw']
    # w, h = calculate_dimensions(width, height, rolwikkeling)  # Example with winding 2
    # print(f"Width: {w}, Height: {h}, rw {rolwikkeling}")
    # # w, h = calculate_dimensions(width, height, 3)  # Example with winding 3
    # # print(f"Width: {w}, Height: {h}")


    # print(process_pdf_files(job_pdf_pad, artwork_pdf_pad))
    # print(process_pdf_files(job_pdf_pad, artwork_pdf_pad))
    ...