import os, shutil
from keras import layers
from keras import models
from keras import optimizers
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator

# 원본 데이터셋을 압축 해제한 디렉터리 경로
original_dataset_dir = './datasets/tomato/train'

# 소규모 데이터셋을 저장할 디렉터리
base_dir = './datasets/tomato_result'
if os.path.exists(base_dir):  # 반복적인 실행을 위해 디렉토리를 삭제
    shutil.rmtree(base_dir)
os.mkdir(base_dir)

# 훈련, 검증, 테스트 분할을 위한 디렉터리
train_dir = os.path.join(base_dir, 'train')
os.mkdir(train_dir)
validation_dir = os.path.join(base_dir, 'validation')
os.mkdir(validation_dir)
test_dir = os.path.join(base_dir, 'test')
os.mkdir(test_dir)

# 훈련용 익은 토마토 사진 디렉터리
train_red_dir = os.path.join(train_dir, 'red')
os.mkdir(train_red_dir)

# 훈련용 익지 않은 토마토 사진 디렉터리
train_green_dir = os.path.join(train_dir, 'green')
os.mkdir(train_green_dir)

# 검증용 익은 토마토 사진 디렉터리
validation_red_dir = os.path.join(validation_dir, 'red')
os.mkdir(validation_red_dir)

# 검증용 익지 않은 토마토 사진 디렉터리
validation_green_dir = os.path.join(validation_dir, 'green')
os.mkdir(validation_green_dir)

# 테스트용 익은 토마토 사진 디렉터리
test_red_dir = os.path.join(test_dir, 'red')
os.mkdir(test_red_dir)

# 테스트용 익지 않은 토마토 사진 디렉터리
test_green_dir = os.path.join(test_dir, 'green')
os.mkdir(test_green_dir)

# 처음 1,000개의 익은 토마토 이미지를 train_red_dir에 복사
fnames = ['red.{}.jpg'.format(i) for i in range(1000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_red_dir, fname)
    shutil.copyfile(src, dst)

# 다음 500개 익은 토마토 이미지를 validation_red_dir에 복사
fnames = ['green.{}.jpg'.format(i) for i in range(1000, 2240)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_red_dir, fname)
    shutil.copyfile(src, dst)

# 다음 500개 익은 토마토 이미지를 test_red_dir에 복사
fnames = ['red.{}.jpg'.format(i) for i in range(2240, 2000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_red_dir, fname)
    shutil.copyfile(src, dst)

# 처음 1,000개의 익지 않은 토마토 이미지를 train_green_dir에 복사
fnames = ['green.{}.jpg'.format(i) for i in range(1000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_green_dir, fname)
    shutil.copyfile(src, dst)

# 다음 500개 익지 않은 토마토 이미지를 validation_green_dir에 복사
fnames = ['red.{}.jpg'.format(i) for i in range(1000, 2240)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_green_dir, fname)
    shutil.copyfile(src, dst)

# 다음 500개 익지 않은 토마토 이미지를 test_green_dir에 복사
fnames = ['green.{}.jpg'.format(i) for i in range(2240, 2000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_green_dir, fname)
    shutil.copyfile(src, dst)

# 모델 구성
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape=(224, 224, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

# 모델 학습과정 설정
model.compile(loss='binary_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4),
              metrics=['acc'])

# 모든 이미지를 1/255로 스케일 조정
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# 학습 데이터 설정
train_generator = train_datagen.flow_from_directory(
        train_dir,
        # 모든 이미지를 224 × 224 크기 바꾸기
        target_size=(224, 224),
        batch_size=16,
        class_mode='binary')

# 검증 데이터 설정
validation_generator = test_datagen.flow_from_directory(
        validation_dir,
        target_size=(224, 224),
        batch_size=16,
        class_mode='binary')

# 모델 학습시키기
history = model.fit_generator(
      train_generator,      # 첫 번째 인자
      steps_per_epoch=100,  # 한 epochs에 사용한 스템 수
      epochs=100,           # 전체 훈련 데이터셋에 대해 학습 반복 횟수
      validation_data=validation_generator,
      validation_steps=50)

# 정확도
acc = history.history['acc']
# 검증용 정확도
val_acc = history.history['val_acc']
# 손실
loss = history.history['loss']
# 검증용 손실
val_loss = history.history['val_loss']

# epochs
epochs = range(len(acc))

# 그래프로 과대적합 확인해보기
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()

