import subprocess
import socketio

# Create a SocketIO client
sio = socketio.Client()

# Define the server URL
server_url = 'http://api-hkiot.kazuyosan.my.id:8081'

# Global variable to store the process
process = None

# Function to run the target script
def run_target_script():
    global process
    script_path = 'main.py'
    process = subprocess.Popen(['python', script_path])

# Function to terminate the target script
def terminate_target_script():
    global process
    if process is not None and process.poll() is None:
        process.terminate()

# SocketIO event handler for receiving data
@sio.on('trigger_ai')
def on_message(data):

    # Check the condition to run or terminate the script
    if 'status' in data:
        if data['status'] == True:
            run_target_script()
        elif data['status'] == False:
            terminate_target_script()

# Connect to the SocketIO server
sio.connect(server_url)

# Run the SocketIO event loop
sio.wait()
