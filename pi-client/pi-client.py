import os
import time
import requests
import subprocess

RELAY_ENDPOINT = os.environ.get("RELAY_ENDPOINT")  # e.g. https://my-app.onrender.com/wake-request
if not RELAY_ENDPOINT:
    print("❌ RELAY_ENDPOINT environment variable not set.")
    exit(1)

def send_wol(mac):
    try:
        subprocess.run(["wakeonlan", mac], check=True)
        print(f"✅ Wake-on-LAN packet sent to {mac}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to send WOL packet: {e}")

while True:
    try:
        resp = requests.get(RELAY_ENDPOINT, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("wake"):
                mac = data["mac"]
                print(f"🔔 Received WOL request for {mac}")
                send_wol(mac)
            else:
                print("⏳ No wake request at this time")
        else:
            print(f"⚠️ Server error: {resp.status_code}")
    except Exception as e:
        print(f"⚠️ Error contacting server: {e}")

    time.sleep(5)  # Poll every 5 seconds (tune as needed)

