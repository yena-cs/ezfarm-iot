import boto3
from datetime import datetime
import os


def image_file(send, farm_id):
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    if len(hour) == 1:
        hour = '0' + hour
    if len(minute) == 1:
        minute = '0' + minute
    if len(second) == 1:
        second = '0' + second

    if os.path.isfile('image.jpg'):
        os.system('rm image.jpg')
    os.system('fswebcam -r 1280x720 image.jpg')
    file_name = 'image.jpg'
    bucket_name = 'tomato-growth-images'
    realtime = farm_id+"_"+year+"-"+month+"-"+day+"["+hour+"-"+minute+"-"+second+'].jpg'
    measure_time = hour
    if send == 1:
        realtime = farm_id+"_"+"9999-99-99[99-99-99].jpg"
        measure_time = "99"
    s3 = boto3.client('s3')
    
    s3.upload_file(file_name, bucket_name, realtime)
    print(realtime + ' upload success')

    return realtime, measure_time

