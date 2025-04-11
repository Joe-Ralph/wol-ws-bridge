import socketio
import subprocess

sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')
    sio.emit('identify', 'pi')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on('wake')
def on_wake(mac):
    print(f'Received WOL command for MAC: {mac}')
    try:
        subprocess.run(['wakeonlan', mac], check=True)
        print(f'WOL packet sent to {mac}')
    except subprocess.CalledProcessError as e:
        print(f'Error sending WOL: {e}')

sio.connect('https://your-cloud-relay-url')  # Replace with actual URL
sio.wait()