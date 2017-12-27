import sys
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyController
from PIL import Image, ImageGrab
import time

#wanted rgb pixel is (1, 10, 19)
mouse = Controller()
keyboard = KeyController()

#get position easily
#while True:
#  print(mouse.position)

x = 536
y = 954

#run the program until you don't get mid
while True:
    px = ImageGrab.grab().load()
    if px[x, y][0] == 1 and px[x, y][1] == 10 and px[x, y][2] == 19:
        mouse.position = (x, y) #move mouse to the wanted position
        mouse.press(Button.left)
        mouse.release(Button.left)

        #type mid a few times
        for i in range(0, 7):
            keyboard.type('MID')
            keyboard.press(Key.enter)
            time.sleep(0.12)
        break
