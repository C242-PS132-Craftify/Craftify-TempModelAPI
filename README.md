# Craftify Model API
# Installation
```bash
git clone https://github.com/C242-PS132-Craftify/Craftify-TempModelAPI.git
cd Craftify=TempModelApi
python -m venv venv
pip install -r requirements.txt
python main.py
```

# Usage
To use the prediction API, send request to the URL where the Flask API is hosted (default is localhost:5000/predict). The prediction API expects key "image" with the value of file of the image you want to predict. </br>
Sample response is as shown below
```json
{
    "data": {
        "detections": [
            {
                "box": [
                    0.30021968483924866,
                    0.0,
                    0.9802529811859131,
                    0.8942404389381409
                ],
                "class": "plastic_bottle",
                "score": 0.5186439156532288
            },
            {
                "box": [
                    0.22569210827350616,
                    0.690287172794342,
                    0.31698718667030334,
                    0.7865968346595764
                ],
                "class": "plastic_bottle",
                "score": 0.4591815173625946
            }
        ],
        "recommendations": [
            {
                "project_img": "https://storage.googleapis.com/diy-image-bucket/Bird%20Feeders%20from%20Plastic%20Bottles",
                "project_name": "Bird Feeders from Plastic Bottles"
            },
            {
                "project_img": "https://storage.googleapis.com/diy-image-bucket/Piggy%20bank%20from%20Plastic%20Bottle",
                "project_name": "Piggy bank from Plastic Bottle"
            },
            {
                "project_img": "https://storage.googleapis.com/diy-image-bucket/Plastic%20Bottle%20Terrarium",
                "project_name": "Plastic Bottle Terrarium"
            },
            {
                "project_img": "https://storage.googleapis.com/diy-image-bucket/Flower%20pot%20from%20Plastic%20Bottle",
                "project_name": "Flower pot from Plastic Bottle"
            },
            {
                "project_img": "https://storage.googleapis.com/diy-image-bucket/Hanging%20Pot%20for%20Plants",
                "project_name": "Hanging Pot for Plants"
            },
            {
                "project_img": "https://storage.googleapis.com/diy-image-bucket/Plastic%20Car",
                "project_name": "Plastic Car"
            },
            {
                "project_img": "https://storage.googleapis.com/diy-image-bucket/Decorative%20Light%20from%20Plastic%20Spoons",
                "project_name": "Decorative Light from Plastic Spoons"
            }
        ]
    }
}
```
