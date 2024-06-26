import time
import pymongo
from bson.objectid import ObjectId
import configparser
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db=client["ArtSD"]
config = configparser.ConfigParser()
config.read('config.ini')
uri = config['mongodb']['ConnectionString']

db = pymongo.MongoClient(uri)
collection_picture=db.get_database().get_collection('picture')
collection_style=db.get_database().get_collection('style')
collection_device=db.get_database().get_collection('device')
collection_behavior=db.get_database().get_collection('behavior')
'''
新增图片
'''
def insertPictures(filename,raw_url,processed_url,styleid,sn,calling_at,begin_at,end_at,background):
    if filename is None:
        query={'raw_url':raw_url}
        filename=collection_picture.find_one(query)['filename']
    inserted_id = collection_picture.insert_one({
        "filename":filename,
        "raw_url":raw_url,
        "processed_url":processed_url,
        "styleid":styleid,
        "calling_at":calling_at,
        "begin_at":begin_at,
        "end_at":end_at,
        "isDeleted":True,
        "sn":sn,
        "background":background # 是否删除背景 true为删除 false不删除
    })
    return {"id":ObjectId(inserted_id.inserted_id).__str__(),"raw_url":raw_url,"processed_url":processed_url}
'''
保存图片
'''
def savePicture(inserted_id):
    query = { "_id": ObjectId(inserted_id) }
    new_value ={"$set":{"isDeleted":False,"updated_at":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) }}
    print(collection_picture.find_one(query))
    collection_picture.update_one(query, new_value)
'''
删除图片(软删除)
'''
def deletePicture(inserted_id):
    query = { "_id": ObjectId(inserted_id) }
    new_value = {"$set": {"isDeleted": True, "updated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}}
    print(collection_picture.find_one(query))
    collection_picture.update_one(query, new_value)
'''
获取历史列表 （分页获取）
'''
def getHistory(sn,page,page_size):
    skip = (page - 1) * page_size
    historylist = []
    query = { "isDeleted": False,"sn":sn }
    result = collection_picture.find(query).sort("calling_at", pymongo.DESCENDING).skip(skip).limit(page_size)
    for i in result:
        styleid = i["styleid"]
        query = { "_id": ObjectId(styleid) }
        result = collection_style.find_one(query)
        style = result['name']
        historylist.append({"id":ObjectId(i['_id']).__str__(),
                            "raw_url":i["raw_url"],
                            "processed_url":i['processed_url'],
                            "static":style})
    total_documents=collection_picture.count_documents({ "isDeleted": False,"sn":sn })
    print(total_documents)
    total_pages = (total_documents + page_size -1) // page_size
    return historylist,total_documents,total_pages
'''
获取风格列表
'''
def getStyle(sex):
    sex_dict = {"0":'man',
                "1":'woman'}

    stylelist=[]
    result = collection_style.find()
    for i in result:
        nickname = i['nickname']
        styleid = ObjectId(i['_id']).__str__()
        path = i['static_path']
        stylelist.append({'nickname':nickname,'styleid':styleid,'path':f"/{path.split('/')[1]}/{sex_dict[sex]}/{path.split('/')[2]}"})
    return stylelist
def addStyle(name,payload,path):
    query = {"name": name}
    result = collection_style.find_one(query)
    print(result)
    if result == None:
        collection_style.insert_one({
            "name": name,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "payload": payload,
            "static_path": path
        })
    else:
        new_value = {"$set": {"payload": payload, "updated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}}
        collection_style.update_one(query, new_value)
    style_id = collection_style.find_one({"name": name})["_id"]
    return ObjectId(style_id).__str__()
def getStylePromp(styleid):
    query = { "_id": ObjectId(styleid) }
    result = collection_style.find_one(query)
    return result['name']
def getPayload(name):
    query = {"name": name}
    result = collection_style.find_one(query)
    return result['payload']
def checkDevice(sn):
    device = collection_device.find_one({'Sn': sn})
    if not device:
        return False
    elif device['isBanned']==True:
        return False
    return True
def getFilename(raw_url):
    query = {"raw_url":raw_url}
    result = collection_picture.find_one(query)
    return result['filename']
'''
插入一条行为记录
1首次生成 
2某个风格首次生成 
3某个风格非首次生成 
4保存
'''
def insertBehavior(sn,btype,gen_id):
    query = {"_id": ObjectId(gen_id)}
    styleid = collection_picture.find_one(query)['styleid']
    inserted_id = collection_behavior.insert_one({
        "sn":sn,
        "btype":btype,
        "happen_at":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "gen_id":gen_id,
        'styleid':styleid
    })

'''
判断是否是首次生成
'''
def isFirstGeneration(sn):
    return collection_behavior.count_documents({"sn":sn})
'''
判断是否是某个风格的首次生成
'''
def isFirstGenerationWithStyle(sn,style):
    return collection_behavior.count_documents({"sn":sn,"styleid":style})