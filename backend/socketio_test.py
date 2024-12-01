import socketio

# Create a SocketIO client instance
sio = socketio.Client()


# Event: Handle connection to the server
@sio.event
def connect():
    print("Connected to the server!")


# Event: Handle response or acknowledgment from the server (optional)
@sio.event
def response(data):
    print("Received response from server:", data)


# Event: Handle any errors or connection issues
@sio.event
def connect_error(data):
    print("Connection failed:", data)


@sio.event
def new_message(data):
    print("Received response from server:", data)


# Set up connection with SSID cookie
cookies = {"SSID": "some_value"}
headers = {"Cookie": "SSID=some_value"}  # Add the SSID cookie here

# Connect to the Flask-SocketIO server with the cookie
sio.connect("http://127.0.0.1:5000", headers=headers)

# Emit the 'send_message' event with data and look_up
sio.emit("send_message", ("what are you?", False))

# Wait for the server's response
import time

time.sleep(2)  # Give time for server processing

input()
# Disconnect after testing
sio.disconnect()
