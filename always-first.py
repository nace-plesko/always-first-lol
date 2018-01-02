from runner import Runner
from detector import Detector
import time

LANE = 'MID'
INITIAL_COUNT = 5
WAIT_INITIAL_SEC = 10 * 60  # 5 minutes
ON_PLAYER_JOINED_COUNT = 3
WAIT_PLAYER_JOINED_SEC = 5

DEBUG_DETECTOR = False
DEBUG_RUNNER = False

time.sleep(2)
runner = Runner()
detector = Detector()
chatbox = detector.find_chatbox(debug=DEBUG_DETECTOR)
lockin = detector.find_lockin(chatbox)
players_joined = detector.find_players_joined(chatbox)

detector.test_detector(chatbox, lockin, players_joined)

runner.move_and_type_first(LANE, INITIAL_COUNT, chatbox, lockin, timeout=WAIT_INITIAL_SEC, debug=DEBUG_RUNNER)
time.sleep(0.1)
runner.move_and_type_again(LANE, ON_PLAYER_JOINED_COUNT, chatbox, players_joined, timeout=WAIT_PLAYER_JOINED_SEC,
                           debug=DEBUG_RUNNER)
