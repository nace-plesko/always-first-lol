from runner import Runner
from detector import Detector
import time

time.sleep(2)
runner = Runner()
detector = Detector()
chatbox = detector.find_chatbox()
lockin = detector.find_lockin(chatbox)
runner.testChatBox(chatbox, lockin)
runner.moveAndType("MID", 9, chatbox, lockin)
