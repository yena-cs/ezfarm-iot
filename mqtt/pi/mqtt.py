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
directControl_sub = 'pi/'+farm_id
directControl_pub = 'pi/send/'+farm_id
imageControl_sub = 'image_send/'+farm_id
imageControl_pub = 'image_send/result/'+farm_id
sensorControl_sub = 'data/'+farm_id
sensorControl_pub = "sensor_sub/"+farm_id
sensor_pub = "test/testing"
image_pub = "connect/sub"
PATH_TO_CERT = "./smartfarm-certificate.pem.crt"
PATH_TO_KEY = "./smartfarm-private.pem.key"
PATH_TO_ROOT = "./AmazonRootCA1.pem"

time.sleep(1)
port = "/dev/ttyUSB0"
port2 = "/dev/ttyUSB1"

while True:
    #if os.path.isdir(port2): #and os.path.isdir(port2):
    ser = serial.Serial(port, 9600)
    ser2 = serial.Serial(port2, 9600)
    ser.flushInput()
    ser2.flushInput()
    if ser.readable() and ser2.readable():
        ser_num = str(ser.readline())
        ser_num = re.sub('[^0-9,]', "", ser_num)
        ser_num = ser_num.split(',')
        break
    else:
         print("Not data Sensor")
    #else:
        #print("Not Connect Arduino")
    time.sleep(1)

if ser_num[0] != '1':
    tmp = port
    port = port2
    port2 = tmp
    ser = serial.Serial(port, 9600)
    ser2 = serial.Serial(port2, 9600)
    ser.flushInput()
    ser2.flushInput()


def sensor_data():
    smart_farm = str(ser.readline())
    print(smart_farm)
    smart_farm2 = str(ser2.readline())
    #smart_farm=[1, 2, 3, 4]
    print(smart_farm2)
    smart_farm = re.sub('[^0-9,.]', "", smart_farm)
    smart_farm2 = re.sub('[^0-9,.]', "", smart_farm2)
    smart_farm = smart_farm.split(',')
    smart_farm2 = smart_farm2.split(',')
    if len(smart_farm) != 4 or len(smart_farm2) != 4:
        return 0
    time = datetime.datetime.now()
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    message = {"farm_id": farm_id, "tmp": smart_farm2[3], "co2": smart_farm[1], "humidity": smart_farm2[2],"illuminance": smart_farm2[1], "mos": smart_farm[2], "ph": smart_farm[3], "measure_date": date}
    print(message)
    return message


def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        mqttc.subscribe(directControl_sub, qos=0)
        mqttc.subscribe(imageControl_sub, qos=0)
        mqttc.subscribe(sensorControl_sub, qos=0)


def on_message(mqttc, obj, msg):
    if msg.topic == directControl_sub:
        payload = msg.payload.decode('utf-8')
        j = json.loads(payload)
        print(j)
        water ="<" + str(j['water'])+","
        tmp = "<" + str(j['tmp']) + ","
        led = str(j['led'])+">"
        window = str(j['window'])+">"
        s1 = water + window
        s2 = tmp + led
        print(s1, s2)
        ser.write(s1.encode('utf-8'))
        ser2.write(s2.encode('utf-8'))
        direct_message = {"farm_id": farm_id}
        mqtt_client.publish(directControl_pub, json.dumps(direct_message), qos=1) 

    if msg.topic == imageControl_sub:
        payload = msg.payload.decode('utf-8')
        j = json.loads(payload)
        key, measure_time = upload.image_file(1, farm_id)
        image_message = {"farm_id": farm_id, "key": key, "measure_time": measure_time}
        mqtt_client.publish(image_pub, json.dumps(image_message), qos=1)
        print(image_message)
        mqtt_client.publish(imageControl_pub, json.dumps(image_message), qos=1)

    if msg.topic == sensorControl_sub:
        payload = msg.payload.decode('utf-8')
        j = json.loads(payload)
        if str(j['farm_id']) == farm_id:
            message = sensor_data()
            mqtt_client.publish(sensorControl_pub, json.dumps(message), qos=1)
            print("Published: '" + json.dumps(message) + "' to the topic: " + sensorControl_pub)


def hour_send():
    message = sensor_data()
    if message == 0:
        time.sleep(1)
        message = sensor_data()
    mqtt_client.publish(sensor_pub, json.dumps(message), qos=1)
    print("Published: '" + json.dumps(message) + "' to the topic: " + sensor_pub)

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
