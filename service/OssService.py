import configparser
from minio import Minio
from utils.path import get_object_name

config = configparser.ConfigParser()
config.read('config.ini')

BUCKET_NAME = config['minio']['bucket_name']
minioClient = Minio(config['minio']['host']+':'+config['minio']['port'],
                    config['minio']['access_key'],
                    config['minio']['secret_key'],
                    secure=False)
found = minioClient.bucket_exists(BUCKET_NAME)# bucket不存在时创建
if not found:
    minioClient.make_bucket(BUCKET_NAME)
    print('created bucket '+BUCKET_NAME)
else:
    print('bucket '+BUCKET_NAME+' exists')

def upload_file(file_name,image_data,type):
    if type == 'uploads':
        object_name = '/uploads/'+get_object_name(file_name)
    if type == 'productions':
        object_name = '/productions/' + get_object_name(file_name)
    minioClient.put_object(bucket_name=BUCKET_NAME,
                           object_name=object_name,
                           data=image_data,
                           length=-1,
                           part_size=10*1024*1024)

    return object_name
def get_file(file_url):
     return minioClient.get_object(BUCKET_NAME, file_url)
