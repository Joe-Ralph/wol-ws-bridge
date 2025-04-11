import socketio
import os
import subprocess

RELAY_SERVER = os.environ.get("RELAY_SERVER")
if not RELAY_SERVER:
    print("❌ RELAY_SERVER environment variable not set.")
    exit(1)

sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to relay server")
    sio.emit("identify", "pi")

@sio.event
def wake(mac):
    print(f"🔔 Received wake request for {mac}")
    try:
        subprocess.run(["wakeonlan", mac], check=True)
        print("✅ Wake-on-LAN packet sent")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to send WOL packet: {e}")

@sio.event
def disconnect():
    print("⚠️ Disconnected from relay server")

sio.connect(RELAY_SERVER)
sio.wait()
