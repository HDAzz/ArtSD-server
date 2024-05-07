from minio import Minio
import  io
BUCKET_NAME = 'artsd'
# 初始化minioClient, 提供访问地址， 访问账号与密码
minioClient = Minio('127.0.0.1:9000',
                    access_key='minioadmin',
                    secret_key='minioadmin',
                    secure=False)
# bucket不存时创建
found = minioClient.bucket_exists(BUCKET_NAME)
if not found:
    minioClient.make_bucket(BUCKET_NAME)
    print('created bucket')
else:
    print('bucket exists')