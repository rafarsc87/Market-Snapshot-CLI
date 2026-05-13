# Market Snapshot CLI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A Python command-line interface (CLI) tool designed to provide real-time snapshots of financial markets. It fetches current exchange rates for fiat currencies and cryptocurrencies, compares them against historical data, and saves the records for future analysis.

## 🚀 Features

-   **Real-time Market Data:** Fetches current bid prices for:
    -   **Fiat Currencies:** USD/BRL and EUR/BRL.
    -   **Cryptocurrencies:** BTC/USD and ETH/USD.
-   **Historical Comparison:** Compares current prices with the last recorded data from the previous day, showing percentage variations.
-   **Persistent Data Storage:** Automatically saves all fetched data into CSV files (`currencies.csv` and `cryptos.csv`) within a `Data/` directory, building a historical record.
-   **Robust Error Handling:** Implements comprehensive error handling for API requests, gracefully managing connection issues, timeouts, and HTTP status errors (e.g., 404 Not Found).
-   **Interactive CLI Menu:** Provides a user-friendly menu to select between checking currencies or cryptocurrencies.
-   **Color-coded Output:** Displays price variations with intuitive green (positive) and red (negative) colors for easy readability.

## 🛠️ Technologies Used

-   Python 3.x
-   Requests: Used for API communication and HTTP requests.

## 📋 Prerequisites

Before running the application, ensure you have Python 3.x installed on your system.

You'll also need to install the `requests` library:

```bash
pip install requests
```

## 🚀 Installation & How to Use

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rafarsc87/market-snapshot-cli.git
    cd market-snapshot-cli
    ```
    
2.  **Run the main application:**
    ```bash
    python main.py
    ```

3.  **Interact with the menu:**
    The application will present an interactive menu. Choose an option to fetch data.
    -   Option `1`: Check USD/BRL and EUR/BRL prices.
    -   Option `2`: Check BTC/USD and ETH/USD prices.
    -   Option `3`: Exit the application.

    After each check, the current data will be displayed, compared with the last recorded data, and then saved to the respective CSV file in the `Data/` directory.

## 📖 Code Structure

The project is organized into several modules for clarity and maintainability:

-   `api.py`: Contains functions for interacting with the AwesomeAPI, including `_fetch_awesome_api` (a private helper for HTTP requests and error handling), `get_currency_prices`, and `get_crypto_prices`.
-   `storage.py`: Handles reading from and saving data to CSV files (`read_csv`, `save_csv`).
-   `logic.py`: Contains the business logic for comparing current data with historical data and building the report (`build_report`).
-   `main.py`: The main entry point of the CLI application, managing the user interface, menu, control flow, and orchestrating calls to other modules.   


---
## 📄 License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## 👨‍💻 Connect with me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rafael-salgado-940ab9406)

## 👨‍💻 Developed By

Rafael Salgado
*Building Python Backend Applications*