from pathlib import Path
import json


def load_json_file(file_path: Path):
    """
    Load helloprint_converted_dataclass JSON file from the given file path.

    Args:
        file_path (Path): The path to the JSON file.

    Returns:
        dict: The content of the JSON file as helloprint_converted_dataclass Python dictionary.
    """
    with open(file_path, "r") as f:
        return json.load(f)


def extract_general_info(data: dict):
    """
    Extract general information like address, width, and height.

    Args:
        data (dict): The order data.

    Returns:
        dict: A dictionary containing the extracted general information.
    """
    general_info = {}

    # Extract address
    address_info = data.get("shipments")[0].get("address", {})
    general_info["address"] = {
        "first_name": address_info.get("firstName"),
        "last_name": address_info.get("lastName"),
        "company_name": address_info.get("companyName"),
        "email": address_info.get("email"),
        "telephone": address_info.get("telephone"),
        "full_street": address_info.get("fullstreet"),
        "house_number": address_info.get("houseNumber"),
        "city": address_info.get("city"),
        "country": address_info.get("country"),
        "postcode": address_info.get("postcode"),
    }

    # Extract dimensions
    options = data.get("options", {})
    general_info["dimensions"] = {
        "width": options.get("width"),
        "height": options.get("height"),
    }

    return general_info


def extract_design_info(data: dict):
    """
    Extract information for each design.

    Args:
        data (dict): The order data.

    Returns:
        list[dict]: A list of dictionaries containing the extracted information for each design.
    """
    designs_info = []

    designs = data.get("designs", [])
    for design in designs:
        design_info_ = {
            "id": design.get("id"),
            "copies": design.get("copies"),
            "href": design.get("href"),
        }
        designs_info.append(design_info_)

    return designs_info


if __name__ == "__main__":
    # Replace with the actual path to your JSON file
    json_file_path = Path("6001120212-1.json")

    # Load the JSON data
    order_data = load_json_file(json_file_path)

    # Extract and display general information
    general_info = extract_general_info(order_data)
    print(f"General Information: {general_info}")

    # Extract and display design-specific information
    design_info = extract_design_info(order_data)
    print(f"Design Information: {design_info}")
