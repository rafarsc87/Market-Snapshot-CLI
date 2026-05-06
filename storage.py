import os
import csv
from datetime import datetime
from typing import Dict, List

base_dir = os.path.dirname(os.path.abspath(__file__))


def create_file_if_not_exists(file_path: str) -> None:
    """
    Ensures that the directory for the given file path exists and creates the file
    with a header if it does not already exist.

    Args:
        file_path (str): The full path to the CSV file.
    """
    folder_path = os.path.dirname(file_path)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True) 

    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "asset", "price", "variation"])


def save_csv(file_path: str, data: Dict[str, float]) -> None:
    """
    Appends new market data to a specified CSV file.

    If the file or its directory does not exist, they will be created.
    Each entry in the 'data' dictionary is written as a new line, including
    the current timestamp and an empty 'variation' field.

    Args:
        file_path (str): The full path to the CSV file where data will be saved.
        data (Dict[str, float]): A dictionary where keys are asset names (e.g., "USD/BRL")
                                  and values are their current prices.
    """
    create_file_if_not_exists(file_path)

    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for asset, price in data.items():
            # Variation is left empty as per logic requirements
            writer.writerow([today, asset, price, ""])


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Reads data from a specified CSV file and returns it as a list of dictionaries.

    Each dictionary represents a row, with keys corresponding to the CSV header.
    If the file does not exist or is empty, an empty list is returned.

    Args:
        file_path (str): The full path to the CSV file to be read.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary
                              represents a row from the CSV. All values are strings.
    """
    if not os.path.exists(file_path):
        return [] # Return empty list if file doesn't exist

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


if __name__ == "__main__":
    test_path = os.path.join(base_dir, "Data", "test.csv")
    print(f"Testing with file: {test_path}")

    # Clean up previous test file if it exists
    if os.path.exists(test_path):
        os.remove(test_path)
        print(f"Cleaned up existing {test_path}")

    test_data = {
        "USD/BRL": 5.10,
        "EUR/BRL": 5.96
    }

    # Test save_csv
    print("Saving test data...")
    save_csv(test_path, test_data)
    print("Data saved.")

    # Test read_csv
    print("Reading data...")
    data = read_csv(test_path)
    print(data)

    # Test with an empty file (after deleting the test file)
    print("\nTesting with an empty/non-existent file...")
    if os.path.exists(test_path):
        os.remove(test_path)
    empty_data = read_csv(test_path)
    print(f"Read from empty file: {empty_data}")

    # Test saving again to a newly created file
    print("\nSaving to a new file after deletion...")
    save_csv(test_path, {"GBP/BRL": 6.50})
    new_data = read_csv(test_path)
    print(f"Read from new file: {new_data}")

    # Clean up test file
    if os.path.exists(test_path):
        os.remove(test_path)
        print(f"\nCleaned up {test_path}")