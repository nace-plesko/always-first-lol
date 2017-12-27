import sys
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyController
from PIL import Image, ImageGrab
import time
from PIL import Image, ImageFilter


class Rect:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def __str__(self):
        return 'Rect(x_min: %d, x_max: %d, y_min: %d, y_max: %d)' % (self.x_min, self.x_max, self.y_min, self.y_max)

    def avg_x(self):
        return int((self.x_max + self.x_min) / 2)

    def avg_y(self):
        return int((self.y_max + self.y_min) / 2)


class Detector:
    def __init__(self, screenshot=None):
        self.screenshot = screenshot if screenshot else ImageGrab.grab()
        self.w = self.screenshot.width
        self.h = self.screenshot.height
        self.chatbox_colors = [
            # (0,  9, 18, 255),  # before start game
            # (1, 10, 19, 255),  # finding match
            # (61, 52, 0, 255),  # frame around chatbox
            # (53, 41, 14),  # frame around chatbox (screenshot)
            (61, 52, 0),  # frame around chatbox
        ]

    def print_color_under_cursor(self):
        mouse = Controller()
        while True:
            print(ImageGrab.grab().load()[mouse.position[0], mouse.position[1]])
            time.sleep(5)

    def find_chatbox(self):
        x_min, x_max = 1000000, -1000000
        y_min, y_max = 1000000, -1000000

        pixels = self.screenshot.load()
        for x in range(self.w):
            for y in range(self.h):
                if pixels[x, y] in self.chatbox_colors:
                    x_min = x if x < x_min else x_min
                    x_max = x if x > x_max else x_max
                    y_min = y if y < y_min else y_min
                    y_max = y if y > y_max else y_max
        return Rect(x_min, x_max, y_min, y_max)
