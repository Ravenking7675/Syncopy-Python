import pyautogui

import base64
from io import BytesIO
from PIL import Image

def create_screenshot():
    print("Taking screenshot...")
    img = pyautogui.screenshot()

    img = img.resize((1280,720), Image.ANTIALIAS)
    img.save('screenshot.jpg', optimize = True, quality=85 )

    thumbnail = Image.open('screenshot.jpg')
    thumbnail = thumbnail.resize((384, 216), Image.ANTIALIAS)
    thumbnail.save("thumbnail.jpg", optimize=True, quality=20)
