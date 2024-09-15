from io import BytesIO
from flask import Flask, Response, jsonify, render_template, request, redirect, url_for, session
import cv2
import base64
from PIL import Image
import os
import time
import json

app = Flask(__name__)
app.secret_key = 'd7b9df1c170072ea7ff4f719ac6d9a51'

# Hardcoded valid login credentials
valid_username = 'jake123'
valid_password = '123'

# Video Feed Setup
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()  # Read frame from camera
        if not success:
            break
        else:
            # Convert frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Yield the frame in a format suitable for video streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Video Feed Setup

# Saving Snapshot
@app.route('/save_snapshot', methods=['POST'])
def save_snapshot():
    data = request.form['image']
    image_data = data.split(",")[1]
    image_data = base64.b64decode(image_data)

    # Generate a unique filename using the current time
    snapshot_filename = 'snapshot_{}.png'.format(int(time.time()))
    filepath = os.path.join('static', 'snapshots', snapshot_filename)

    with open(filepath, 'wb') as f:
        f.write(image_data)

    return jsonify({'filename': snapshot_filename})
# Saving Snapshot

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == valid_username and password == valid_password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/wardrobe')
def wardrobe():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('wardrobe.html')

@app.route('/outfits')
def outfits():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('outfits.html')

@app.route('/expand')
def expand():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('expand.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)



