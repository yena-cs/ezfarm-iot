import cv2
import cvlib as cv
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import s3
import os

np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model('/home/ubuntu/tomato/model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


def image_color(name):
    if os.path.isfile('/home/ubuntu/tomato/image.jpg'):
        os.system('rm /home/ubuntu/tomato/image.jpg')
    s3.download(name)
    image_path = '/home/ubuntu/tomato/image.jpg'
    im = cv2.imread(image_path)
    bbox, label, conf = cv.detect_common_objects(im)
    if not label:
        return 0.0

    im_result = Image.open(image_path)
    crop_image = im_result.crop((bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3]))
    size = (224, 224)
    image = ImageOps.fit(crop_image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    return prediction[0][0] * 100

