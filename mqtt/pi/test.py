import time, json, ssl
import paho.mqtt.client as mqtt
import datetime
import re
import serial
import upload

ENDPOINT = 'a3l96rdgghmoau-ats.iot.ap-northeast-2.amazonaws.com'
THING_NAME = 'smartfarm'
sub = 'pi/2'

PATH_TO_CERT = "/home/pi/certs/smartfarm-certificate.pem.crt"
PATH_TO_KEY = "/home/pi/certs/smartfarm-private.pem.key"
PATH_TO_ROOT = "/home/pi/certs/AmazonRootCA1.pem"
TOPIC = "test/testing"


def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print('connected!!')
        mqttc.subscribe(sub, qos=0)


def on_message(mqttc, obj, msg):
    if msg.topic == sub:
        payload = msg.payload.decode('utf-8')
        j = json.loads(payload)
        print(j['LED'])
        print(j['WATER'])
        print(j['UP'])
        print(j['DOWN'])
        print(j['WINDOW'])


mqtt_client = mqtt.Client(client_id=THING_NAME)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.tls_set(PATH_TO_ROOT, certfile=PATH_TO_CERT, keyfile=PATH_TO_KEY, tls_version=ssl.PROTOCOL_TLSv1_2,
                    ciphers=None)
mqtt_client.connect(ENDPOINT, port=8883)
mqtt_client.loop_start()

port = "/dev/ttyUSB0"
port2 = "/dev/ttyUSB1"
tmp = datetime.datetime(2021, 1, 1, 0, 0, 0, 0)
while True:
    d = datetime.datetime.now()
    now_hour = d.minute  # 시간으로 바꾸기
    tmp_hour = tmp.minute  # 시간으로 바꾸기
    if d.date() != tmp.date():
        key = upload.image_file()
        key = "{}".format(key)
        image_message = {"farm_id": str(1), "key": key}
        mqtt_client.publish("connect/sub", json.dumps(image_message), qos=1)
        tmp = d
    time.sleep(10)
