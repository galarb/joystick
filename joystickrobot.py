from joystick import joystick
from time import sleep

joy = joystick(
    up_pin=12, down_pin=14, right_pin=26, left_pin=27,
    speedup_pin=25, speeddown_pin=13
)

joy.connect_wifi()
joy.connect_mqtt()

print("Starting control loop...")

while True:
    joy.send_vector()
    sleep(0.1)
    
