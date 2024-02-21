# stopwatch.py
###############################################################################
# Description 
#
# This is a stopwatch GUI app with start, stop, and reset functions.
#
# Hitting start while already started has no effect.
#
# When you hit stop, the time is not reset.
#
# You can hit start to resume from the last stop. For example, if you stop at
# 1.5 seconds, and then wait 5 seconds, and then hit start, the time continues
# from 1.5 seconds; not 6.5 seconds.
#
# reset stops and resets the time to 0.
#
# stopping while already stopped has no effect.
#
# On Windows, you can run this without a console window via
# > pythonw .\stopwatch.py 
#
###############################################################################
# Implementation Notes
#
# I just learned how to post a custom event for the tkinter window loop.
# This enabled me to change updateThread so that it doesn't directly update
# lbl_time, and therefore can't deadlock with the window thread.
# However, I didn't take advantage of this to join updateThread directly from
# the window thread. Might be something to try later, to see if it simplifies
# the code.
#
# Also, I figured out the app was hanging on exceptions - not because of the
# window thread deadlocking - but because threadMgr was still running. So I
# guess python doesn't kill the process in that case. So I added a try-except
# that will kill via os._exit(1). 
#

import os
import sys
import threading
import time
import tkinter as tk
import traceback

ONE_MS = 1/1000
SEC_PER_MIN = 60
SEC_PER_HR = SEC_PER_MIN * 60

start = 0
running = False
reset = False
ellapsedSinceStart = 0
ellapsedBeforeStop = 0
ellapsedTotal = 0
updateThread = 0
appRunning = True
eventUpdateTime = "<<UpdateTime>>"
strTime = ""


def startClock():
    global start, running
    if not running:
        start = time.time()
    running = True

def stopClock():
    global running
    running = False

def resetClock():
    global running, reset
    running = False
    reset = True

def manageThread():
    global reset, ellapsedSinceStart, ellapsedBeforeStop, ellapsedTotal, updateThread
    oldVal = running
    valChanged = False
    while appRunning:
        time.sleep(ONE_MS)
        valChanged = oldVal != running
        if valChanged:
            if running:
                updateThread = threading.Thread(target=updateClock)
                updateThread.start()
            else:
                updateThread.join()
                updateThread = 0
                ellapsedBeforeStop += ellapsedSinceStart
        if reset:
            lbl_time["text"] = "00:00:00.000"
            ellapsedBeforeStop = 0
            ellapsedTotal = 0
            reset = False
        oldVal = running

def updateClock():
    global strTime, ellapsedTotal, ellapsedSinceStart
    while running:
        time.sleep(ONE_MS)
        ellapsedSinceStart = time.time() - start
        ellapsedTotal = ellapsedBeforeStop + ellapsedSinceStart
        hours = divmod(ellapsedTotal, SEC_PER_HR)[0]
        remaining = ellapsedTotal - (hours * SEC_PER_HR)
        minutes = divmod(remaining, SEC_PER_MIN)[0]
        seconds = remaining - (minutes * SEC_PER_MIN)
        # print(f"{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}")
        strTime = f"{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}"
        window.event_generate(eventUpdateTime, when="tail")

def on_updateTime(*args):
    lbl_time["text"] = strTime

def on_closing():
    global running
    running = False
    if updateThread != 0:
        window.after(1, on_closing)
        return
    window.destroy()

try:
    fontSize = 25

    window = tk.Tk()
    window.title("stopwatch")
    window.resizable(False,False)
    window.bind(eventUpdateTime, on_updateTime)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    frame_clock = tk.Frame(master=window, bg="yellow")

    lbl_time = tk.Label(master=frame_clock, text="00:00:00.000", font=("Arial",fontSize), width=14, height=2, bg="#FFFFFF")
    lbl_time.pack()

    frame_buttons = tk.Frame(master=window)
    frame_buttons.rowconfigure(0, minsize=50)
    frame_buttons.columnconfigure([0,1,2], minsize=50)

    btn_start = tk.Button(master=frame_buttons, text="start", command=startClock, font=("Arial",fontSize), bg="#00DD00")
    btn_start.grid(row=0, column=0)

    btn_stop = tk.Button(master=frame_buttons, text="stop", command=stopClock, font=("Arial",fontSize), bg="red")
    btn_stop.grid(row=0, column=1)

    btn_reset = tk.Button(master=frame_buttons, text="reset", command=resetClock, font=("Arial",fontSize), bg="blue", fg="#EEEEFF")
    btn_reset.grid(row=0, column=2)

    frame_clock.pack()
    frame_buttons.pack()


    threadMgr = threading.Thread(target=manageThread)
    threadMgr.start()

    window.mainloop()

    appRunning = False
    threadMgr.join()

except:
    traceback.print_exc()
    os._exit(1)

