import paho.mqtt.client as mqtt
from subprocess import call
import gtts, os

port = 1883
serverPath = "85468LAPTOPPATH"
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(serverPath + "/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    command = str(msg.payload)[1:]

    # if msg.topic == serverPath + "/range":
    #     volume = str(msg.payload)[1:]
    #     call(["amixer", "-D", "pulse", "sset", "Master", volume, "%"])

    if msg.topic == serverPath + "/lock":
        os.system("rundll32.exe user32.dll, LockWorkStation")

    if msg.topic == serverPath + "/shutdown":
        os.system("shutdown -s -t 1")

    if msg.topic == serverPath + "/speech":
        text = str(msg.payload)[1:]

        print(text)

        if '\xc3\xa4' in text:
            text = text.replace("\xc3\xa4", "ä")
            print("KORVATTU Ä")

        if "\xc3\xb6" in text:
            text = text.replace("\xc3\xb6", "ö")
            print("KORVATTU Ö")


        gtts.gTTS(text=text, lang="fi").save("speech.mp3")
        os.system("speech.mp3")








client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
