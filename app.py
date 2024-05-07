import uuid
from flask import Flask, request, send_from_directory
from utils.img2img import img2img
from db import db
from service.OssService import upload_file

app = Flask(__name__)

# 图生图并保存
# @app.route('/generate',methods=['POST'])
# def generate_img():
#     img = request.files['img']
#     img.filename=uuid.uuid4().hex+img.filename
#     img_path = 'uploads/' + img.filename
#     img.save(img_path)
#     styleid = request.form.get('style')
#     styleprompt = db.getStylePromp(styleid)
#     new_img = img2img(img_path,styleprompt)
#     data= db.insertPictures(img.filename, '/' + img.filename, styleid)
#     return {'code':0,'msg':'ok','data':data}
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
                                type='productions')
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
    style = request.form.get('name')
    path = request.form.get('path')
    styleid = db.addStyle(style, path)
    return {'code': 0, 'msg': 'ok', 'data': styleid}
@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename, cache_timeout=0)

app.run(port=8080, debug=True)