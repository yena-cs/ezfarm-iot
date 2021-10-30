import time, json, ssl
import schedule
import os
import paho.mqtt.client as mqtt
import datetime
import re
import serial
import upload

farm_id = os.environ.get('FARM_ID')
ENDPOINT = 'a3l96rdgghmoau-ats.iot.ap-northeast-2.amazonaws.com'
THING_NAME = 'smart_farm'
imageControl_sub = 'image_send/'+farm_id
imageControl_pub = 'image_send/result/'+farm_id
image_pub = "connect/sub"
PATH_TO_CERT = "./smartfarm-certificate.pem.crt"
PATH_TO_KEY = "./smartfarm-private.pem.key"
PATH_TO_ROOT = "./AmazonRootCA1.pem"


def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        mqttc.subscribe(imageControl_sub, qos=0)


def on_message(mqttc, obj, msg):
    if msg.topic == imageControl_sub:
        payload = msg.payload.decode('utf-8')
        j = json.loads(payload)
        key, measure_time = upload.image_file(1, farm_id)
        image_message = {"farm_id": farm_id, "key": key, "measure_time": measure_time}
        mqtt_client.publish(image_pub, json.dumps(image_message), qos=1)
        print(image_message)
        mqtt_client.publish(imageControl_pub, json.dumps(image_message), qos=1)


def hour_send():
    key, measure_time = upload.image_file(0, farm_id)
    image_message = {"farm_id": farm_id, "key": key, "measure_time": measure_time}
    mqtt_client.publish(image_pub, json.dumps(image_message), qos=1)
    print(image_message)


mqtt_client = mqtt.Client(client_id=THING_NAME)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.tls_set(PATH_TO_ROOT, certfile=PATH_TO_CERT, keyfile=PATH_TO_KEY, tls_version=ssl.PROTOCOL_TLSv1_2,ciphers=None)
mqtt_client.connect(ENDPOINT, port=8883)
mqtt_client.loop_start()
schedule.every(1).hours.do(hour_send)

hour_send()
while True:
    schedule.run_pending()
    time.sleep(1)
