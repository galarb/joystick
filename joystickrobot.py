import socket
import network
import time

WIFI_SSID = "xxx"
WIFI_PASSWORD = "xxxx"
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
        
s = socket.socket()
s.settimeout(3)
try:
    s.connect(("10.100.102.47", 1883))
    print("Port 1883 open!")
except Exception as e:
    print("Connection failed:", e)
finally:
    s.close()

