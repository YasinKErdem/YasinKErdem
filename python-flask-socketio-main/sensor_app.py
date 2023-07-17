import random
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Lock
from datetime import datetime

"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():
    #print("Generating random sensor values")
    #dummy_sensor_value = round(random() * 100, 3)
    while True:
        dummy_sensor_value = ["red", "blue" , "yellow" , "white" , "orange"]
        randNumber=random.randint(0,4)
        print(randNumber)
        dummy_sensor_value = dummy_sensor_value[randNumber]
        print(dummy_sensor_value)
        #dummy_sensor_value = round(random() * 100, 3)
        socketio.emit('updateSensorData', {'value': dummy_sensor_value, "date": get_current_datetime()})
        #socketio.emit('updateSensorData' , {value : "red" , "date" : get_current_datetime()} 
        socketio.sleep(5)

"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)