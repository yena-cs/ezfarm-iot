#!usrbinenv python3
import json
import ssl
import paho.mqtt.client as mqtt
import sys
import os
import time

ENDPOINT = 'a3l96rdgghmoau-ats.iot.ap-northeast-2.amazonaws.com'
THING_NAME = 'control'

PATH_TO_CERT = .certsconnect-certificate.pem.crt
PATH_TO_KEY = .certsconnect-private.pem.key
PATH_TO_ROOT = .certsAmazonRootCA1.pem

TOPIC = data
SUB = sensor_sub

def on_connect(mqttc, obj, flags, rc)
    if rc == 0
        status = 3
    else
        global result
        result = 0,0,0,0,0,0,0


def on_disconnect(client, userdata, flags, rc=0)
    status = 3
    global result
    print(result)


def on_message(mqttc, obj, msg)
    if msg.topic == SUB
        payload = msg.payload.decode('utf-8')
        j = json.loads(payload)
        tmp = str(j['tmp'])
        humidity = str(j['humidity'])
        illuminance = str(j['illuminance'])
        co2 = str(j['co2'])
        ph = str(j['ph'])
        mos = str(j['mos'])
        time = str(j['measure_date'])
        global result
        result = humidity + , + tmp + , + illuminance + , + co2 + , + ph + , + mos+,+time
        mqttc.loop_stop()
        mqttc.disconnect()

mqtt_client = mqtt.Client(client_id=THING_NAME)
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message
mqtt_client.tls_set(PATH_TO_ROOT, certfile=PATH_TO_CERT, keyfile=PATH_TO_KEY, tls_version=ssl.PROTOCOL_TLSv1_2,ciphers=None)
mqtt_client.connect(ENDPOINT, port=8883)
mqtt_client.loop_start()


time.sleep(1)
if len(sys.argv) == 2
    a1 = sys.argv[1]
    TOPIC += str(a1)
    SUB += str(a1)
    message = {farm_id a1}
    mqtt_client.publish(TOPIC, json.dumps(message), qos=1)
    mqtt_client.subscribe(SUB, qos=0)
    mqtt_client.loop_forever()
else
    result = 0,0,0,0,0,0,0
    print(result)
