from io import BytesIO
from flask import Flask, Response, jsonify, render_template, request, redirect, url_for, session
import cv2
import base64
from PIL import Image
import os
import time
import json
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = 'd7b9df1c170072ea7ff4f719ac6d9a51'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snapshots.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Snapshot Database
class Snapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Hardcoded valid login credentials
valid_username = 'jake123'
valid_password = '123'



# WEBSCRAPING ----------------------------------------------------------------------------------------------------
def fetch_tops():
    url = 'https://www.hollisterco.com/shop/wd/mens-tops'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tops = []
    
    # Fetching titles, prices, and images
    product_titles = soup.find_all('h2', {'data-aui': 'product-card-name'})
    product_prices = soup.find_all('span', {'class': 'product-price-text'})
    product_images = soup.find_all('img', {'data-aui': 'product-card-image'})
    product_links = soup.find_all('a')
    
    # Check lengths
    len_titles = len(product_titles)
    len_prices = len(product_prices)
    len_images = len(product_images)
    print(f"Titles: {len_titles}, Prices: {len_prices}, Images: {len_images}")

    counter = 0

    # Combine the lists into a single list of dictionaries
    for i in range(min(len_titles, len_prices, len_images)):

        if(i >11):
            break

        title = product_titles[i].get_text().strip()
        price = product_prices[i].get_text().strip()
        image = product_images[i]['src']
        index = 352 + counter
        link = f"https://www.hollisterco.com{product_links[index]['href']}"

        counter += 2
        
        tops.append({
            'title': title,
            'price': price,
            'image': image,
            'link': link
        })

    return tops

def fetch_bottoms():
    url = 'https://www.hollisterco.com/shop/ca/mens-bottoms'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    bottoms = []
    
    # Fetching titles, prices, and images
    product_titles = soup.find_all('h2', {'data-aui': 'product-card-name'})
    product_prices = soup.find_all('span', {'class': 'product-price-text'})
    product_images = soup.find_all('img', {'data-aui': 'product-card-image'})
    
    # Check lengths
    len_titles = len(product_titles)
    len_prices = len(product_prices)
    len_images = len(product_images)
    print(f"Titles: {len_titles}, Prices: {len_prices}, Images: {len_images}")

    # Combine the lists into a single list of dictionaries
    for i in range(min(len_titles, len_prices, len_images)):

        if(i > 11):
            break

        title = product_titles[i].get_text().strip()
        price = product_prices[i].get_text().strip()
        image = product_images[i]['src']
        
        bottoms.append({
            'title': title,
            'price': price,
            'image': image
        })

    return bottoms

@app.route('/expand')
def bottoms():
    bottoms = fetch_bottoms()
    tops = fetch_tops()
    return render_template('expand.html', bottoms=bottoms, tops=tops)



# WEBSCRAPING ----------------------------------------------------------------------------------------------------



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

    # Save image to database
    new_snapshot = Snapshot(filename=snapshot_filename, image_data=image_data)
    db.session.add(new_snapshot)
    db.session.commit()

    with open(filepath, 'wb') as f:
        f.write(image_data)

    return jsonify({'filename': snapshot_filename})

@app.route('/get_snapshots')
def get_snapshots():
    snapshots = Snapshot.query.all()
    snapshot_list = [{'id': s.id, 'filename': s.filename, 'timestamp': s.timestamp} for s in snapshots]
    return jsonify(snapshot_list)

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
    with app.app_context():
        db.create_all()
        # db.drop_all()
    app.run(debug=True)

