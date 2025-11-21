
#!/usr/bin/env python3
import os
import time
import logging

# Setup logging yang proper, anjing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 STARTING TELEGRAM BOT ON RAILWAYS")
    
    # Test environment variables, bangsat
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone = os.getenv('PHONE_NUMBER')
    
    logger.info(f"📋 ENV VARS - API_ID: {api_id}, API_HASH: {api_hash}, PHONE: {phone}")
    
    if not api_id or not api_hash:
        logger.error("❌ MISSING API_ID or API_HASH!")
        return
    
    logger.info("✅ ENVIRONMENT VARIABLES LOADED SUCCESSFULLY")
    
    # Test basic functionality, sialan
    counter = 0
    while True:
        logger.info(f"💓 BOT IS ALIVE - COUNTER: {counter}")
        counter += 1
        time.sleep(30)  # Log every 30 seconds

if __name__ == "__main__":
    main()
