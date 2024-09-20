from time import sleep
import pygetwindow
from IOControl import IOControl
from FrontendReader import FrontendReader
from TooltipReader import TooltipReader

if "Megaloot" in pygetwindow.getActiveWindowTitle():
    print("[INFO] Capturing now")
    img = FrontendReader.capture_screenshot()
    cash = FrontendReader.cash()
    next_f, current_f = FrontendReader.next_floor(img)
    next_c, current_c = FrontendReader.next_fight(img)
    #FrontendReader.player_stats()
    if True:
        for id in range (32):
            FrontendReader.capture_item(id)
