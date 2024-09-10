import os
from time import sleep
import cv2
import numpy as np
import win32gui
import pygetwindow as gw
import mss
from PIL import Image

class FrontendReader:
    def capture_screenshot():
        window = gw.getWindowsWithTitle("Megaloot")
        if window:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                print("[INFO] Capturing Frontend")
                img = np.array(sct.grab(monitor))
                imgs = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                pil_img = Image.fromarray(cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB))
                img_bgr = pil_img.convert("P", palette=Image.ADAPTIVE, colors=256)      # set to native 8 Bit
                img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)                         
                imgxs = cv2.resize(img_bgr, (640, 360), interpolation=cv2.INTER_CUBIC)  # set to native render resolution
                print("[INFO] Processing Frontend - Rescaling FHD")
                save_path = os.path.join("rescaled_image.png")
                cv2.imwrite(save_path, imgxs)
                print("[INFO] Image Saved at", save_path)
                return imgxs

    def process_screenshot(img):
        coords_equi = [(20, 127), (20, 166), (20, 205), (20, 244)]
        coords_inve = [(106, 127), (145, 127), (184, 127), (223, 127), (262, 127), (106, 166), (145, 166), (184, 166), (223, 166), (262, 166), (106, 205), (145, 205), (184, 205), (223, 205), (262, 205), (106, 244), (145, 243), (184, 243), (223, 244), (262, 244)]
        coords_shop = [(87, 313), (126, 313), (165, 313), (204, 313)]
        snippets = []
        for x, y in coords_equi:
            box = (x, y, x + 26, y + 26)
            icon = img.crop(box)
            FrontendReader.identify("equipped", icon)
        for x, y in coords_inve:
            box = (x, y, x + 26, y + 26)
            icon = img.crop(box)
            FrontendReader.identify("inventory", icon)
        for x, y in coords_shop:
            box = (x, y, x + 26, y + 26)
            icon = img.crop(box)
            FrontendReader.identify("shop", icon)

    def identify(pos, icon):
        if pos == "equipped":
            pass
        if pos == "inventory":
            pass
        if pos == "shop":
            pass

if __name__ == "__main__":
    print("[INFO] Starting")
    while True:
        if "Megaloot" == win32gui.GetWindowText(win32gui.GetForegroundWindow()):
            print("[INFO] Frontend captured")
            img = FrontendReader.capture_screenshot()
            print("[INFO] Frontend captured")
            FrontendReader.process_screenshot(img)
            print("[INFO] Icons processed")
            sleep(1)
        else:
            sleep(1)