import base64
import uuid
from flask import Flask, request, send_from_directory,send_file
from utils.img2img import img2img
from db import db
from service.OssService import upload_file,get_file

app = Flask(__name__)

@app.route('/generate',methods=['POST'])
def generate_img():
    img = request.files['img']
    raw_url = upload_file(img.filename,
                           img,
                           type='uploads') # '/upload/xx/xx/xx/xxxx.jpg'
    styleid = request.form.get('style')
    styleprompt = db.getStylePromp(styleid)
    new_img_data_b = img2img(raw_url,styleprompt)
    processed_url = upload_file(img.filename,
                                new_img_data_b,
                                type='productions')# '/productions/xx/xx/xx/xxxx.jpg'
    data= db.insertPictures(img.filename, raw_url,processed_url, styleid)
    return {'code':0,'msg':'ok','data':data}


# 获取风格列表
@app.route('/stylelist',methods=['GET'])
def stylelist():
    stylelist = db.getStyle()
    return {'code': 0, 'msg': 'ok', 'data': stylelist}
# 获取历史列表
@app.route('/history',methods=['GET'])
def history():
    pathlist = db.getHistory()
    return {'code': 0, 'msg': 'ok', 'data': pathlist}
# 保存图片
@app.route('/save',methods=['POST'])
def saveimg():
    inserted_id = request.form.get('id')
    db.savePicture(inserted_id)
    return {'code': 0, 'msg': 'ok', 'data': None}
@app.route('/picture',methods=['DELETE'])
def deletePicture():
    id = request.form.get('id')
    db.deletePicture(id)
    return {'code': 0, 'msg': 'ok', 'data': None}
@app.route('/style',methods=['POST'])
def addStyle():
    name = request.form.get('name')
    payload= request.form.get('payload')
    path = request.form.get('path')
    styleid = db.addStyle(name, payload,path)
    return {'code': 0, 'msg': 'ok', 'data': styleid}
@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename, cache_timeout=0)
@app.route('/minio/<path:url>')
def minio(url):
    # return base64.b64encode(get_file(url)).decode('utf-8')
    return send_file(get_file(url), mimetype='image/jpg')
app.run(port=8080, debug=True)