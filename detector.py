import sys
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyController
from PIL import Image, ImageGrab
import time
from PIL import Image, ImageFilter
import util


class Calibration:
    def __init__(self, chatbox=None, lockin=None, players_joined=None):
        self.chatbox = chatbox
        self.lockin = lockin
        self.players_joined = players_joined

    def calibrate(self, ):
        try:
            detector = Detector()
            print("calibration in proccess...")
            self.chatbox = detector.find_chatbox()
            self.lockin = detector.find_lockin(self.chatbox)
            self.players_joined = detector.find_players_joined(self.chatbox)
            #detector.test_detector(self.chatbox, self.lockin, self.players_joined) #uncomment this line if you want to see which chat it finds
            print("calibration was successful!")
            return True

        except AssertionError:
            print("Error: can not calibrate. Make sure you are in LOBBY and try again")
            return False



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

    def height(self):
        return self.y_max - self.y_min

    def length(self):
        return self.x_max - self.x_min

    def topRight_x(self):
        return self.x_max

    def topRight_y(self):
        return self.y_min

    def to_tuple(self):
        return self.x_min, self.y_min, self.x_max, self.y_max


class Detector:
    def __init__(self, screenshot=None):
        self.screenshot = screenshot if screenshot else ImageGrab.grab()
        self.w = self.screenshot.width
        self.h = self.screenshot.height
        self.chatbox_colors = [
            (61, 52, 0),  # frame around chatbox
        ]

    def print_color_under_cursor(self):
        mouse = Controller()
        while True:
            print(ImageGrab.grab().load()[mouse.position[0], mouse.position[1]])
            time.sleep(1)

    def find_chatbox(self, debug=False):
        x_min, x_max = 1000000, -1000000
        y_min, y_max = 1000000, -1000000

        pixels = self.screenshot.load()
        for x in range(self.w):
            for y in range(self.h):
                if util.color_matches_at_least_one(pixels[x, y], self.chatbox_colors, tolerance=3):
                    x_min = x if x < x_min else x_min
                    x_max = x if x > x_max else x_max
                    y_min = y if y < y_min else y_min
                    y_max = y if y > y_max else y_max

                    if debug:
                        pixels[x, y] = (0, 0, 255, 255)
                else:
                    if debug:
                        pixels[x, y] = (0, 0, 0, 255)

        if debug:
            self.screenshot.show()

        if x_max < 0:
            raise AssertionError('Could not find chatbox - make sure you switch to LOL window after starting the program!')

        r = Rect(x_min, x_max, y_min, y_max)
        print('Chatbox: %s' % r)
        return r

    def print_coordinates_under_cursor(self):
        mouse = Controller()
        while True:
            print(mouse.position)
            time.sleep(5)

    def find_lockin(self, rect):
        x_max = int(rect.topRight_x() + rect.length() * 0.95)
        y_min = int(rect.topRight_y() - rect.height() * 2.2)
        r = Rect(x_max - 5 , x_max , y_min - 450, y_min + 50)
        print('Lockin: %s' % r)
        return r

    def find_players_joined(self, rect):
        r = Rect(rect.x_min, rect.x_max, rect.y_min - 3*rect.height(), rect.y_min)
        print('Players joined: %s' % r)
        return r

    def test_detector(self, chatbox, lockin, players_joined):
        image = ImageGrab.grab()
        px = image.load()
        for i in range(chatbox.x_min, chatbox.x_max):
            for j in range (chatbox.y_min, chatbox.y_max):
                px[i, j] = (0, 200, 0, 255)

        for i in range(lockin.x_min, lockin.x_max):
            for j in range (lockin.y_min, lockin.y_max):
                px[i, j] = (0, 200, 0, 255)

        for i in range(players_joined.x_min, players_joined.x_max):
            for j in range (players_joined.y_min, players_joined.y_max):
                px[i, j] = (255, 0, 0, 255)

        image.show()
