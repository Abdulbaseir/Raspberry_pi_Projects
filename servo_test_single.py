#!/usr/bin/env python3
"""Test a single servo directly on GPIO 12"""

from gpiozero import AngularServo
from time import sleep

print("Initializing servo on GPIO 12...")
servo = AngularServo(13, min_pulse_width=0.0005, max_pulse_width=0.0025)

try:
    print("\n--- Moving to -90 (Physical 0) ---")
    servo.angle = -90
    sleep(2)

    print("--- Moving to 0 (Physical 90 / Center) ---")
    servo.angle = 0
    sleep(2)

    print("--- Moving to 90 (Physical 180) ---")
    servo.angle = 90
    sleep(2)

    print("\n--- Sweeping back and forth ---")
    for angle in range(-90, 91, 5):
        servo.angle = angle
        print(f"\r  Angle: {angle} deg", end="", flush=True)
        sleep(0.05)
        
    for angle in range(90, -91, -5):
        servo.angle = angle
        print(f"\r  Angle: {angle} deg", end="", flush=True)
        sleep(0.05)

    print("\n\nServo test PASSED!")

except KeyboardInterrupt:
    print("\nTest stopped by user.")

finally:
    print("Detaching servo...")
    servo.detach()
