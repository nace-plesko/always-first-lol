from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyController
from PIL import ImageGrab
import time
from datetime import datetime, timedelta

#wanted rgb pixel is (1, 10, 19)

class Runner:

    def __init__(self):
        self.mouse = Controller()
        self.keyboard = KeyController()
        self.chat_colors = [
            (1, 10, 19),
        ]
        self.lockin_colors = [
            (30, 35, 40),
            (29, 36, 41),
            (29, 38, 42),
        ]
        self.player_joined_colors = [
            (66, 66, 65),
            (66, 66, 66),
        ]

    def color_at_pixel(self, x, y):
        px = ImageGrab.grab((x, y, x + 1, y + 1)).load()
        selected = px[0, 0]
        return selected[0], selected[1], selected[2] # R, G, B

    def rect_contains_color(self, rect, colors=[]):
        px = ImageGrab.grab(rect.to_tuple()).load()
        for i in range(rect.length()):
            for j in range(rect.height()):
                if px[i, j] in colors:
                    return True
        return False

    #go to given coordinates and type the text
    def moveAndType(self, lane, howManyTimes, chatbox, lockin):
        t_start = datetime.utcnow()
        x = chatbox.avg_x()
        y = chatbox.avg_y()
        while True:
            if datetime.utcnow() - t_start > timedelta(minutes=5):
                print('Timeout waiting matchmaking screen to appear')
                return
            if self.color_at_pixel(lockin.avg_x(), lockin.avg_y()) in self.lockin_colors:
                print('lockin color is correct')
                self.mouse.position = (x, y)  #move mouse to the wanted position
                self.mouse.press(Button.left) #and click there
                self.mouse.release(Button.left)
                self.type(lane, howManyTimes) #type your lane a few times
                break

    def move_and_type_again(self, lane, howManyTimes, chatbox, players_joined):
        t_start = datetime.utcnow()
        x = chatbox.avg_x()
        y = chatbox.avg_y()
        while True:
            if datetime.utcnow() - t_start > timedelta(seconds=3):
                print('Timeout waiting new players to join')
                return
            if self.rect_contains_color(players_joined, self.player_joined_colors):
                print('new player has joined')
                self.mouse.position = (x, y)  #move mouse to the wanted position
                self.mouse.press(Button.left) #and click there
                self.mouse.release(Button.left)
                self.type(lane, howManyTimes) #type your lane a few times


    #this method types a certian text specified amount of times and presses enter
    #each time
    def type(self, lane, howManyTimes):
        for i in range(howManyTimes):
            self.keyboard.type(lane)
            self.keyboard.press(Key.enter)
            time.sleep(0.1)

    def testChatBox(self, chatbox, lockin, players_joined):
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
        time.sleep(1)
        self.keyboard.press(Key.alt)
        self.keyboard.press(Key.f4)
        self.keyboard.release(Key.alt)
        self.keyboard.release(Key.f4)