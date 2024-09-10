import time
import win32gui
import FrontendReader

if __name__ == "__main__":
    print("[INFO] Starting")
    while True:
        if "Megaloot" == win32gui.GetWindowText(win32gui.GetForegroundWindow()):
            print("[INFO] Frontend captured")
            img = FrontendReader.capture_screenshot()
            FrontendReader.process_screenshot(img)
            print("[INFO] Icons processed")
            time.sleep(1)
        else:
            time.sleep(1)
