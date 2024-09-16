from time import sleep
import pygetwindow
from IOControl import IOControl
from FrontendReader import FrontendReader
from TooltipReader import TooltipReader

def get_shop_items(img_rescaled):
    id = 28
    for id in range(28,4):
        icon, id = FrontendReader.process_screenshot(img_rescaled, id)
        id, item_shop = FrontendReader.identify(id, icon)
        print(f"[INFO] Shop Item {id-27} is: {item_shop}")

while "Megaloot" in pygetwindow.getActiveWindowTitle():
    sleep(1)
    print("[INFO] Capturing now")
    img = FrontendReader.capture_screenshot()
    get_shop_items(img)
    cash = FrontendReader.cash()
    next_f, current_f = FrontendReader.next_floor(img)
    next_c, current_c = FrontendReader.next_fight(img)
    FrontendReader.player_stats()