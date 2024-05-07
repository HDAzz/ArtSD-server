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