# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)


# make new client
client = mqtt.Client()
# set callback function on_connect(connect to broker), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
# address : localhost, port: 1883 에 연결
client.connect('192.168.0.200', 1883)
client.loop_start()
# common topic 으로 메세지 발행
# client.publish('common', json.dumps({"success": "ok"}), 1)
client.publish("/home/pim/esw/test_mqtt","tada", 1)
# +datetime.now().strftime('%Y-%m-%d_%H%M%S')
client.loop_stop()
# 연결 종료
client.disconnect()