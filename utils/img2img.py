import base64
import configparser
import io
import numpy as np
import cv2
import requests
from PIL import Image
from service.OssService import upload_file,get_file

config = configparser.ConfigParser()
config.read('config.ini')
host = config['stable-diffusion-webui']['host']
port = config['stable-diffusion-webui']['port']
def img2img(picture_path, style):
    '''
      这个是Stable-diffusion的api接口地址
    '''
    url = "http://"+host+":"+port

    # 此处为读取一张图片作为输入图像
    # img = cv2.imread(picture_path)
    data = get_file(picture_path).read()
    image = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # 编码图像
    retval, bytes = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(bytes).decode('utf-8')

    '''
            皮卡斯风格
    '''
    picas_prompt = "teenger,(best quality:1.2),cute,looking at viewer,masterpiece,delicate face,full of youthful energy,professional,vivid colors,bright,live and beautiful eyes"
    picas_negative_prompt = "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality,blurry, ((monochrome)), ((grayscale)),skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331),(morbid:1.21), (mutilated:1.21), (tranny: 1.331), mutated hands,(poorly drawn hands: 1.5), (bad anatomy: 1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missingarms:1.331), (extra legs: 1.331), (fused fingers: 1.61051), (too many fingers: 1.61051), (easynegative:1.2), (unclear eyes: 1.331),(strange eyes:1.3),bad hands, missing fingers, extra digit, (((extraarms and legs)))"
    picas_payload = {
        # 模型设置
        "override_settings": {
            "sd_model_checkpoint": "disneyPixarCartoon_v10"
        },

        # 基本参数
        "prompt": picas_prompt,
        "negative_prompt": picas_negative_prompt,
        "steps": 30,
        "sampler_name": "Euler a",
        "width": 480,
        "height": 640,
        "batch_size": 1,
        "n_iter": 1,
        "seed": -1,
        "cfg_scale": 6.5,
        "denoising_strength": 0.3,
        "CLIP_stop_at_last_layers": 2,

        "init_images": [encoded_image],

        # 面部修复 face fix
        "restore_faces": False,

        # 高清修复 highres fix
        # "enable_hr": True,
        # "denoising_strength": 0.4,
        # "hr_scale": 2,
        # "hr_upscaler": "Latent",

    }

    '''
          动漫风格
    '''

    anime_prompt = "(best quality:1.2),looking at viewer,masterpiece,full of youthful energy,professional,bright,live and beautiful eyes"
    anime_negative_prompt = "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality,blurry, ((monochrome)), ((grayscale)),skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331),(morbid:1.21), (mutilated:1.21), (tranny: 1.331), mutated hands,(poorly drawn hands: 1.5), (bad anatomy: 1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missingarms:1.331), (extra legs: 1.331), (fused fingers: 1.61051), (too many fingers: 1.61051), (easynegative:1.2), (unclear eyes: 1.331),(strange eyes:1.3),bad hands, missing fingers, extra digit, (((extraarms and legs)))"
    anime_payload = {
        # 模型设置
        "override_settings": {
            "sd_model_checkpoint": "manmaruMix_v30"
        },

        # 基本参数
        "prompt": anime_prompt,
        "negative_prompt": anime_negative_prompt,
        "steps": 30,
        "sampler_name": "Euler a",
        "width": 480,
        "height": 640,
        "batch_size": 1,
        "n_iter": 1,
        "seed": -1,
        "cfg_scale": 8,
        "denoising_strength": 0.25,
        "CLIP_stop_at_last_layers": 2,

        "init_images": [encoded_image],

        # 面部修复 face fix
        "restore_faces": False,

        # 高清修复 highres fix
        # "enable_hr": True,
        # "denoising_strength": 0.4,
        # "hr_scale": 2,
        # "hr_upscaler": "Latent",

    }

    '''
          卡通插图风格
    '''
    illustration_prompt = "(teenger:1.5),(best quality:1.2),looking at viewer,masterpiece,full of youthful energy,professional,bright"
    illustration_negative_prompt = "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres,(beard:1.2),elder,old, normal quality,blurry, ((monochrome)), ((grayscale)),skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331),(morbid:1.21), (mutilated:1.21), (tranny: 1.331), mutated hands,(beard:1.2),(poorly drawn hands: 1.5), (bad anatomy: 1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missingarms:1.331), (extra legs: 1.331), (fused fingers: 1.61051), (too many fingers: 1.61051), (easynegative:1.2), (unclear eyes: 1.331),(strange eyes:1.3),bad hands, missing fingers, extra digit, (((extraarms and legs)))"
    illustration_payload = {
        # 模型设置
        "override_settings": {
            "sd_model_checkpoint": "pixelstyleckpt_strength07"
        },

        # 基本参数
        "prompt": illustration_prompt,
        "negative_prompt": illustration_negative_prompt,
        "steps": 30,
        "sampler_name": "Euler a",
        "width": 480,
        "height": 640,
        "batch_size": 1,
        "n_iter": 1,
        "seed": -1,
        "cfg_scale": 7.5,
        "denoising_strength": 0.4,
        "CLIP_stop_at_last_layers": 2,

        "init_images": [encoded_image],

        # 面部修复 face fix
        "restore_faces": False,

        # 高清修复 highres fix
        # "enable_hr": True,
        # "denoising_strength": 0.4,
        # "hr_scale": 2,
        # "hr_upscaler": "Latent",

    }
    '''
          真实卡通风格
    '''
    relCartoon_prompt = "(teenger:1.5),(best quality:1.2),looking at viewer,masterpiece,full of youthful energy,professional,bright"
    relCartoon_negative_prompt = "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres,(beard:1.2),elder,old, normal quality,blurry, ((monochrome)), ((grayscale)),skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331),(morbid:1.21), (mutilated:1.21), (tranny: 1.331), mutated hands,(beard:1.2),(poorly drawn hands: 1.5), (bad anatomy: 1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missingarms:1.331), (extra legs: 1.331), (fused fingers: 1.61051), (too many fingers: 1.61051), (easynegative:1.2), (unclear eyes: 1.331),(strange eyes:1.3),bad hands, missing fingers, extra digit, (((extraarms and legs)))"
    relCartoon_payload = {
        # 模型设置
        "override_settings": {
            "sd_model_checkpoint": "animics_v12"
        },

        # 基本参数
        "prompt": relCartoon_prompt,
        "negative_prompt": relCartoon_negative_prompt,
        "steps": 30,
        "sampler_name": "Euler a",
        "width": 480,
        "height": 640,
        "batch_size": 1,
        "n_iter": 1,
        "seed": -1,
        "cfg_scale": 8,
        "denoising_strength": 0.35,
        "CLIP_stop_at_last_layers": 2,

        "init_images": [encoded_image],

        # 面部修复 face fix
        "restore_faces": False,

        # 高清修复 highres fix
        # "enable_hr": True,
        # "denoising_strength": 0.4,
        # "hr_scale": 2,
        # "hr_upscaler": "Latent",

    }


    '''
          艺术油画风格
    '''
    oilPrinting_prompt = "(teenger:1.5),(best quality:1.2),looking at viewer,masterpiece,full of youthful energy,professional,bright"
    oilPrinting_negative_prompt = "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres,(beard:1.2),elder,old, normal quality,blurry, ((monochrome)), ((grayscale)),skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331),(morbid:1.21), (mutilated:1.21), (tranny: 1.331), mutated hands,(beard:1.2),(poorly drawn hands: 1.5), (bad anatomy: 1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missingarms:1.331), (extra legs: 1.331), (fused fingers: 1.61051), (too many fingers: 1.61051), (easynegative:1.2), (unclear eyes: 1.331),(strange eyes:1.3),bad hands, missing fingers, extra digit, (((extraarms and legs)))"
    oilPrinting_payload = {
        # 模型设置
        "override_settings": {
            "sd_model_checkpoint": "aniverse_v30Pruned"
        },

        # 基本参数
        "prompt": oilPrinting_prompt,
        "negative_prompt": oilPrinting_negative_prompt,
        "steps": 30,
        "sampler_name": "Euler a",
        "width": 480,
        "height": 640,
        "batch_size": 1,
        "n_iter": 1,
        "seed": -1,
        "cfg_scale": 8,
        "denoising_strength": 0.2,
        "CLIP_stop_at_last_layers": 2,

        "init_images": [encoded_image],

        # 面部修复 face fix
        "restore_faces": False,

        # 高清修复 highres fix
        # "enable_hr": True,
        # "denoising_strength": 0.4,
        # "hr_scale": 2,
        # "hr_upscaler": "Latent",

    }





    if style == 'illustration':
        payload = illustration_payload
    elif style == 'anime':
        payload = anime_payload
    elif style == 'picas':
        payload = picas_payload
    elif style == 'relCartoon':
        payload = relCartoon_payload
    elif style == 'oilPrinting':
        payload = oilPrinting_payload
    else:
        # default
        payload = anime_payload

    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    r = response.json()
    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))

    image.show()
    # image.save('./static/' + picture_path.split('/')[-1])

    return io.BytesIO(base64.b64decode(r['images'][0]))
