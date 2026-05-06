import sys
import os
from typing import List, Dict, Any, Callable, Optional
from api import get_currency_prices, get_crypto_prices
from storage import read_csv, save_csv
from logic import build_report


# ----------------------------
# Market Snapshot CLI V1
# Main - Control flow
# ----------------------------

# ANSI Color Codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def show_menu() -> None:
    """Displays the main menu and tool description to the user."""
    
    print("\n" + "="*30)
    print("      MARKET SNAPSHOT CLI     ")
    print("="*30)
    
    print("\nWelcome! This tool provides a quick snapshot of the financial market.")
    print("How it works:")
    print("- Fetches real-time prices for Currencies (USD/EUR in BRL) and Crypto (BTC/ETH in USD).")
    print("- Prices based on BID value (market buy price).")
    print("- Compares current data with the last record from the previous day.")
    print("- Automatically saves a history of every check in CSV files.")
    print("- Press Ctrl+C at any time to exit the application.  \n")
    print("-" * 30)

    print(" 1. Check Currencies (USD/EUR)")
    print(" 2. Check Crypto (BTC/ETH)")
    print(" 3. Exit")
    print("="*30)


def get_user_choice() -> str:
    """
    Prompts the user for a menu choice and validates the input.

    Returns:
        str: A valid option string ('1', '2', or '3').
    """
    valid_options = ["1", "2", "3"]

    while True:
        try:
            user_choice = input("Choose an option: ").strip()
            if user_choice in valid_options:
                return user_choice
            else:
                print("Invalid option. Please choose again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)


def display_results(report: List[Dict[str, Any]]) -> None:
    """
    Formats and prints the market report to the console with color coding.

    Args:
        report (List[Dict[str, Any]]): List of asset data including current price,
                                       previous price, and variation.
    """
    print("\n--- Current Market Status ---")
    for item in report:
        asset = item['asset']
        current = item['current']
        previous = item['previous']
        previous_date = item['previous_date']
        variation = item['variation']

        if variation is None:
            print(f"{asset}: {current} (prev: N/A) (no previous data)")
        elif variation > 0:
            print(f"{asset}: {current} (prev: {previous} in {previous_date}) ({GREEN}variation: +{variation}%{RESET})")
        elif variation < 0:
            print(f"{asset}: {current} (prev: {previous} in {previous_date}) ({RED}variation: {variation}%{RESET})")
        else:
            print(f"{asset}: {current} (prev: {previous} in {previous_date}) (variation: 0%)")


def process_market_request(
    fetch_callback: Callable[[], Optional[Dict[str, float]]], 
    file_path: str, 
    label: str
) -> None:
    """
    Orchestrates the data flow: fetch from API, read history, build report, 
    display results, and save current data.

    Args:
        fetch_callback: The function to call to get current prices.
        file_path: Path to the CSV file for this asset type.
        label: Descriptive name (e.g., 'Currencies').
    """
    print(f"\nChecking {label}...")
    current_data = fetch_callback()

    if current_data is None:
        print(f"Error: Failed to fetch {label.lower()} prices.")
        return

    # Load history and generate comparison
    history = read_csv(file_path)
    report = build_report(current_data, history)
    
    # Output and Persist
    display_results(report)
    save_csv(file_path, current_data)
    
    input("\nPress Enter to return to menu...")


def main() -> None:   
    """Main entry point for the CLI application."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    currency_path = os.path.join(base_dir, "Data", "currencies.csv")
    crypto_path = os.path.join(base_dir, "Data", "cryptos.csv")

    while True:
        show_menu()
        choice = get_user_choice()

        try:
            if choice == "1":
                process_market_request(get_currency_prices, currency_path, "Currencies")
                    
            elif choice == "2":
                process_market_request(get_crypto_prices, crypto_path, "Cryptocurrencies")
            
            elif choice == "3":
                print("Exiting...")
                break

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            input("Press Enter to continue...")

    print("Goodbye!")

if __name__ == "__main__":
    main()