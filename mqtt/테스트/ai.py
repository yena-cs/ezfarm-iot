import cv2
import cvlib as cv
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

# 미리 학습된 모델 가져오기
np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model('model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


# 숙도 판별하는 함수
def image_color():
    image_path = 'C:\\Users\\ynkim\\Desktop\\tomato\\1.jpg'
    # 이미지 읽어오기
    im = cv2.imread(image_path)
    # 이미지 객체 인식
    bbox, label, conf = cv.detect_common_objects(im)
    # 이미지 열기
    print(label)
    if not label:
        return 0
    im_result = Image.open(image_path)
    # 각각의 이미지 정확도 리스트
    predict_list = []
    # 학습된 모델과 비교
    for i in range(len(label)):
        crop_image = im_result.crop((bbox[i][0], bbox[i][1], bbox[i][2], bbox[i][3]))
        size = (224, 224)
        image = ImageOps.fit(crop_image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        # 이미지 정확도 구하기
        prediction = model.predict(data)
        predict_list.append(prediction[0][0])
    # 평균 이미지 정확도 구하기
    predict = 0
    for i in range(len(predict_list)):
        predict = predict_list[i] * 100 + predict
    predict = predict / len(predict_list)
    return predict


print(image_color())

