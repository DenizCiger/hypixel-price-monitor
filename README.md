# Hypixel Price Monitor

This project monitors the prices of items on Hypixel's Skyblock and sends notifications via Telegram when certain thresholds are crossed.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/DenizCiger/hypixel-price-monitor.git
    cd hypixel-price-monitor
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your Hypixel API key and Telegram bot token:
    ```env
    HYPIXEL_API_KEY=your_hypixel_api_key
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    ```

5. Run the price monitor:
    ```sh
    python price_monitor.py
    ```

## Configuration

You can configure the items to monitor and their thresholds in the `config.py` file.

## License

This project is licensed under the MIT License.