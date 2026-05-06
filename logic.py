from datetime import datetime
from typing import List, Dict, Optional, Any


def find_previous_day_price(asset_history: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    """
    Filters the asset history to find the most recent price record that is not from today.

    Args:
        asset_history (List[Dict[str, str]]): List of historical records for a specific asset.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing 'price' and 'date' of the last record 
                                  from a previous day, or None if not found.
    """
   
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Filter records where the date part (YYYY-MM-DD) is different from today
    previous_records = [record for record in asset_history if record["date"].split(" ")[0] != today]

    if previous_records:
        last_record = previous_records[-1]
        return {
                "price": float(last_record["price"]),
                "date": last_record["date"]
        }

    return None
    
    
def calculate_variation(current_price: float, previous_price: Optional[float]) -> Optional[float]:
    """
    Calculates the percentage variation between the current and previous price.

    Args:
        current_price (float): The current asset price.
        previous_price (Optional[float]): The previous recorded price.

    Returns:
        Optional[float]: Percentage variation rounded to 2 decimal places, or None if invalid.
    """
    
    if previous_price is None or previous_price == 0:
        return None
    
    variation = (current_price - previous_price) / previous_price * 100
    
    return round(variation, 2)


def build_report(current_data: Dict[str, float], history: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Orchestrates the data comparison to build a final market report.

    Args:
        current_data (Dict[str, float]): Current prices from the API.
        history (List[Dict[str, str]]): Historical data from the CSV.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing the full report for each asset.
    """
    
    report = []

    for asset, current_price in current_data.items():
        asset_history = [record for record in history if record['asset'] == asset]
        previous_price: Optional[float] = None
        previous_date: Optional[str] = None
        variation: Optional[float] = None
        

        # One single call to get both price and date
        last_data = find_previous_day_price(asset_history)
            
        if last_data:
            previous_price = last_data["price"]
            previous_date = last_data["date"]
            variation = calculate_variation(current_price, previous_price)
            
        report.append({
            "asset": asset,
            "current": current_price,
            "previous": previous_price,
            "previous_date": previous_date,
            "variation": variation
        })
                    
    return report


if __name__ == "__main__":
    current_data = {
        "USD/BRL": 5.50,
        "EUR/BRL": 6.26
    }
    history = [
        {'date': '2026-04-09 16:46', 'asset': 'USD/BRL', 'price': '5.1', 'variation': ''}, 
        {'date': '2026-04-09 16:46', 'asset': 'EUR/BRL', 'price': '5.96', 'variation': ''}, 
        {'date': '2026-04-15 10:59', 'asset': 'USD/BRL', 'price': '5.1', 'variation': ''}, 
        {'date': '2026-04-15 10:59', 'asset': 'EUR/BRL', 'price': '5.96', 'variation': ''}, 
        {'date': '2026-04-15 15:03', 'asset': 'USD/BRL', 'price': '5.1', 'variation': ''}, 
        {'date': '2026-04-15 15:03', 'asset': 'EUR/BRL', 'price': '5.96', 'variation': ''}
    ]
    report = build_report(current_data, history)
    print(report)
