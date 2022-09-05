import paho.mqtt.client as mqtt
import time


OUR_IP = "192.168.0.6"  #필요에 따라 바꿔 쓰세용

mqttc = mqtt.Client()
mqttc.connect(OUR_IP,1883,60)
mqttc.loop_start

while True:
    now = time.localtime()
    (result, mid) = mqttc.publish("testtest", "Hello From The " + time.strftime('%c', now))
    print("Hello From The " + time.strftime('%c', now), result, sep=',')
    time.sleep(1)

mqttc.loop_stop()
mqttc.disconnect()
