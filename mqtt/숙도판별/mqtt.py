import json
import ssl
import paho.mqtt.client as mqtt
import discrimination

ENDPOINT = 'a3l96rdgghmoau-ats.iot.ap-northeast-2.amazonaws.com'
THING_NAME = 'connect'
sub = 'connect/sub' 
PATH_TO_CERT = "./certs/connect-certificate.pem.crt"
PATH_TO_KEY = "./certs/connect-private.pem.key"
PATH_TO_ROOT = "./certs/AmazonRootCA1.pem"
TOPIC = "connect/pub"

def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        mqttc.subscribe(sub, qos=0)


def on_message(mqttc, obj, msg):
    if msg.topic == sub:
        payload = msg.payload.decode('utf-8')
        j = json.loads(payload)
        farm_id = str(j['farm_id'])
        key = str(j['key'])
        measure_time = str(j['measure_time'])
        predict = str(discrimination.image_color(key))
        connect_message = {"farm_id": farm_id, "key": key, "predict": predict, "measure_time": measure_time}
        mqtt_client.publish(TOPIC, json.dumps(connect_message), qos=1)
        print(connect_message)


mqtt_client = mqtt.Client(client_id=THING_NAME)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.tls_set(PATH_TO_ROOT, certfile=PATH_TO_CERT, keyfile=PATH_TO_KEY, tls_version=ssl.PROTOCOL_TLSv1_2,
                    ciphers=None)
mqtt_client.connect(ENDPOINT, port=8883)
mqtt_client.loop_start()

mqtt_client.loop_forever()
