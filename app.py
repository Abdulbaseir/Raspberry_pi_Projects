#!/usr/bin/env python3
"""RC Excavator: 6 Servos via PCA9685 + Camera Stream"""

from flask import Flask, render_template, Response, jsonify, request
from adafruit_servokit import ServoKit
import cv2
from picamera2 import Picamera2
import time
import atexit

app = Flask(__name__)

# --- PCA9685 SERVO SETUP ---
# 16 channels available, using first 6
print("Initializing PCA9685...")
kit = ServoKit(channels=16)

SERVO_NAMES = ["Left Track", "Right Track", "Cab Rotation", "Boom Lift", "Arm Lift", "Bucket"]
current_angles = [90.0] * 6

def set_servo_angle(servo_id, web_angle):
    """Move servo (0-180 degrees)"""
    web_angle = max(0, min(180, web_angle))
    current_angles[servo_id] = web_angle
    # The adafruit library takes 0-180 directly!
    kit.servo[servo_id].angle = web_angle

def cleanup():
    """Disable all servos (stops buzzing/sending signals)"""
    for i in range(6):
        kit.servo[i].angle = None
    print("Servos detached.")

atexit.register(cleanup)

# Initialize all to center
for i in range(6):
    set_servo_angle(i, 90)

# --- CAMERA SETUP (LOW CPU) ---
print("Starting camera...")
camera = Picamera2()
config = camera.create_video_configuration(main={"size": (480, 360), "format": "RGB888"})
camera.configure(config)
camera.start()
time.sleep(2)

def generate_frames():
    while True:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        time.sleep(0.08) # 12 FPS keeps network smooth

# --- ROUTES (Exact same as before, UI won't notice a difference) ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/servo/all', methods=['POST'])
def update_all_servos():
    data = request.get_json()
    angles = data.get('angles', current_angles)
    for i in range(6):
        set_servo_angle(i, angles[i])
    return jsonify({"status": "success"})

@app.route('/api/servo/center', methods=['POST'])
def center_all():
    for i in range(6):
        set_servo_angle(i, 90)
    return jsonify({"status": "success"})

@app.route('/api/servo/emergency_stop', methods=['POST'])
def e_stop():
    cleanup()
    return jsonify({"status": "stopped"})

if __name__ == '__main__':
    print("6-Servo Excavator System Ready!")
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    finally:
        cleanup()