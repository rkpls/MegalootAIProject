import gym
from gym import spaces
import numpy as np
from IOControl import IOControl
from FrontendReader import FrontendReader
from TooltipReader import TooltipReader
from DataManager import DataManager

class GameEnv(gym.Env):
    def __init__(self):
        super(GameEnv, self).__init__()
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(low=0, high=100, shape=(10,), dtype=np.float32)

    def get_game_state():
        gold = FrontendReader.get_gold()
        max_life, armor, atack, misc = DataManager.get_stats()
        amount_equipped = DataManager.get_equipped()
        value_equipped = DataManager.get_value_equipped()
        return np.array([gold, max_life, armor, atack, misc, amount_equipped, value_equipped])
    
    def calculate_reward():
        if FrontendReader.next_floor():
            return 20
        next_fight, fight_number = FrontendReader.next_fight()
        if next_fight: 
            return 2
    
    def check_game_over():
        if FrontendReader.is_dead():
            return True
        return False

    def reset(self):
        DataManager.reset_temp_file()
        IOControl.start_game()
        self.state = None
        return self.state

    def step(self, action, id):
        if action == 0:
            print("[INFO] Attack!")
            IOControl.fight()
        elif action == 1:
            print("[INFO] Selecting target!")
            IOControl.choose_enemy()
        elif action == 2:
            print("[INFO] Going shopping!")
            IOControl.buy_item(id)
        elif action == 3:
            print("[INFO] Selling the garbage!")
            IOControl.sell(id)
        elif action == 4:
            print("[INFO] Upgrading my gear!")
            IOControl.equip(id)
        elif action == 5:
            print("[INFO] Fusing items!")
            IOControl.fusing(id)
        elif action == 6:
            print("[INFO] Checking on item!")
            IOControl.check_item(id)
            id, icon, data = FrontendReader.capture_item(id)
            if not data:
                id, name, rarity, i_class, price, gold_factor, data = TooltipReader.analyze(id)
            id, name, rarity, i_class, price, gold_factor, data = TooltipReader.analyze(id)
            if id > 27:
                DataManager.save_permanent(icon, name, rarity, i_class, price, gold_factor, data)
                DataManager.save_temporary(id, name, rarity, i_class, gold_factor, data)
            else:
                DataManager.save_temporary(id, name, rarity, i_class, gold_factor, data)
        elif action == 7:
            IOControl.smelting(id)
        
        
        new_state = self.get_game_state()
        reward = self.calculate_reward()
        done = self.check_game_over()
        
        return new_state, reward, done
