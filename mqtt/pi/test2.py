import time, json, ssl
import schedule
import paho.mqtt.client as mqtt
import datetime
import re
import serial
import upload

ENDPOINT = 'a3l96rdgghmoau-ats.iot.ap-northeast-2.amazonaws.com'
THING_NAME = 'smartfarm'
sub = 'pi/1'
sub2 = 'image/send/1'
PATH_TO_CERT = "./smartfarm-certificate.pem.crt"
PATH_TO_KEY = "./smartfarm-private.pem.key"
PATH_TO_ROOT = "./AmazonRootCA1.pem"
TOPIC = "test/testing"


def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print('connected!!')
        mqttc.subscribe(sub, qos=0)
        mqttc.subscribe(sub2, qos=0)


def on_message(mqttc, obj, msg):
    if msg.topic == sub:
        payload = msg.payload.decode('utf-8')
        j = json.loads(payload)
        water ="<" + str(j['water'])+";"
        tmp = "<" + str(j['tmp']) + ";"
        led = str(j['led'])+">"
        window = str(j['window'])+">"
        s1 = water + window
        s2 = tmp + led
        print(s1, s2)
        ser.write(s1.encode())
        ser2.write(s2.encode())

    if msg.topic == sub2:
        payload = msg.payload.decode('utf-8')
        j = json.loads(payload)
        im = str(j['image'])
        key, measure_time = upload.image_file(1)
        image_message = {"farm_id": str(1), "key": key, "measure_time": measure_time}
        mqtt_client.publish("connect/sub", json.dumps(image_message), qos=1)
        print(image_message)


def hour_send():
    key, measure_time = upload.image_file(0)
    image_message = {"farm_id": str(1), "key": key, "measure_time": measure_time}
    mqtt_client.publish("connect/sub", json.dumps(image_message), qos=1)
    print(image_message)


mqtt_client = mqtt.Client(client_id=THING_NAME)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.tls_set(PATH_TO_ROOT, certfile=PATH_TO_CERT, keyfile=PATH_TO_KEY, tls_version=ssl.PROTOCOL_TLSv1_2,
                    ciphers=None)
mqtt_client.connect(ENDPOINT, port=8883)
mqtt_client.loop_start()
schedule.every(1).hours.do(hour_send)

hour_send()
while True:
    schedule.run_pending()
    time.sleep(1)

