import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hypixel_price_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("telegram_bot")

def send_telegram_notification(message):
    """Send a notification message to Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Telegram Bot Token or Chat ID not set")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info("Telegram notification sent successfully")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending Telegram notification: {e}")
        return False

def test_telegram_connection():
    """Test the connection to the Telegram API"""
    return send_telegram_notification("Hypixel Price Monitor is now running!")
