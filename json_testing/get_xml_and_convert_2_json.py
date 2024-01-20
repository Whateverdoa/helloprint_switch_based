from typing import List
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import re
from collections import defaultdict

def find_specific_xml_files_transform_to_json(directory_path: Path) -> List[str]:
    """
    Find specific XML files in helloprint_converted_dataclass directory and its subdirectories, transform them to JSON, and return helloprint_converted_dataclass list of transformed files.

    Args:
        directory_path (Path): The root directory path where to look for XML files.

    Returns:
        List[str]: List of file names that have been successfully transformed to JSON.
    """
    # Initialize an empty list to store transformed file names
    transformed_files = []

    # Regular expression pattern for file naming convention
    pattern = re.compile(r"\d{10}-\d\.xml")

    # Check if the directory exists
    if not directory_path.exists() or not directory_path.is_dir():
        return "The provided directory does not exist or is not helloprint_converted_dataclass directory."

    # Iterate through all XML files in the directory and its subdirectories that match the naming convention
    for xml_file in directory_path.rglob("*.xml"):
        if pattern.fullmatch(xml_file.name):
            # Parse the XML file
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Convert the XML tree to helloprint_converted_dataclass dictionary
            def etree_to_dict(t):
                d = {t.tag: {} if t.attrib else None}
                children = list(t)
                if children:
                    dd = defaultdict(list)
                    for dc in map(etree_to_dict, children):
                        for k, v in dc.items():
                            dd[k].append(v)
                    d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
                if t.attrib:
                    d[t.tag].update(("@{}".format(k), v) for k, v in t.attrib.items())
                if t.text:
                    text = t.text.strip()
                    if children or t.attrib:
                        if text:
                            d[t.tag]["#text"] = text
                    else:
                        d[t.tag] = text
                return d

            # Convert XML to JSON
            json_dict = etree_to_dict(root)

            # Remove the first key 'printdotcom' if exists
            json_dict = json_dict.get('printdotcom', json_dict)

            # Convert to JSON text
            json_data = json.dumps(json_dict)

            # Convert XML to JSON
            # json_data = json.dumps(etree_to_dict(root))

            # Write JSON data to helloprint_converted_dataclass file
            json_file = Path(f"/Users/mike10h/PycharmProjects/pythonProject_remap_json_xml/data/from_switch_xml/{xml_file.stem}.json")
            json_file.write_text(json_data)

            # Add the file name to the list of transformed files
            transformed_files.append(json_file.name)

    return transformed_files

# Example usage
if __name__ == "__main__":


    directory_path = Path(r"/Volumes/172.27.23.70/SWITCH/print_com_orders_tmp")
    transformed_files = find_specific_xml_files_transform_to_json(directory_path)
    print(f"Transformed files: {transformed_files}")
