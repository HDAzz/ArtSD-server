import base64
import configparser
import io
import json
import time

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
def img2img(picture_path, style,background):
    url = "http://"+host+":"+port
    data = get_file(picture_path).read()
    image = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # 编码图像
    retval, bytes = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(bytes).decode('utf-8')

    payload = eval(getPayload(style))
    payload['init_images'].append(encoded_image)

    begin_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 开始生成时间
    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    end_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 结束生成时间
    r = response.json()
    if(background):
        temp_img = r['images'][0]
        conf={
            'input_image':temp_img,
            'model':'u2net',
        }
        temp_response = requests.post(url=f'{url}/rembg',json=conf)
        temp_r = temp_response.json()
        image = Image.open(io.BytesIO(base64.b64decode(temp_r['image'])))
        return io.BytesIO(base64.b64decode(temp_r['image'])),begin_at,end_at
    else:
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
        return io.BytesIO(base64.b64decode(r['images'][0])),begin_at,end_at
