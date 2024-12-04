from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2
from flask_cors import CORS
import pandas as pd
from db_conn import get_data
import threading
import regex as re

model = None
detect_fn = None
model_lock = threading.Lock()

def load_model():
    global model, detect_fn
    with model_lock:
        if model is None:
            print('Loading Model........')
            model = tf.saved_model.load('model/saved_model')
            detect_fn = model.signatures['serving_default']
            
load_model()

app = Flask(__name__)
CORS(app)



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

data2 = get_data()

# data2 = pd.read_csv('jas.csv')

# def recommend_project(labels, data2):
#     if isinstance(labels, str):
#         labels = [labels]

#     mask = data2[labels].any(axis=1)
#     filtered_data = data2[mask]

#     recommendations = []
#     for _, row in filtered_data.iterrows():
#         project_recipe = row.get("project_recipe", "")
#         formatted_recipe = project_recipe.replace(". ", ".\n") if project_recipe else ""
#         recommendations.append({
#             "project_name": row["project_name"],
#             # "project_materials": row.get("project_materials", ""),
#             "project_img": row.get("project_img", ""),
#             # "project_recipe": formatted_recipe
#         })

#     return recommendations

def recommend_project(labels, data2):
    if isinstance(labels, str):
        labels = [labels]

    mask = data2[labels].any(axis=1)
    recommend = data2[mask]
    print(recommend)

    recommendations = []

    for index, row in recommend.iterrows():
        project_name = str(row["project_name"]),
        project_img = str(row["project_img"]),
        project_name_clean = re.sub(r"[(),']", '', str(project_name))
        project_img_clean = re.sub(r"[(),']", '', str(project_img))
        # print(f'Project Name: {project_name}')
        # print(f'Project IMG: {project_img}')
        recommendations.append({
            "project_name": project_name_clean,
            "project_img": project_img_clean,
        })
    return recommendations

@app.route("/get_project", methods=["POST", "GET"])
@app.route("/get_project/<project_name>", methods=["GET"])
def get_project(project_name=None):
    project_names = []
    
    if request.method == 'POST':
        project_names = request.json.get('project_names', [])
    elif request.method == 'GET':
        # project_names_str = request.args.get('project_name', '')
        # project_names = [name.strip() for name in project_names_str.split(',') if name.strip()]
        if project_name:
            project_names = [name.strip() for name in project_name.split(',') if name.strip()]
            print(f'project names: {project_names}')

    if not project_names:
        return jsonify({"error": "No project names provided"}), 400

    projects = data2[data2['project_name'].isin(project_names)]

    response_data = []
    for _, project in projects.iterrows():
        project_materials = []
        project_recipe = []
        project_recipe_raw = project.get("project_recipe", "")
        project_recipe_raw = project_recipe_raw.split("\r\n")
        project_materials_raw = project.get("project_materials", "")
        project_materials_raw = project_materials_raw.split("\r\n")
        for materials in project_materials_raw:
            if materials == "":
                continue
            else:
                project_materials.append(materials)
                
        for steps in project_recipe_raw:
            if steps == "":
                continue
            else:
                project_recipe.append(steps)
        response_data.append({
            "project_name": project["project_name"],
            "project_materials": project_materials,
            "project_img": project.get("project_img", ""),
            "project_recipe": project_recipe
        })

    response = {
        "data": response_data
    }
    
    return jsonify(response)

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]

    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    resized_image = cv2.resize(image, (320, 320))
    input_tensor = tf.convert_to_tensor([image], dtype=tf.uint8)

    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop("num_detections"))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections["num_detections"] = num_detections
    detections["detection_classes"] = detections["detection_classes"].astype(np.int64)

    detection_results = []
    detected_labels = []
    for i in range(num_detections):
        if (float(detections["detection_scores"][i]) >= 0.4) and (i < 5):
            detected_label = label_map[detections["detection_classes"][i]]
            detected_label = detected_label.lower()
            detected_label = detected_label.replace(" ", "_")
            detected_label = ("plastic_bottle" if detected_label in {"other_plastic_bottle", "clear_plastic_bottle"} else detected_label)
            detected_label = ("carton" if detected_label in {"other_carton", "corrugated_carton"} else detected_label)
            detected_labels.append(detected_label)
            detection_results.append({
                "class": detected_label,
                "score": float(detections["detection_scores"][i]),
                "box": detections["detection_boxes"][i].tolist()
            })
    print(f'detected labels: {detected_labels}')
    
    if not detection_results:
        max_score_index = np.argmax(detections['detection_scores'])
        detected_label = label_map[detections['detection_classes'][max_score_index]].lower().replace(" ", "_")
        detected_label = ("plastic_bottle" if detected_label in {"other_plastic_bottle", "clear_plastic_bottle"} else detected_label)
        detected_label = ("carton" if detected_label in {"other_carton", "corrugated_carton"} else detected_label)

        detected_labels.append(detected_label)
        detection_results.append({
            "class": detected_label,
            "score": float(detections['detection_scores'][max_score_index]),
            "box": detections['detection_boxes'][max_score_index].tolist()
        })
    if len(detected_labels) == 0:
        recommendations = []
    else:
        recommendations = recommend_project(detected_labels, data2)

    response = {
        "data": {
            "detections": detection_results,
            "recommendations": recommendations
        }
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run()
