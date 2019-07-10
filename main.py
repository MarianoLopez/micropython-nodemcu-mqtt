import json
import ubinascii
from machine import Pin,Timer,unique_id
from umqtt.simple import MQTTClient
from TemperatureSensor import TemperatureSensor

with open('mqtt_config.json') as mqtt_file:
    data = json.load(mqtt_file)

#Led
led = Pin(2, Pin.OUT, value=1)
#Temperature DS18X20 sensor
temp = TemperatureSensor(15)
#MQTT client
CLIENT_ID = ubinascii.hexlify(unique_id())
client = MQTTClient(CLIENT_ID,data['host'],data['port'],data['username'],data['password'])
#topic to publish on
publishTopic = b'temp'
#delay in ms between every publish
publishTimerInMs=5000
#topic to subscribe
subscribeTopic = b'led'

#callback onMessage in subscribeTopic
def subscribeCallback(topic,msg):
    print('Received: {} on topic: {}'.format(msg,topic))
    if msg == b"on":
        led.value(0)
    elif msg == b"off":
        led.value(1)
    elif msg == b"toggle":
        led.value(not led.value())

#init mqtt connection, set subscription topic & callback
def __initMqtt():
    client.set_callback(subscribeCallback)
    client.connect()
    client.subscribe(subscribeTopic)
    print("Connected to %s, subscribed to %s topic as %s" % (data['host'], subscribeTopic,CLIENT_ID))

#read temperature from sensor parse to String & publish to mqtt @publishTopic
def publishTemperature(tim):
    t = str(temp.read_temp())
    print('publish: {} into -> {} topic'.format(t,publishTopic))
    client.publish(publishTopic,t)

def main():
    try:
        __initMqtt()
        #create Timer to call @publishTemperature method every @publishTimerInMs
        tim = Timer(-1)
        tim.init(period=publishTimerInMs, mode=Timer.PERIODIC, callback=publishTemperature)
        while True:
            #check mqtt new messages without block
            client.check_msg()
    except KeyboardInterrupt:        
        print('Interrupted')
        #stop timer
        tim.deinit()
        
main()