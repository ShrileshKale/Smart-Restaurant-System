import json
import requests
import sys
import os
import paho.mqtt.client as mqtt
import time

# Data to pass to online editor of pddl
data = {'domain': open(sys.argv[1], 'r').read(),
        'problem': open(sys.argv[2], 'r').read()}


# Function for MQTT connect ,triggrs when connection established
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    print('Connected')


# Function on_message is callback function once data is received
def on_message(mqttc, obj, msg):
    response = msg.payload
    data = (str(response.decode("utf-8")))

    if data == 'AI':
        func()
        fileop()

    else:
        return


# Function which triggers when subscribed to particular topic
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    return

# Function to publish data
def publish_data():
    print('inside publish')

    Data = {
        'Central Lighting': 'ON'
    }
    print(Data)
    mqttc.publish('lighting_control/central/lighting/PC', json.dumps(Data))
    print("Data Published")
    time.sleep(1)


# Function to execute AI planning and get plan.txt file
def func():
    response = requests.post('http://solver.planning.domains/solve', json=data).json()
    with open(sys.argv[3], 'w') as f:
        for act in response['result']['plan']:
            f.write('\n')
            f.write(str(act['name']))

# Function to operate on plan.txt file
def fileop():
    f = open("plan.txt", "r")

    zero_line = f.readline()

    first_line = f.readline()

    second_line = f.readline()

    third_line = f.readline()

    if first_line[7] == 'o' and first_line[8] == 'n':
        if second_line[5] == 'o' and second_line[6] == 'n':
            if third_line[5] == 'o' and third_line[6] == 'n':
                publish_data()

    f.close()


# Initialize MQTT and subscribe to MQTT broke(RPi)
mqttc = mqtt.Client("client-id")
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.connect("192.168.0.111", 1883, 60)
mqttc.subscribe("lighting_control/central/lighting/esp8266", 0)
mqttc.loop_forever()
