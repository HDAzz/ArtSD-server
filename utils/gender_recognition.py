import cv2
import numpy as np


def gender_recognition(picture):
    # 加载模型和权重
    genderProto = "age_gender/gender_deploy.prototxt"
    genderModel = "age_gender/gender_net.caffemodel"
    genderList = ['Male', 'Female']
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    # 读取一张人脸图片
    # image = cv2.imread(picture_path)
    data = picture.read()
    img = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(img, cv2.IMREAD_COLOR)

    # 对输入图片进行预处理
    blob = cv2.dnn.blobFromImage(image, 1, (227, 227), (78.4437, 78.4437, 78.4437, 0))
    genderNet.setInput(blob)

    # 运行模型
    genderPreds = genderNet.forward()

    # 解析模型输出
    gender = genderList[np.argmax(genderPreds)]

    # print("Gender : {}, conf = {:.3f}".format(gender, genderPreds[0].max()))
    return gender
