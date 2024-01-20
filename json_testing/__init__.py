from pathlib import Path
from typing import List

def find_json_files(directory: Path) -> List[str]:
    """
    Find all JSON files in the given directory and return their names.

    Args:
        directory (Path): The directory to search for JSON files.

    Returns:
        List[str]: A list of filenames for the JSON files.
    """
    return [json_file.name for json_file in directory.glob("*.json")]

if __name__ == "__main__":
    # Replace this with the directory you want to search
    directory_path = Path("path/to/directory")

    if directory_path.exists() and directory_path.is_dir():
        json_filenames = find_json_files(directory_path)

        if json_filenames:
            print("Found the following JSON filenames:")
            for filename in json_filenames:
                print(filename)
        else:
            print("No JSON files found.")

    else:
        print(f"Directory {directory_path} does not exist.")

# Store the filenames in helloprint_converted_dataclass variable for reuse
json_filenames_for_reuse = json_filenames if 'json_filenames' in locals() else []
