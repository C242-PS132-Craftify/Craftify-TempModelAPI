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
## Predict API
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
## Get Project API
For get_project there is two methods to call the API which is by GET and POST. When requesting by GET we can specify the projects we want to get by parameter in the link. for example: </br>
(base_url:port/get_project/Plastic Car, Cardboard Maze). </br>
However when requesting by POST we can give it key "project_names": ["project_name1", "project_name2", etc] </br>
Sample response is shown below:
```json
{
    "data": [
        {
            "project_img": "https://storage.googleapis.com/diy-image-bucket/Plastic%20Car",
            "project_materials": [
                "1.Plastic Bottle",
                "2.Scissor",
                "3.4 Bottle caps"
            ],
            "project_name": "Plastic Car",
            "project_recipe": [
                "1.Cut a square hole using a scissor in the middle of a plastic bottle (you can draw a square first for easier cutting)",
                "2.Using the tip of a scissor, cut 4 small holes on the opposite side of the square hole for the wheels",
                "3.Insert two wooden sticks into the holes and glue 4 plastic bottle caps to the end of each sticks.",
                "4.You can decorate the plastic car by painting it or by using ice cream sticks"
            ]
        },
        {
            "project_img": "https://storage.googleapis.com/diy-image-bucket/Cardboard%20Maze",
            "project_materials": [
                "1.Cardboard",
                "2.Scissor"
            ],
            "project_name": "Cardboard Maze",
            "project_recipe": [
                "1.Get a flat cardboard sheet",
                "2.Draw the maze layout using a marker",
                "3.Cut 4 strips of cardboard and glue them to form walls on each edge of the flat cardboard sheet",
                "4.Glue plastic straws or cardboard strips along the drawn maze layout",
                "5.Use a small marble as the game piece",
                "6.Tilt the board around to navigate around the maze"
            ]
        }
    ]
}
```
