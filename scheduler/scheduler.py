import paho.mqtt.client as mqtt
import schedule
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    msg_txt = str(msg.payload)
    print("MSG: " + msg.topic + " " + msg_txt)

def update_temp(temp):
    client.publish("LORA/send", "APPLYTEMP," + str(temp))

hot = False

def toggle_temp():
    if hot:
        update_temp(30)
    else:
        update_temp(10)
    hot = not hot

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt", 1883, 60)
client.loop_start()

# THE IMPORTANT BIT #
# PUT YOUR HEATING SCHEDULE HERE #
schedule.every().monday.at("06:00").do(update_temp, 21)
schedule.every().monday.at("08:00").do(update_temp, 18)
schedule.every().monday.at("17:00").do(update_temp, 21)
schedule.every().monday.at("23:00").do(update_temp, 18)

schedule.every().tuesday.at("06:00").do(update_temp, 21)
schedule.every().tuesday.at("08:00").do(update_temp, 18)
schedule.every().tuesday.at("17:00").do(update_temp, 21)
schedule.every().tuesday.at("23:00").do(update_temp, 18)

schedule.every().wednesday.at("06:00").do(update_temp, 21)
schedule.every().wednesday.at("08:00").do(update_temp, 18)
schedule.every().wednesday.at("17:00").do(update_temp, 21)
schedule.every().wednesday.at("23:00").do(update_temp, 18)

schedule.every().thursday.at("06:00").do(update_temp, 21)
schedule.every().thursday.at("08:00").do(update_temp, 18)
schedule.every().thursday.at("17:00").do(update_temp, 21)
schedule.every().thursday.at("23:00").do(update_temp, 18)

schedule.every().friday.at("06:00").do(update_temp, 21)
schedule.every().friday.at("08:00").do(update_temp, 18)
schedule.every().friday.at("17:00").do(update_temp, 21)
schedule.every().friday.at("23:00").do(update_temp, 18)

schedule.every().saturday.at("06:00").do(update_temp, 21)
schedule.every().saturday.at("23:00").do(update_temp, 18)

schedule.every().sunday.at("06:00").do(update_temp, 21)
schedule.every().sunday.at("23:00").do(update_temp, 18)

# Test schedule (not recommended)
schedule.every(15).seconds.do(toggle_temp)

while True:
    schedule.run_pending()
    time.sleep(1)