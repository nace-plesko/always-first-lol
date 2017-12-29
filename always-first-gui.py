from tkinter import *
from detector import Detector, Calibration, Rect
from tkinter import messagebox
from runner import Runner
from threading import Thread
import threading
import time

LANE = 'MID'
INITIAL_COUNT = 5
WAIT_INITIAL_SEC = 10 * 60  # 5 minutes
ON_PLAYER_JOINED_COUNT = 3
WAIT_PLAYER_JOINED_SEC = 5

runner_thread = None
stoprequest = threading.Event()

# def hello():
#    messagebox.showinfo("Say Hello", "Hello World")


def button_calibrate(): #this button calibrates the program
    calibration = Calibration()
    calibrated = calibration.calibrate()
    if calibrated:
        messagebox.showinfo(title="calibration", message="calibration was successful! You can click 'run' now")
    else:
        messagebox.showinfo(title="calibration", message="Error: can not calibrate. Make sure you are in LOBBY and try again")


def button_run(): #this button runs the program
    global runner_thread
    global stoprequest
    stoprequest.clear()
    if runner_thread is None or not runner_thread.is_alive():
        runner_thread = Thread(target=run)
        runner_thread.start()
    else:
        messagebox.showinfo(title="Run",
                            message="Already running")

def button_stop():
    global runner_thread
    global stoprequest
    if runner_thread is not None and runner_thread.is_alive():
        stoprequest.set()
    else:
        messagebox.showinfo(title="Stop",
                            message="Not running")

def run():
    global stoprequest
    runner = Runner()
    calibrated = Calibration()
    is_calibrated = calibrated.calibrate()
    if is_calibrated:
        runner.move_and_type_first(LANE, INITIAL_COUNT, calibrated.chatbox, calibrated.lockin, timeout=WAIT_INITIAL_SEC,
                                   stoprequest=stoprequest)

    else:
        messagebox.showinfo(title="calibration",
                            message="Error: can not calibrate. Make sure you are in LOBBY and try again")
    # messagebox.showinfo(title="ready", message="waiting to get in the game. After you click ACCEPT in LOL, do not move the mouse")


top = Tk()

top.geometry("100x100")

# b1 = Button(top, text = "calibrate", command = button_calibrate)
# b1.place(x = 20, y = 50)

b2 = Button(top, text = "run", command = button_run)
b2.place( x = 50, y = 50)

b3 = Button(top, text = "stop", command = button_stop)
b3.place( x = 50, y = 10)

top.mainloop()


print("------end-------")


