import time
import logging
import schedule
from datetime import datetime

from config import MONITORED_ITEMS, CHECK_INTERVAL, SHOW_THRESHOLD_MESSAGES
from hypixel_api import fetch_bazaar_data, get_item_price, fetch_auction_data, get_bin_price
from telegram_bot import send_telegram_notification, test_telegram_connection

# Fix the logging format
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hypixel_price_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("price_monitor")

# Store the last notification time for each item to prevent spam
last_notification = {}

def check_prices():
    """Check prices for all monitored items and send notifications if thresholds are crossed"""
    logger.info("Checking prices...")
    
    bazaar_data = fetch_bazaar_data()
    auction_data = None  # Only fetch auction data if needed
    
    if not bazaar_data:
        logger.error("Failed to fetch bazaar data")
        return
    
    current_time = datetime.now()
    
    for item_id, config in MONITORED_ITEMS.items():
        item_name = config["name"]
        high_threshold = config["high_threshold"]
        low_threshold = config["low_threshold"]
        
        # First try bazaar
        buy_price, sell_price = get_item_price(bazaar_data, item_id)
        
        # If not available in bazaar, try auction house
        if buy_price is None and sell_price is None:
            # Auction house logic remains unchanged
            if auction_data is None:
                auction_data = fetch_auction_data()
                if not auction_data:
                    logger.error("Failed to fetch auction data")
                    continue
            
            bin_price = get_bin_price(auction_data, item_name)
            if bin_price:
                logger.info(f"{item_name}: BIN Price = {bin_price}")
                
                # For auction house, treat BIN price as both buy and sell price for threshold checks
                # Check if BIN price crossed high threshold (selling opportunity)
                if bin_price > high_threshold:
                    last_notif = last_notification.get(f"{item_id}_high")
                    if not last_notif or (current_time - last_notif).total_seconds() > 3600:
                        message = f"🚨 <b>HIGH BIN PRICE ALERT - SELL OPPORTUNITY</b> 🚨\n\n" \
                                f"Item: <b>{item_name}</b>\n" \
                                f"BIN Price: <b>{bin_price:.2f}</b> coins\n" \
                                f"High Threshold: {high_threshold} coins\n\n" \
                                f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                        
                        if send_telegram_notification(message):
                            last_notification[f"{item_id}_high"] = current_time
                
                # Check if BIN price crossed low threshold (buying opportunity)
                if bin_price < low_threshold:
                    last_notif = last_notification.get(f"{item_id}_low")
                    if not last_notif or (current_time - last_notif).total_seconds() > 3600:
                        message = f"💰 <b>LOW BIN PRICE ALERT - BUY OPPORTUNITY</b> 💰\n\n" \
                                f"Item: <b>{item_name}</b>\n" \
                                f"BIN Price: <b>{bin_price:.2f}</b> coins\n" \
                                f"Low Threshold: {low_threshold} coins\n\n" \
                                f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                        
                        if send_telegram_notification(message):
                            last_notification[f"{item_id}_low"] = current_time
                else:
                    # Only log threshold messages if enabled in config
                    if SHOW_THRESHOLD_MESSAGES:
                        logger.info(f"{item_name}: BIN Price {bin_price:.2f} is within thresholds ({low_threshold:.2f} - {high_threshold:.2f})")
            else:
                logger.warning(f"Could not retrieve prices for {item_name} ({item_id})")
            continue
        
        logger.info(f"{item_name}: Bazaar Buy = {buy_price}, Sell = {sell_price}")
        
        # ===== HIGH PRICE SCENARIOS =====
        
        # Scenario 1: Sell price exceeds high threshold (best case)
        if sell_price > high_threshold:
            last_notif = last_notification.get(f"{item_id}_high_sell")
            if not last_notif or (current_time - last_notif).total_seconds() > 3600:
                message = f"🚨 <b>HIGH SELL PRICE ALERT - PRIME SELL OPPORTUNITY</b> 🚨\n\n" \
                          f"Item: <b>{item_name}</b>\n" \
                          f"Sell Price (Instant): <b>{sell_price:.2f}</b> coins\n" \
                          f"Buy Price (Sell Offer): <b>{buy_price:.2f}</b> coins\n" \
                          f"High Threshold: {high_threshold} coins\n\n" \
                          f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                
                if send_telegram_notification(message):
                    last_notification[f"{item_id}_high_sell"] = current_time
        
        # Scenario 2: Buy price (sell offer) exceeds high threshold but sell price doesn't
        elif buy_price > high_threshold:
            last_notif = last_notification.get(f"{item_id}_high_buy")
            if not last_notif or (current_time - last_notif).total_seconds() > 3600:
                message = f"📈 <b>HIGH BUY PRICE ALERT - POTENTIAL SELL OPPORTUNITY</b> 📈\n\n" \
                          f"Item: <b>{item_name}</b>\n" \
                          f"Buy Price (Sell Offer): <b>{buy_price:.2f}</b> coins\n" \
                          f"Sell Price (Instant): <b>{sell_price:.2f}</b> coins\n" \
                          f"High Threshold: {high_threshold} coins\n\n" \
                          f"Consider placing a sell offer instead of selling instantly\n\n" \
                          f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                
                if send_telegram_notification(message):
                    last_notification[f"{item_id}_high_buy"] = current_time
        elif SHOW_THRESHOLD_MESSAGES:
            logger.info(f"{item_name}: Both prices below high threshold, Buy={buy_price:.2f}, Sell={sell_price:.2f}, Threshold={high_threshold:.2f}")
            
        # ===== LOW PRICE SCENARIOS =====
        
        # Scenario 3: Buy price falls below low threshold (best case)
        if buy_price < low_threshold:
            last_notif = last_notification.get(f"{item_id}_low_buy")
            if not last_notif or (current_time - last_notif).total_seconds() > 3600:
                message = f"💰 <b>LOW BUY PRICE ALERT - PRIME BUY OPPORTUNITY</b> 💰\n\n" \
                          f"Item: <b>{item_name}</b>\n" \
                          f"Buy Price (Instant): <b>{buy_price:.2f}</b> coins\n" \
                          f"Sell Price (Buy Order): <b>{sell_price:.2f}</b> coins\n" \
                          f"Low Threshold: {low_threshold} coins\n\n" \
                          f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                
                if send_telegram_notification(message):
                    last_notification[f"{item_id}_low_buy"] = current_time
        
        # Scenario 4: Sell price (buy order) falls below low threshold but buy price doesn't
        elif sell_price < low_threshold:
            last_notif = last_notification.get(f"{item_id}_low_sell")
            if not last_notif or (current_time - last_notif).total_seconds() > 3600:
                message = f"📉 <b>LOW SELL PRICE ALERT - POTENTIAL BUY OPPORTUNITY</b> 📉\n\n" \
                          f"Item: <b>{item_name}</b>\n" \
                          f"Sell Price (Buy Order): <b>{sell_price:.2f}</b> coins\n" \
                          f"Buy Price (Instant): <b>{buy_price:.2f}</b> coins\n" \
                          f"Low Threshold: {low_threshold} coins\n\n" \
                          f"Consider placing a buy order instead of buying instantly\n\n" \
                          f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                
                if send_telegram_notification(message):
                    last_notification[f"{item_id}_low_sell"] = current_time
        elif SHOW_THRESHOLD_MESSAGES:
            logger.info(f"{item_name}: Both prices above low threshold, Buy={buy_price:.2f}, Sell={sell_price:.2f}, Threshold={low_threshold:.2f}")

def main():
    """Main function to run the price monitor"""
    logger.info("Starting Hypixel Price Monitor...")
    
    # Test Telegram connection
    if test_telegram_connection():
        logger.info("Telegram connection successful")
    else:
        logger.error("Failed to connect to Telegram. Check your bot token and chat ID.")
        return
    
    # Run initial check
    check_prices()
    
    # Schedule regular checks
    schedule.every(CHECK_INTERVAL).seconds.do(check_prices)
    
    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping Hypixel Price Monitor...")
        send_telegram_notification("Hypixel Price Monitor has been stopped.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        send_telegram_notification(f"⚠️ Error: The price monitor encountered an error: {e}")

if __name__ == "__main__":
    main()
