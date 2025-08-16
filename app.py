from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import eval7
from calculateOdds import calculate_hand_equity

app = Flask(__name__)
model = YOLO("weights/best.pt")

def create_class_mapping(name):
    if name[:2] == '10':
        return 'T' + name[2].lower()
    else:
        return name[0] + name[1].lower()

def calculate_odds(detected_classes):
    try:
        card1 = create_class_mapping(list(detected_classes)[0])
        card2 = create_class_mapping(list(detected_classes)[1])
        hand = [eval7.Card(card1), eval7.Card(card2)]
        equity = calculate_hand_equity(hand, num_opponents=1, simulations=1000)
        return f"Chance of winning: {equity:.2f}%"
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'frame' not in request.files:
        return jsonify({"result": "No frame received"})

    file = request.files['frame']
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    results = model(img)
    detected_classes = {model.names[int(box.cls)] for box in results[0].boxes}

    if len(detected_classes) == 2:
        overlay_text = calculate_odds(detected_classes)
    else:
        overlay_text = "Show exactly 2 cards to the camera."

    return jsonify({"result": overlay_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
