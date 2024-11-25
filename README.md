# How to Set Up

## Installation
```bash
git clone https://github.com/C242-PS132-Craftify/Craftify-TempModelAPI.git
cd Craftify-TempModelAPI
python -m venv venv
pip install -r requirements.txt
python main.py
```

## Usage
Send POST request to /predict with the key: 'image' with the type as File. <br>
CURL example
```bash
CURL -X POST -F "image:@path/to/image.jpg" adress:port/predict
```

## Example Response
```json
[
    {
        "box": [
            0.10138887166976929,
            0.3802175521850586,
            0.9693744778633118,
            0.699131965637207
        ],
        "class": "Clear plastic bottle",
        "score": 0.8991949558258057
    },
    {
        "box": [
            0.10201099514961243,
            0.5088871717453003,
            0.15592584013938904,
            0.6247860193252563
        ],
        "class": "Plastic bottle cap",
        "score": 0.7119922041893005
    }
]
```
