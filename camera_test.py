#!/usr/bin/env python3
"""Python camera test"""

from picamera2 import Picamera2
import time

print("Initializing camera...")
camera = Picamera2()

config = camera.create_still_configuration(
    main={"size": (640, 480)}
)
camera.configure(config)

print("Starting camera...")
camera.start()
time.sleep(2)

print("Capturing image...")
image = camera.capture_array()

from PIL import Image
img = Image.fromarray(image)
img.save("python_test.jpg")
print("? Image saved as 'python_test.jpg'")

print(f"? Camera test PASSED!")
print(f"  Image size: {image.shape}")

camera.stop()

