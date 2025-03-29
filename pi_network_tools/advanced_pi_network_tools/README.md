
# Advanced Pi Network Tools ( Network Monitoring System ) 

## Overview

**Advanced Pi Network Tools** is an advanced network monitoring and cryptocurrency connectivity application designed for the Raspberry Pi. This project provides functionalities for testing network connectivity, monitoring Wi-Fi signal strength, analyzing network traffic, and integrating cryptocurrency functionalities. It is modular, efficient, and user-friendly, making it suitable for both personal and professional use.

## Features

- **Connectivity Testing**: Periodically tests connectivity to a specified host (default is Google's public DNS).
- **Wi-Fi Signal Monitoring**: Monitors the Wi-Fi signal strength and SSID of the connected network.
- **Network Traffic Analysis**: Tracks the amount of data sent and received over each network interface.
- **Cryptocurrency Integration**: Connects to cryptocurrency APIs to fetch real-time data.
- **Asynchronous Operations**: Utilizes asynchronous programming for improved performance and responsiveness.
- **Comprehensive Logging**: Logs detailed information about network status and events.
- **Configuration Management**: Uses a `.env` file for easy configuration of settings.
- **Graceful Shutdown**: Handles termination signals for a clean exit.

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `psutil`
  - `python-dotenv`
  - `requests` (for cryptocurrency API integration)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KOSASIH/Pi-CryptoConnect.git
   cd Pi-CryptoConnect
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**:
   Copy the provided `.env` template and customize it according to your needs:
   ```plaintext
   # General Configuration
   CHECK_INTERVAL=10  # Time in seconds to check connectivity and Wi-Fi signal strength
   TIMEOUT=5          # Timeout for connection attempts
   TEST_HOST=8.8.8.8  # Default host to test connectivity (Google's public DNS)

   # Wi-Fi Configuration
   WIFI_INTERFACE=wlan0  # The interface to check for Wi-Fi signal strength

   # Network Traffic Monitoring
   TRAFFIC_CHECK_INTERVAL=10  # Time in seconds to check network traffic

   # Cryptocurrency API Configuration
   CRYPTO_API_URL=https://api.coingecko.com/api/v3/simple/price
   CRYPTO_CURRENCY=bitcoin  # Default cryptocurrency to monitor

   # Logging Configuration
   LOG_LEVEL=INFO  # Log level can be DEBUG, INFO, WARNING, ERROR, CRITICAL
   ```

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Monitor the logs**: The application will log connectivity tests, Wi-Fi signal strength, network traffic statistics, and cryptocurrency data to the console.

3. **Stop the application**: You can stop the application gracefully by pressing `Ctrl+C` in the terminal.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the contributors and the open-source community for their support and inspiration.
- Special thanks to the developers of the libraries used in this project: [psutil](https://github.com/giampaolo/psutil), [python-dotenv](https://github.com/theskumar/python-dotenv), and [requests](https://docs.python-requests.org/en/master/).
