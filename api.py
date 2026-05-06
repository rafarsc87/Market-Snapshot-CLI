import requests 
from typing import Dict, Optional


def _fetch_awesome_api(url: str, description: str) -> Optional[Dict]:
    """
    Helper function to handle GET requests to AwesomeAPI.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\n[API Error] Could not fetch {description}: {e}")
        return None
    

def get_currency_prices() -> Optional[Dict[str, float]]:
    """
    Fetches current USD and EUR prices in BRL using the AwesomeAPI.

    Returns:
        Optional[Dict[str, float]]: Dictionary with USD/BRL and EUR/BRL bid prices.
        Or None if the request fails.
    """
    
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"
    
    data = _fetch_awesome_api(url, "currency data")
    
    if data is None:
        return None
    else:
        return {
            "USD/BRL": float(data["USDBRL"]["bid"]),
            "EUR/BRL": float(data["EURBRL"]["bid"])
        }


def get_crypto_prices() -> Optional[Dict[str, float]]:
    """
    Fetches current BTC and ETH prices in USD using the AwesomeAPI.

    Returns:
        Optional[Dict[str, float]]: Dictionary with BTC/USD and ETH/USD bid prices.
        Or None if the request fails.
    """
    
    url = "https://economia.awesomeapi.com.br/last/BTC-USD,ETH-USD"

    data = _fetch_awesome_api(url, "crypto data")

    if data is None:
        return None
    else:
        return {
            "BTC/USD": float(data["BTCUSD"]["bid"]),
            "ETH/USD": float(data["ETHUSD"]["bid"])
        }
    

def test_error_handling() -> None:
    """
    Simulates API error scenarios to verify that the application handles 
    HTTP errors (404) and connection issues gracefully.
    """
    
    print("\n--- Testing Error Handling ---")
    
    # 1. Force the raise_for_status() -> URL does not exist (404 Error)
    print("1. Forcing raise_for_status (404 Error):")
    url_404 = "https://economia.awesomeapi.com.br/last/MOEDA-INEXISTENTE"
    try:
        res = requests.get(url_404)
        res.raise_for_status() 
    except Exception as e:
        print(f"Caught expected status error: {e}")

    # 2. Force the except (Exception) -> URL with domain that does not exist (Connection Error)
    print("\n2. Forcing Connection Error (General Exception):")
    url_invalid = "https://url.que.nao.existe.com.br"
    try:
        res = requests.get(url_invalid, timeout=2)
    except requests.exceptions.RequestException as e:
        print(f"Caught expected HTTP error: {e}")


if __name__ == "__main__":
    # Execute the test function to verify error handling works as expected
    test_error_handling()

    print("\n--- Testing Normal Operation ---")
    prices = get_currency_prices()
    print(prices)

    crypto_prices = get_crypto_prices()
    print(crypto_prices)