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
'''
新增图片
'''
def insertPictures(filename,raw_url,processed_url,styleid):
    inserted_id = collection_picture.insert_one({
        "filename":filename,
        "raw_url":raw_url,
        "processed_url":processed_url,
        "styleid":styleid,
        "created_at":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
        "updated_at":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
        "isDeleted":True
    })
    return {"id":ObjectId(inserted_id.inserted_id).__str__(),"processed_url":processed_url}
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
获取历史列表
'''
def getHistory():
    historylist = []
    query = { "isDeleted": False }
    result = collection_picture.find(query).sort("created_at", pymongo.DESCENDING)
    for i in result:
        styleid = i["styleid"]
        query = { "_id": ObjectId(styleid) }
        result = collection_style.find_one(query)
        style = result['name']
        historylist.append({"id":ObjectId(i['_id']).__str__(),
                            "raw_url":i["raw_url"],
                            "processed_url":i['processed_url'],
                            "style":style})
    return historylist
'''
获取风格列表
'''
def getStyle():
    stylelist=[]
    result = collection_style.find()
    for i in result:
        name = i['name']
        styleid = ObjectId(i['_id']).__str__()
        path = i['static_path']
        stylelist.append({'name':name,'styleid':styleid,'path':path})
    return stylelist
def addStyle(name,payload,path):
    query = {"name": name}
    result = collection_style.find_one(query)
    if result == None:
        style_id = collection_style.insert_one({
            "name": name,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "payload": payload,
            "static_path": path
        })
    else:
        new_value = {"$set": {"payload": payload, "updated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}}
        collection_picture.update_one(query, new_value)
        style_id = collection_style.find_one({"name":name})["styleid"]
    return ObjectId(style_id.inserted_id).__str__()
def getStylePromp(styleid):
    query = { "_id": ObjectId(styleid) }
    result = collection_style.find_one(query)
    return result['name']