from machine import Pin
import time
import network
from umqtt.simple import MQTTClient
import json

WIFI_SSID = "estupit"
WIFI_PASSWORD = "lafamilia"
MQTT_BROKER = "10.100.102.47"
MQTT_TOPIC = b"control/vector"

class joystick:
    def __init__(self,
                 up_pin,
                 down_pin,
                 right_pin,
                 left_pin,
                 speedup_pin,
                 speeddown_pin):

        self.up = Pin(up_pin, Pin.IN, Pin.PULL_UP)
        self.down = Pin(down_pin, Pin.IN, Pin.PULL_UP)
        self.right = Pin(right_pin, Pin.IN, Pin.PULL_UP)
        self.left = Pin(left_pin, Pin.IN, Pin.PULL_UP)
        self.speedup = Pin(speedup_pin, Pin.IN, Pin.PULL_UP)
        self.speeddown = Pin(speeddown_pin, Pin.IN, Pin.PULL_UP)

        self.speed = 100  # Initial speed (0–100)
        self.last_speedup = 1
        self.last_speeddown = 1
        self.last_update_time = time.ticks_ms()

        self.client = MQTTClient("joystick", "10.100.102.47", port=1883)

    def connect_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        time.sleep(1)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        print("Connecting to Wi-Fi...", end="")
        timeout = 0
        while not wlan.isconnected():
            time.sleep(0.5)
            print(".", end="")
            timeout += 1
            if timeout > 20:
                raise RuntimeError("Wi-Fi timeout")
        print("\nConnected! IP:", wlan.ifconfig()[0])

    def connect_mqtt(self):
        self.client.connect()
        print("MQTT connected")

    def get_vector(self):
        vx = 0
        vy = 0
        omega = 0

        if self.left.value() == 0:
            vx = -1
            print("left")  

        elif self.right.value() == 0:
            vx = 1
            print("right")  


        if self.up.value() == 0:
            vy = 1
            print("up")  

        elif self.down.value() == 0:
            vy = -1
            print("down")  

        if self.speedup.value() == 0:
            omega = -1
            #print("speed up")  

        elif self.speeddown.value() == 0:
            omega = 1
            #print("speed down")  

        #print("Raw vector:", (vx, vy, omega))  

        return vx, vy, omega

    def update_speed(self):
        su = self.speedup.value()
        sd = self.speeddown.value()
        now = time.ticks_ms()

        if time.ticks_diff(now, self.last_update_time) > 200:
            if su == 0 and self.last_speedup == 1:
                self.speed = min(100, self.speed + 10)
                self.last_update_time = now
            elif sd == 0 and self.last_speeddown == 1:
                self.speed = max(0, self.speed - 10)
                self.last_update_time = now

        self.last_speedup = su
        self.last_speeddown = sd

    def get_scaled_vector(self):
        self.update_speed()
        vx, vy, omega = self.get_vector()
        return vx * self.speed, vy * self.speed, omega * self.speed

    def send_vector(self):
        
        vx, vy, omega = self.get_scaled_vector()
        payload = json.dumps({"vx": vx, "vy": vy, "omega": omega})
        self.client.publish(MQTT_TOPIC, payload.encode())
        
