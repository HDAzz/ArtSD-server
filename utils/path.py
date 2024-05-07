from datetime import datetime
import uuid
import os
def get_object_name(file_name):
    # 获取当前日期
    current_date = datetime.now()
    # 构建文件路径
    year = str(current_date.year)
    month = str(current_date.month)
    day = str(current_date.day)
    # 确保月份和日期的格式为两位数，例如 '01'、'02' 等
    month = month.zfill(2)
    day = day.zfill(2)
    # return os.path.join(year, month, day, uuid.uuid4().hex+file_name)
    return f'{year}/{month}/{day}/{uuid.uuid4().hex}{file_name}'