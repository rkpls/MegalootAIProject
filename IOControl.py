import pyautogui
import pygetwindow as gw
from time import sleep

class IOControl:
    coords_equipped = [(20, 127), (20, 166), (20, 205), (20, 244), (59, 127), (59, 166), (59, 205), (59, 244)]
    coords_inventory = [(106, 127), (145, 127), (184, 127), (223, 127), (262, 127), (106, 166), (145, 166), (184, 166), (223, 166), (262, 166), (106, 205), (145, 205), (184, 205), (223, 205), (262, 205), (106, 244), (145, 243), (184, 243), (223, 244), (262, 244)]
    coords = coords_equipped + coords_inventory
    item_coords = [(x + 13, y + 13) for x, y in coords]
    
    def wait_for_focus():
        active_window = gw.getActiveWindow()
        while not active_window and active_window.title == 'Megaloot':
            sleep(0.1)
        
    def coord_scaling(base_x, base_y):
        window = gw.getWindowsWithTitle('Megaloot')[0]
        app_width = window.width
        app_height = window.height
        g_width, g_height = (640, 360)
        new_x = int(base_x * (app_width / g_width))
        new_y = int(base_y * (app_height / g_height))
        return new_x, new_y
    
    def move_mouse(x, y):
        IOControl.wait_for_focus()
        coords = IOControl.coord_scaling(x,y)
        pyautogui.moveTo(coords)
        
    def buy_item(id):
        print(f"[INFO] Buying Item No. {id - 27}")
        if id == 28:
            pyautogui.press('1')
            sleep(0.1)
        if id == 29:
            pyautogui.press('2')
            sleep(0.1)
        if id == 30:
            pyautogui.press('3')
            sleep(0.1)
        if id == 31:
            pyautogui.press('4')
            sleep(0.1)
    
    def fight():
        print("[INFO] ATTACK!")
        IOControl.move_mouse(520, 320)
        sleep(0.1)
        pyautogui.click(button='left')
        sleep(0.1)
        IOControl.move_mouse(300, 200)
        sleep(1)

    def reroll():
        pyautogui.press('r')
        sleep(0.1)

    def choose_enemy():
        print(f"[INFO] Fighting the other guy")
        pyautogui.press('right')
        sleep(0.1)
    
    def start_game():
        IOControl.move_mouse(484, 312)
        sleep(0.1)
        pyautogui.click(button='left')
        sleep(0.1)
        
    def equip(id):
        print(f"[INFO] Equipping item No. {id}")
        x, y = IOControl.item_coords[id]
        IOControl.move_mouse(x, y)
        sleep(0.1)
        pyautogui.click(button='right')
        sleep(0.1)
        IOControl.move_mouse(300, 200)
        sleep(0.1)

    def fusing(id):
        print(f"[INFO] Fusing item No. {id}")
        x, y = IOControl.item_coords[id]
        IOControl.move_mouse(x, y)
        sleep(0.1)
        pyautogui.click(button='right')
        sleep(0.1)
        IOControl.move_mouse(300, 200)
        sleep(0.1)

    def sell(id):
        print(f"[INFO] Selling item No. {id}")
        x, y = IOControl.item_coords[id]
        IOControl.move_mouse(x, y)
        sleep(0.1)
        pyautogui.click(button='left')
        sleep(0.1)
        pyautogui.click(button='right')
        sleep(0.1)
        IOControl.move_mouse(300, 200)
        sleep(0.1)

    def retry():
        print("[INFO] Trying again")
        IOControl.move_mouse(570, 320)
        sleep(0.1)
        pyautogui.click(button='left')
        sleep(1)
        IOControl.move_mouse(570, 320)
        sleep(0.1)
        pyautogui.click(button='left')  
        sleep(7)
        IOControl.start_game()
        IOControl.move_mouse(300, 200)
        sleep(0.1)

    def check_item(id):
        print(f"[INFO] Checking on item No. {id}")
        x, y = IOControl.item_coords[id]
        IOControl.move_mouse(x, y)
        sleep(1)
        return id
    
    def smelting(id):
        print(f"[INFO] Smelting the item No. {id}")
        x, y = IOControl.item_coords[id]
        IOControl.move_mouse(x, y)
        sleep(0.1)
        pyautogui.click(button='left')
        sleep(0.1)
        IOControl.move_mouse(480, 180)
        sleep(0.1)
        pyautogui.click(button='left')
        sleep(0.1)
        IOControl.move_mouse(480, 240)
        sleep(0.1)
        pyautogui.click(button='left')
        sleep(0.1)

sleep(2)
IOControl.retry()