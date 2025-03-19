import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Hypixel API configuration
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
BAZAAR_ENDPOINT = "https://api.hypixel.net/skyblock/bazaar"
AUCTION_ENDPOINT = "https://api.hypixel.net/skyblock/auctions"

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Items to monitor - format: {item_id: {"name": "Display Name", "high_threshold": value, "low_threshold": value}}
MONITORED_ITEMS = {
    "STOCK_OF_STONKS": {
        "name": "Stock of Stonks", 
        "high_threshold": 4000000.0,  # Alert when SELL price exceeds this value
        "low_threshold": 3500000.0,   # Alert when BUY price falls below this value
    },
    "ESSENCE_UNDEAD": {
        "name": "Undead Essence",
        "high_threshold": 750.0,
        "low_threshold": 645.0,
    },
    "ENCHANTED_SLIME_BALL": {
        "name": "Enchanted Slime Ball",
        "high_threshold": 910.0,
        "low_threshold": 600.0,
    }
    # Add more items as needed
}

# Debug configuration
SHOW_THRESHOLD_MESSAGES = True  # Set to False to hide threshold messages

# How often to check prices (in seconds)
CHECK_INTERVAL = 60
