import paho.mqtt.client as mqtt
import subprocess
import gtts, os, time


class main():
    def __init__(self):

        self.port = 1883
        self.serverPath = "85468LAPTOPPATH"

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect("iot.eclipse.org", self.port, 60)

        self.batteryCharge = ""


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe(self.serverPath + "/#")


    def verify(self, verification):
        if verification:
            self.client.publish(self.serverPath + "/verify", "#00FF00")
        else:
            self.client.publish(self.serverPath + "/verify", "#FF0000")
        return

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        #print(msg.topic+" "+str(msg.payload))



        command = str(msg.payload)[1:]

        # if msg.topic == self.serverPath + "/range":
        #     volume = str(msg.payload)[1:]
        #     call(["amixer", "-D", "pulse", "sset", "Master", volume, "%"])


        if msg.topic == self.serverPath + "/swich":
            self.verify(True)
            time.sleep(0.1)
            self.verify(False)
            pass

        if msg.topic == self.serverPath + "/lock":
            self.verify(True)
            os.system("rundll32.exe user32.dll, LockWorkStation")
            self.verify(False)

        if msg.topic == self.serverPath + "/shutdown":
            self.verify(True)
            os.system("shutdown -s -t 1")
            self.verify(False)

        if msg.topic == self.serverPath + "/speech":
            self.verify(True)
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
            self.verify(False)

    def checkBattery(self):
        out = subprocess.run("WMIC PATH Win32_Battery Get EstimatedChargeRemaining", stdout=subprocess.PIPE)
        val = str(out.stdout)
        val = val.replace("EstimatedChargeRemaining", "")
        self.batteryCharge = val[10:12]
        return self.batteryCharge

    def send(self):
        pass

    def sendVariables(self):
        self.client.publish(self.serverPath + "/charge", self.checkBattery())


    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.

    # mainloop starts here
    def run(self):
        start = time.time()
        while True:
            self.client.loop()

            if time.time() - start >= 10:
                print("10 sec kulunut")
                self.sendVariables()
                start = time.time()

            time.sleep(0.1)
            #print("-------------")

if __name__ == "__main__":
    main = main()
    main.run()
