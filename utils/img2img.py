import json
import requests
import io
import base64
from PIL import Image
import cv2


def img2img(picture_path, style):
    '''
      这个是Stable-diffusion的api接口地址
    '''
    url = "http://127.0.0.1:7860"

    # 此处为读取一张图片作为输入图像
    img = cv2.imread(picture_path)
    # 编码图像
    retval, bytes = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(bytes).decode('utf-8')

    '''
            皮卡斯风格
    '''
    picas_prompt = "(best quality:1.2),cute,looking at viewer,masterpiece,delicate face,full of youthful energy,professional,vivid colors,bright,live and beautiful eyes"
    picas_negative_prompt = "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality,blurry, ((monochrome)), ((grayscale)),skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331),(morbid:1.21), (mutilated:1.21), (tranny: 1.331), mutated hands,(poorly drawn hands: 1.5), (bad anatomy: 1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missingarms:1.331), (extra legs: 1.331), (fused fingers: 1.61051), (too many fingers: 1.61051), (easynegative:1.2), (unclear eyes: 1.331),(strange eyes:1.3),bad hands, missing fingers, extra digit, (((extraarms and legs)))"
    picas_payload = {
        # 模型设置
        "override_settings": {
            "sd_model_checkpoint": "disneyPixarCartoon"
        },

        # 基本参数
        "prompt": picas_prompt,
        "negative_prompt": picas_negative_prompt,
        "steps": 30,
        "sampler_name": "Euler a",
        "width": 512,
        "height": 512,
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
          日系动漫风格
    '''

    anime_prompt = "(best quality:1.2),looking at viewer,masterpiece,full of youthful energy,professional,bright,live and beautiful eyes"
    anime_negative_prompt = "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality,blurry, ((monochrome)), ((grayscale)),skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331),(morbid:1.21), (mutilated:1.21), (tranny: 1.331), mutated hands,(poorly drawn hands: 1.5), (bad anatomy: 1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missingarms:1.331), (extra legs: 1.331), (fused fingers: 1.61051), (too many fingers: 1.61051), (easynegative:1.2), (unclear eyes: 1.331),(strange eyes:1.3),bad hands, missing fingers, extra digit, (((extraarms and legs)))"
    anime_payload = {
        # 模型设置
        "override_settings": {
            "sd_model_checkpoint": "manmaruMix"
        },

        # 基本参数
        "prompt": anime_prompt,
        "negative_prompt": anime_negative_prompt,
        "steps": 30,
        "sampler_name": "Euler a",
        "width": 512,
        "height": 512,
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
          漫画小说插图风格
    '''
    illustration_prompt = "(best quality:1.2),looking at viewer,masterpiece,full of youthful energy,professional,bright"
    illustration_negative_prompt = "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality,blurry, ((monochrome)), ((grayscale)),skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331),(morbid:1.21), (mutilated:1.21), (tranny: 1.331), mutated hands,(beard:1.2),(poorly drawn hands: 1.5), (bad anatomy: 1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missingarms:1.331), (extra legs: 1.331), (fused fingers: 1.61051), (too many fingers: 1.61051), (easynegative:1.2), (unclear eyes: 1.331),(strange eyes:1.3),bad hands, missing fingers, extra digit, (((extraarms and legs)))"
    illustration_payload = {
        # 模型设置
        "override_settings": {
            "sd_model_checkpoint": "pixelstyleckpt"
        },

        # 基本参数
        "prompt": illustration_prompt,
        "negative_prompt": illustration_negative_prompt,
        "steps": 30,
        "sampler_name": "Euler a",
        "width": 512,
        "height": 512,
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

    if style == 'illustration':
        payload = illustration_payload
    elif style == 'anime':
        payload = anime_payload
    elif style == 'picas':
        payload = picas_payload
    else:
        # default
        payload = picas_payload

    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    r = response.json()
    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))

    image.show()
    image.save('./static/' + picture_path.split('/')[-1])



