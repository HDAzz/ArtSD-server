import configparser
import time

from flask import Flask, request, send_from_directory,send_file
from utils.img2img import img2img
from utils.response import success,error
from db import db
from service.OssService import upload_file,get_file
from flask_cors import CORS
from utils.gender_recognition import gender_recognition
import re

config = configparser.ConfigParser()
config.read('config.ini')
app = Flask(__name__)
CORS(app)

@app.before_request
def before():
    # app.logger.info('【请求方法】{}【请求路径】{}【请求设备】{}【请求参数】{}【请求地址】{}'.format(request.method, request.path,request.headers['Sn'],dict(request.form),request.remote_addr))
    url = request.path
    passUrl = ['/sex','/style']
    pattern = r'^/minio/.+'
    if url in passUrl:
        pass
    elif re.match(pattern, url):
        # 如果是请求静态文件的路由，则不进行拦截
        pass
    else:
        sn = request.headers.get('Sn')
        if sn is None or db.checkDevice(sn) is False:
            return error('40000', 'Sn is not exist or the device is banned')
@app.route('/generate',methods=['POST'])
def generate_img():
    calling_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 获取接口调用的时间
    sn = request.headers.get('Sn') # 获取设备号
    img = request.files['img'] # 获取原始图片
    raw_url = upload_file(img.filename,
                           img,
                           type='uploads') # '/upload/xx/xx/xx/xxxx.jpg'
    styleid = request.form.get('style')

    background = True if (request.form.get('background')=='true' or request.form.get('background')=='True')else False
    # print(background)
    styleprompt = db.getStylePromp(styleid)
    new_img_data_b,begin_at,end_at = img2img(raw_url,styleprompt,background)
    processed_url = upload_file(img.filename,
                                new_img_data_b,
                                type='productions')# '/productions/xx/xx/xx/xxxx.jpg'
    data= db.insertPictures(img.filename, raw_url,processed_url, styleid,sn,calling_at,begin_at,end_at)
    return success(data)
@app.route('/sex',methods=['POST'])
def get_sex():
    img = request.files['img']
    gender = gender_recognition(img)
    return success(gender)
# 获取风格列表
@app.route('/stylelist',methods=['POST'])
def stylelist():
    sex = request.form.get('sex')
    stylelist = db.getStyle(sex)
    return success(stylelist)
# 获取历史列表
@app.route('/history',methods=['GET'])
def history():
    sn = request.headers.get('Sn')
    # 获取分页参数
    page = int(request.form.get('page'))
    page_size = int(request.form.get('page_size'))


    pathlist,total_documents,total_pages = db.getHistory(sn,page,page_size)
    return success({
        'pathlist':pathlist,
        'page':page,
        'page_size':page_size,
        'total_documents':total_documents,
        'total_pages':total_pages
    })
# 保存图片
@app.route('/save',methods=['POST'])
def saveimg():
    inserted_id = request.form.get('id')
    db.savePicture(inserted_id)
    return success(None)
@app.route('/picture',methods=['DELETE'])
def deletePicture():
    id = request.form.get('id')
    db.deletePicture(id)
    return success(None)
@app.route('/style',methods=['POST'])
def addStyle():
    name = request.form.get('name')
    payload= request.form.get('payload')
    path = request.form.get('path')
    styleid = db.addStyle(name, payload,path)
    return success(styleid)
@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename, cache_timeout=0)
@app.route('/minio/<path:url>')
def minio(url):

    return send_file(get_file(url), mimetype='image/jpg')
if __name__ == '__main__':
    app.run(host=config['flask']['host'],port=int(config['flask']['port']), debug=True)