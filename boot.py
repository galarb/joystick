import machine, time, sys

# ESCAPE PIN setup: hold LOW during boot to cancel running main script
ESCAPE_PIN = 0  # GPIO0
p = machine.Pin(ESCAPE_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

print("Booting in 3 seconds... (hold GPIO0 to cancel)")
time.sleep(3)

if p.value():
    try:
        import joystickrobot  # Replace with your actual script name
    except Exception as e:
        print("Fatal error in myscript:", e)
        time.sleep(5)
        print("Rebooting...")
        machine.reset()
else:
    print("Boot interrupted by user. Entering REPL.")

