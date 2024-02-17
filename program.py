import os
import time
import requests
import logging

pushgateway_url = os.getenv('PUSHGATEWAY_URL')
exporter_url = os.getenv('EXPORTER_URL')
interval = int(os.getenv('INTERVAL'))
log_level = os.getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

while True:
    try:
        response = requests.get(exporter_url)
        metrics = response.text
        response = requests.put(pushgateway_url, data=metrics)
        
        if response.status_code == 202:
            logger.info(f"Metrics successfully pushed to Pushgateway at {pushgateway_url}")
        else:
            logger.error(f"Failed to push metrics to Pushgateway. Status code: {response.status_code}")
        
    except Exception as e:
        logger.exception(f"Error: {e}")
    
    time.sleep(interval)