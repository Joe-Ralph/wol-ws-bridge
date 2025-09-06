import os
import time
import requests
import subprocess
import logging
from logging.handlers import RotatingFileHandler

# Set up logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_dir = os.path.expanduser('~/.local/share/pi-wol-client')
log_file = os.path.join(log_dir, 'pi-wol-client.log')

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Set up rotating file handler
file_handler = RotatingFileHandler(
    log_file, 
    maxBytes=5*1024*1024,  # 5MB
    backupCount=5,         # Keep 5 backup files
    encoding='utf-8'
)
file_handler.setFormatter(log_formatter)

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Also log to console when running interactively
if os.isatty(0):  # If running in a terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

RELAY_ENDPOINT = os.environ.get("RELAY_ENDPOINT")  # e.g. https://my-app.onrender.com/wake-request
if not RELAY_ENDPOINT:
    logger.error("RELAY_ENDPOINT environment variable not set.")
    exit(1)

def send_wol(mac):
    try:
        subprocess.run(["wakeonlan", mac], check=True)
        logger.error(f"Wake-on-LAN packet sent to {mac}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to send WOL packet: {e}")

while True:
    try:
        resp = requests.get(RELAY_ENDPOINT, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("wake"):
                mac = data["mac"]
                logger.error(f"Received WOL request for {mac}")
                send_wol(mac)
            else:
                logger.error("No wake request at this time")
        else:
            logger.error(f"Server error: {resp.status_code}")
    except Exception as e:
        logger.error(f"Error contacting server: {e}")

    time.sleep(5)  # Poll every 5 seconds (tune as needed)

