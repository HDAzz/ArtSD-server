import configparser
from minio import Minio
import  io
config = configparser.ConfigParser()
config.read('../config.ini')

BUCKET_NAME = config['minio']['bucket_name']
minioClient = Minio(config['minio']['host']+':'+config['minio']['port'],
                    config['minio']['access_key'],
                    config['minio']['secret_key'],
                    secure=False)
# bucket不存时创建
found = minioClient.bucket_exists(BUCKET_NAME)
if not found:
    minioClient.make_bucket(BUCKET_NAME)
    print('created bucket '+BUCKET_NAME)
else:
    print('bucket '+BUCKET_NAME+' exists')
# 创建文件， 直接提供内容。 若从文件路径上传，使用fput_object
name = u'art-001'
content = u'this the content body'
put_result = minioClient.put_object(BUCKET_NAME, name, io.BytesIO(content.encode()), len(content), 'text/plain')
print(put_result)

# 读取内容
try:
    get_response = minioClient.get_object(BUCKET_NAME, name)
    #print(get_response.getheaders())
    print(get_response.read())
finally:
    get_response.close()
    get_response.release_conn()