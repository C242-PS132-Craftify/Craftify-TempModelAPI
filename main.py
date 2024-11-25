from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2

app = Flask(__name__)

model = tf.saved_model.load("model/saved_model")
detect_fn = model.signatures["serving_default"]

def load_label_map(label_map_path):
    with open(label_map_path, 'r') as f:
        label_map = {}
        id = None
        name = None

        for line in f:
            line = line.strip()
            if line.startswith("id:"):
                id = int(line.split(":")[1].strip())
            elif line.startswith("name:"):
                name = line.split(":")[1].strip().strip('"')
            
            if id is not None and name is not None:
                label_map[id] = name
                id = None
                name = None
                
        return label_map

label_map = load_label_map("model/label_map.pbtxt")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    resized_image = cv2.resize(image, (320, 320))
    
    input_tensor = tf.convert_to_tensor([resized_image], dtype=tf.uint8)

    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop("num_detections"))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections["num_detections"] = num_detections
    detections["detection_classes"] = detections["detection_classes"].astype(np.int64)

    detection_results = []
    for i in range(num_detections):
        if (float(detections["detection_scores"][i]) >= 0.4) and (i < 5):
            detection_results.append({
                "class": label_map[detections["detection_classes"][i]],
                "score": float(detections["detection_scores"][i]),
                "box": detections["detection_boxes"][i].tolist()
            })

    return jsonify(detection_results)

if __name__ == "__main__":
    app.run()
