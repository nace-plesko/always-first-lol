from tkinter import *
from detector import Detector, Calibration, Rect
from tkinter import messagebox
from runner import Runner
from threading import Thread
import threading
import time, os

LANE = ''
INITIAL_COUNT = 5
WAIT_INITIAL_SEC = 10 * 60  # 5 minutes
ON_PLAYER_JOINED_COUNT = 2
WAIT_PLAYER_JOINED_SEC = 5

runner_thread = None
stoprequest = threading.Event()
status = None
status_string = None


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
    global runner_thread, status
    global stoprequest
    if runner_thread is not None and runner_thread.is_alive():
        stoprequest.set()
        status.destroy()

    else:
        messagebox.showinfo(title="Stop",
                            message="Not running")


def run():
    global stoprequest, status, status_string, top
    runner = Runner()
    calibrated = Calibration()
    is_calibrated = calibrated.calibrate()
    LANE = e1.get()
    status_string = StringVar(top)
    status = Label(textvariable=status_string, bd=1, relief=SUNKEN)
    status.place(x=0, y=80)
    status_string.set("Status: calibrating...")

    if is_calibrated:
        status_string.set("Status: running...")

        runner.move_and_type_first(LANE, INITIAL_COUNT, calibrated.chatbox, calibrated.lockin,
                                   timeout=WAIT_INITIAL_SEC, stoprequest=stoprequest)
        time.sleep(0.1)
        status_string.set("Status: searching for players joined...")
        runner.move_and_type_again(LANE, ON_PLAYER_JOINED_COUNT, calibrated.chatbox, calibrated.players_joined,
                                   timeout=WAIT_PLAYER_JOINED_SEC, stoprequest=stoprequest)
        status_string.set("Status: done")


    else:
        messagebox.showinfo(title="calibration",
                            message="Error: can not calibrate. Make sure you are in LOBBY and try again")
        button_stop()

top = Tk(className="always first")
top.geometry("250x100")

# b1 = Button(top, text = "calibrate", command = button_calibrate)
# b1.place(x = 20, y = 50)

Label(top, text="Lane").grid(row=0)
e1 = Entry(top)
e1.insert(10, "MID")
e1.grid(row=0, column=1)

b2 = Button(top, text = "Run", command = button_run)
b2.place( x = 30, y = 30)

b3 = Button(top, text = "Stop", command = button_stop)
b3.place( x = 75, y = 30)

author = Label(text="@author: Nace P.", bd=1, relief=FLAT)
author.place(x=150, y=80)

version = Label(text="v0.2.0", bd=1, relief=FLAT)
version.place(x=183, y=60)

#top.iconbitmap(r'C:\Nace\PycharmProjects\always-first-lol\First_Place_PNG_Clipart_Image.ico')

top.mainloop()


print("------end-------")


