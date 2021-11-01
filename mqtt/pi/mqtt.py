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
port3 = "/dev/ttyUSB2"


ser = serial.Serial(port, 9600)
ser2 = serial.Serial(port2, 9600)
ser3 = serial.Serial(port3, 9600)
ser.flushInput()
ser2.flushInput()
ser3.flushInput()


def sensor_data():
    farm = str(ser.readline())
    print(farm)
    farm2 = str(ser2.readline())
    print(farm2)
    farm = re.sub('[^0-9,.]', "", farm)
    farm2 = re.sub('[^0-9,.]', "", farm2)
    farm = farm.split(',')
    farm2 = farm2.split(',')
    if len(farm) != 4 or len(farm2) != 4:
        return 0
    if(farm[0] == '1'):
        smart_farm = list(farm)
    else:
        smart_farm = list(farm2)
    
    if(farm[0] == '2'):
        smart_farm2 = list(farm)
    else:
        smart_farm2 = list(farm2)
    
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
        water =str(j['water'])
        tmp = str(j['tmp'])
        led = str(j['led'])
        farm = str(ser.readline())
        print(farm)
        farm2 = str(ser2.readline())
        print(farm2)
        farm = re.sub('[^0-9,.]', "", farm)
        farm2 = re.sub('[^0-9,.]', "", farm2)
        farm = farm.split(',')
        farm2 = farm2.split(',')
        if len(farm) != 4 or len(farm2) != 4:
            return 0
        if(farm[0] == '1'):
            s1 = water.encode('utf-8')
        elif(farm2[0] == '1'):
            s2 = water.encode('utf-8')
        
        if(farm[0] == '2'):
            s1 = tmp.encode('utf-8')
        elif(farm2[0] == '2'):
            s2 = tmp.encode('utf-8')
        
        s3 = led.encode('utf-8')
        print(s1, s2, s3)
        time.sleep(3)
        direct_message = {"farm_id": farm_id}
        mqtt_client.publish(directControl_pub, json.dumps(direct_message), qos=1)
        ser.write(s1)
        ser2.write(s2)
        ser3.write(s3)
        print(direct_message)

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
    print(message)
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
