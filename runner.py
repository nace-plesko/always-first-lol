from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyController
from PIL import ImageGrab
import time

#wanted rgb pixel is (1, 10, 19)

class Runner:

    def __init__(self):
        self.mouse = Controller()
        self.keyboard = KeyController()

    #go to given coordinates and type the text
    def moveAndType(self, x, y, lane, howManyTimes):
        while True:
            #check the color of wanted pixel and wait for the right rgb values
            px = ImageGrab.grab((x, y, x+1, y+1)).load()

            # print('x, y = (%d, %d)' % (x, y))
            # print('barve = (%d, %d, %d)' % (px[0,0][0], px[0,0][1], px[0,0][2]))

            # if px[x, y][0] == 1 and px[x, y][1] == 10 and px[x, y][2] == 19:
            if px[0, 0][0] == 1 and px[0, 0][1] == 10 and px[0, 0][2] == 19:
                self.mouse.position = (x, y)  #move mouse to the wanted position
                self.mouse.press(Button.left) #and click there
                self.mouse.release(Button.left)
                self.type(lane, howManyTimes) #type your lane a few times

                break

            time.sleep(0.1)

    #this method types a certian text specified amount of times and presses enter
    #each time
    def type(self, lane, howManyTimes):
        for i in range(howManyTimes):
            self.keyboard.type(lane)
            self.keyboard.press(Key.enter)
            time.sleep(0.1)

    def testChatBox(self, x_min, x_max, y_min, y_max):
        image = ImageGrab.grab()
        px = image.load()
        for i in range(x_min, x_max):
            for j in range (y_min, y_max):
                px[i, j] = (0, 200, 0, 255)

        image.show()