import base64
import configparser
import io
import json

import numpy as np
import cv2
import requests
from PIL import Image
from service.OssService import upload_file,get_file
from db.db import getPayload

config = configparser.ConfigParser()
config.read('config.ini')
host = config['stable-diffusion-webui']['host']
port = config['stable-diffusion-webui']['port']
def img2img(picture_path, style):
    url = "http://"+host+":"+port
    data = get_file(picture_path).read()
    image = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # 编码图像
    retval, bytes = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(bytes).decode('utf-8')

    payload = eval(getPayload(style))
    payload['init_images'].append(encoded_image)


    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    r = response.json()
    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))


    return io.BytesIO(base64.b64decode(r['images'][0]))
