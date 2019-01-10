import paho.mqtt.client as mqtt
from time import sleep

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("LORA/recv")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    msg_txt = str(msg.payload)
    if (msg_text.startswith("SETTEMP,")):
        cmd, value = msg_txt.split(",", 1)
        temp = int(value)
        if (value >= 10 and value <= 30):
            client.publish("LORA/send", "APPLYTEMP," + value)
        else:
            println("Invalid temperature: " + value)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt", 1883, 60)

client.loop_forever()