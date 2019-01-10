import paho.mqtt.client as mqtt
from time import sleep

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("LORA/recv")

def on_message(client, userdata, msg):
    try:        
        msg_txt = str(msg.payload)
        print("MSG: " + msg.topic + " " + msg_txt)
        if msg_txt.startswith("SETTEMP,"):
            println("Set temperature message")
            cmd, value = msg_txt.split(",", 1)
            temp = int(value)
            if value >= 10 and value <= 30:
                client.publish("LORA/send", "APPLYTEMP," + value)
            else:
                println("Invalid temperature: " + value)
        else:
            println("Unrecognised message")
    except:
        print "Unexpected error:", sys.exc_info()[0]

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt", 1883, 60)

client.loop_forever()