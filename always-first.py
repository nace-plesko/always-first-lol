from runner import Runner
from detector import Detector
import time

LANE = 'MID'
INITIAL_COUNT = 5
ON_PLAYER_JOINED_COUNT = 3

time.sleep(2)
runner = Runner()
detector = Detector()
chatbox = detector.find_chatbox()
lockin = detector.find_lockin(chatbox)
players_joined = detector.find_players_joined(chatbox)
detector.test_detector(chatbox, lockin, players_joined)
runner.move_and_type_first(LANE, INITIAL_COUNT, chatbox, lockin)
time.sleep(0.1)
runner.move_and_type_again(LANE, ON_PLAYER_JOINED_COUNT, chatbox, players_joined)
