from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyController
from PIL import ImageGrab
import time
from datetime import datetime, timedelta


class Runner:
    def __init__(self):
        self.mouse = Controller()
        self.keyboard = KeyController()
        self.chat_colors = [
            (1, 10, 19),  # chatbox body color
            (14, 23, 30),
        ]
        self.lockin_colors = [
            (92, 91, 87),  # button border
        ]
        self.player_joined_colors = [
            (66, 66, 65),
            (66, 66, 66),
        ]

    def move_and_type_first(self, lane, repeat, chatbox, lockin, timeout=5*60):
        self._type_when_color(
            chatbox,
            lockin,
            self.lockin_colors,
            lane,
            repeat,
            rect2=chatbox,
            expected_colors2=self.chat_colors,
            timeout_sec=timeout,
            name='matchmake screen'
        )

    def move_and_type_again(self, lane, repeat, chatbox, players_joined, timeout=5):
        self._type_when_color(chatbox, players_joined, self.player_joined_colors, lane, repeat, timeout_sec=timeout, name='player joined', wait_timeout=True)

    #
    # Utility
    #

    def _type_when_color(self, chatbox, rect, expected_colors, text, repeat, timeout_sec=5, name='', rect2=None, expected_colors2=None, wait_timeout=False):
        print('Type when %s...' % name)
        t_start = datetime.utcnow()
        x = chatbox.avg_x()
        y = chatbox.avg_y()
        while True:
            if datetime.utcnow() - t_start > timedelta(seconds=timeout_sec):
                print('Done waiting %s to appear (timeout is set to %d sec)' % (name, timeout_sec))
                break
            if self._rect_contains_color(rect, expected_colors):
                print('First color is correct')
                if rect2 is None or self._rect_contains_color(rect2, expected_colors2):
                    print('Typing to coordinates: (%d, %d)' % (x, y))
                    self._move_and_type(x, y, text, repeat)
                    if not wait_timeout:
                        break
        print('Done typing when %s' % name)

    def _move_and_type(self, x, y, lane, howManyTimes):
        for i in range(howManyTimes):
            self.mouse.position = (x, y)
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)
            self.keyboard.type(lane)
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)
            time.sleep(0.1)

    def _color_at_pixel(self, x, y):
        px = ImageGrab.grab((x, y, x + 1, y + 1)).load()
        selected = px[0, 0]
        return selected[0], selected[1], selected[2] # R, G, B

    def _rect_contains_color(self, rect, colors):
        px = ImageGrab.grab(rect.to_tuple()).load()
        for i in range(rect.length()):
            for j in range(rect.height()):
                if px[i, j] in colors:
                    return True
        return False
