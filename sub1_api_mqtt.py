from threading import Timer
import paho.mqtt.client as mqtt
import config
import json
from datetime import datetime

from dialogue import Information


def write_log(msg, ex=None):
    print("[%s] %s" % (str(datetime.now())[5:-3], msg))
    if ex:
        print(ex)


class Sub1_api:

    def __init__(self):
        self.location = ([25.0070536, 121.4708157], [True])
        self.destination = None
        self.indoor = False
        self.arrived = True
        self.awakable = False

        print("Connecting to %s, port: %d, user: %s" % (config.mqtt_address, config.mqtt_port, config.mqtt_username))
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        if config.mqtt_username:
            self.client.username_pw_set(config.mqtt_username, config.mqtt_password)
        self.client.connect(config.mqtt_address, config.mqtt_port, config.mqtt_keepalive)
        self.client.loop_start()

    def __on_connect(self, client, userdata, flags, rc):
        write_log("Connected with result code " + str(rc))
        client.subscribe("echo")
        client.subscribe("location")
        client.subscribe("awakable")
        client.subscribe("indoor")
        client.subscribe("kanban_indoor")

    def __on_message(self, client, db, msg):
        data = msg.payload.decode('utf-8', 'ignore')
        write_log("topic: %s, data: %s" % (msg.topic, data))
        if data:
            try:
                data = json.loads(data)
            except:
                write_log("[ERROR] json.loads(data)")
                topic = ""
                data = {}

        if "location" == msg.topic:
            self.location = ([data["lat"], data["lng"]], [True])
        elif "awakable" == msg.topic:
            self.awakable = "on" == data["status"]
        elif "indoor" == msg.topic:
            self.indoor = "on" == data["status"]
        elif "kanban_indoor" == msg.topic:
            Information.set_indoor_kanbans(data)
        elif "arrived" == msg.topic:
            self.__set_arrived()
        elif "echo" == msg.topic:
            write_log("An echo got.")

    def __set_arrived(self):
        self.arrived = True
        if self.arrived:
            payload = {"status": "on"}
        else:
            payload = {"status": "off"}
        self.client.publish("arrived", json.dumps(payload))
        print("Sub1 arrived..")
    
    def get_location(self):
        return self.location

    def is_awakable(self):
        return self.awakable

    def set_user_speaking(self, is_speaking):
        if is_speaking:
            payload = {"status": "on"}
        else:
            payload = {"status": "off"}
        self.client.publish("user_speaking", json.dumps(payload))

    def set_destination(self, dest):
        self.destination = dest

        if dest:
            self.arrived = False

            payload = {
                "lat": dest[0],
                "lng": dest[1],
                "type": dest[2],
            }
            self.client.publish("destination", json.dumps(payload))
            self.client.publish("arrived", json.dumps({"status": "off"}))
        else:
            self.arrived = True
            self.client.publish("destination", "")
            self.client.publish("arrived", json.dumps({"status": "on"}))


    def is_indoor(self):
        return self.indoor

    def set_indoor(self, indoor):
        self.indoor = indoor
        if self.indoor:
            payload = {"status": "on"}
        else:
            payload = {"status": "off"}
        self.client.publish("indoor", json.dumps(payload))

    def is_arrived(self):
        return self.arrived

    
if __name__ == '__main__':
    sub1_api = Sub1_api()
