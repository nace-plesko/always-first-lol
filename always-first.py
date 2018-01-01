from runner import Runner
from detector import Detector
import time

LANE = 'MID'
INITIAL_COUNT = 5
WAIT_INITIAL_SEC = 10 * 60  # 5 minutes
ON_PLAYER_JOINED_COUNT = 3
WAIT_PLAYER_JOINED_SEC = 5

time.sleep(2)
runner = Runner()
detector = Detector()

#detector.print_color_under_cursor()

chatbox = detector.find_chatbox()
lockin = detector.find_lockin(chatbox)
players_joined = detector.find_players_joined(chatbox)

#chatbox.x_max = chatbox.x_min + 10

detector.test_detector(chatbox, lockin, players_joined)
runner.move_and_type_first(LANE, INITIAL_COUNT, chatbox, lockin, timeout=WAIT_INITIAL_SEC)
time.sleep(0.1)
runner.move_and_type_again(LANE, ON_PLAYER_JOINED_COUNT, chatbox, players_joined, timeout=WAIT_PLAYER_JOINED_SEC)
