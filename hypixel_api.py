import requests
import logging
from config import HYPIXEL_API_KEY, BAZAAR_ENDPOINT, AUCTION_ENDPOINT

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hypixel_price_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("hypixel_api")

def fetch_bazaar_data():
    """Fetch bazaar data from Hypixel API"""
    try:
        headers = {"API-Key": HYPIXEL_API_KEY} if HYPIXEL_API_KEY else {}
        response = requests.get(BAZAAR_ENDPOINT, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching bazaar data: {e}")
        return None

def get_item_price(data, item_id):
    """Extract buy and sell prices for an item from bazaar data"""
    if not data or "products" not in data:
        return None, None
    
    try:
        item_data = data["products"].get(item_id)
        if not item_data or "quick_status" not in item_data:
            return None, None
        
        quick_status = item_data["quick_status"]
        buy_price = quick_status.get("buyPrice", 0)
        sell_price = quick_status.get("sellPrice", 0)
        
        return buy_price, sell_price
    except KeyError as e:
        logger.error(f"Error extracting price for {item_id}: {e}")
        return None, None

def fetch_auction_data():
    """Fetch auction data from Hypixel API"""
    try:
        headers = {"API-Key": HYPIXEL_API_KEY} if HYPIXEL_API_KEY else {}
        response = requests.get(AUCTION_ENDPOINT, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching auction data: {e}")
        return None

def get_bin_price(data, item_name):
    """Extract BIN (Buy It Now) price for an item from auction data"""
    if not data or "auctions" not in data:
        return None
    
    try:
        bin_auctions = [a for a in data["auctions"] 
                      if a.get("bin", False) and item_name.lower() in a.get("item_name", "").lower()]
        
        if not bin_auctions:
            return None
        
        # Find lowest BIN price
        lowest_price = min(bin_auctions, key=lambda x: x.get("starting_bid", float("inf")))
        return lowest_price.get("starting_bid")
    except Exception as e:
        logger.error(f"Error extracting BIN price for {item_name}: {e}")
        return None
