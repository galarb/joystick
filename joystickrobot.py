from joystick import joystick
from time import sleep

joy = joystick(
    up_pin=13, down_pin=12,
    right_pin=27, left_pin=4,
    speedup_pin=25, speeddown_pin=32
)

joy.connect_wifi()
joy.connect_mqtt()

for _ in range(200):
    joy.send_vector()
    sleep(0.05)  # 20 Hz rate
print('finished')
