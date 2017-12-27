from runner import Runner
from detector import Detector
import time

time.sleep(2)
runner = Runner()
detector = Detector()
box = detector.find_chatbox()
runner.testChatBox(box.x_min, box.x_max, box.y_min, box.y_max)
print(box)
runner.moveAndType(box.avg_x(), box.avg_y(), "MID", 7)