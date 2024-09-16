import json
import tensorforce
from tensorforce.environments import Environment
import FrontendReader
import DataManager
import IOControl

class GameEnv(Environment):
    def __init__(self):
        super().__init__()
        # Initialize state variables
        self.gold = FrontendReader.cash()  # Gold for purchasing items
        self.amount_equipped = DataManager.get_equipped()  # Amount of items equipped
        self.amount_inventory = DataManager.get_inventory()  # Number of items in inventory
        self.value_equipped = DataManager.value_equipped()  # Value of equipped items
        self.value_inventory = DataManager.value_inventory()  # Value of inventory items
        self.next_floor, self.floor_number = FrontendReader.next_floor()  # Floor progress
        self.next_fight, self.fight_number = FrontendReader.next_fight()  # Fight progress
        
        self.done = False  # Track whether the game is over
        self.state = self.get_current_state()  # Initialize the state

    def get_current_state(self):
        # Collect game state as an observation
        return {
            'gold': self.gold,
            'amount_equipped': self.amount_equipped,
            'amount_inventory': self.amount_inventory,
            'value_equipped': self.value_equipped,
            'value_inventory': self.value_inventory,
            'floor_number': self.floor_number,
            'fight_number': self.fight_number
        }

    def reset(self):
        # Reset the game from defeat screen
        DataManager.reset_temp_file()
        IOControl.retry()
        self.done = False
        self.state = self.get_current_state()
        return self.state

    def states(self):
        # Define the structure of the state (observation)
        return dict(type='float', shape=(7,))

    def actions(self):
        # Define the actions space (Buy, reroll, sell, fuse, equip, smelt)
        return dict(type='int', num_values=6)  # Six possible actions (0-5)

    def execute(self, actions):
        # Execute the action chosen by the AI
        if actions == 0:  # Buy item
            item_id = self.choose_item_to_buy()
            IOControl.buy_item(item_id)
        elif actions == 1:  # Reroll shop
            IOControl.reroll()
        elif actions == 2:  # Sell item
            item_id = self.choose_item_to_sell()
            IOControl.sell(item_id)
        elif actions == 3:  # Fuse items
            item_id = self.choose_item_to_fuse()
            IOControl.fusing(item_id)
        elif actions == 4:  # Equip item
            item_id = self.choose_item_to_equip()
            IOControl.equip(item_id)
        elif actions == 5:  # Smelt item
            item_id = self.choose_item_to_smelt()
            IOControl.smelting(item_id)

        # After each action, refresh the state with new data
        FrontendReader.identify_all()
        self.gold = FrontendReader.cash()
        
        # Update fight/floor progress after every action
        self.next_fight, self.fight_number = FrontendReader.next_fight()
        self.next_floor, self.floor_number = FrontendReader.next_floor()
        
        # Check if the game is over
        self.done = FrontendReader.is_dead()
        
        # Define reward structure (this can be further refined)
        reward = self.calculate_reward()

        # Get new game state after action
        self.state = self.get_current_state()

        return self.state, self.done, reward

    def calculate_reward(self):
        # Example reward function based on game state (you can refine this)
        if self.next_fight:
            return 10  # Positive reward if the next fight gives a reward
        if self.floor_number == 11 and self.fight_number == 12:
            return 50  # Large reward for smelting after fight 12
        if self.done:
            return -100  # Large penalty for game over
        return 1  # Small reward for surviving each step

    # Helper functions for item selection logic
    def choose_item_to_buy(self):
        # Logic to choose the best item to buy from data/temp.json
        with open('data/temp.json') as f:
            shop_items = json.load(f)
        best_item = max(shop_items[28:32], key=lambda item: item['stats']['attack damage'])  # Example: choose highest damage item
        return best_item['id']

    def choose_item_to_sell(self):
        # Logic to choose the worst item to sell
        with open('data/temp.json') as f:
            inventory_items = json.load(f)
        worst_item = min(inventory_items[0:28], key=lambda item: item['value'])  # Example: sell lowest value item
        return worst_item['id']

    def choose_item_to_fuse(self):
        # Logic to find duplicates and fuse
        with open('data/temp.json') as f:
            inventory_items = json.load(f)
        duplicates = [item for item in inventory_items if item['name'] == 'some_name' and item['rarity'] == 'some_rarity']
        if len(duplicates) > 1:
            return duplicates[1]['id']  # Fuse with the second duplicate
        return None

    def choose_item_to_equip(self):
        # Logic to equip the best available item
        with open('data/temp.json') as f:
            inventory_items = json.load(f)
        best_item = max(inventory_items[8:28], key=lambda item: item['stats']['attack damage'])  # Equip highest damage item
        return best_item['id']

    def choose_item_to_smelt(self):
        # Logic to choose an item to smelt
        with open('data/temp.json') as f:
            inventory_items = json.load(f)
        worst_item = min(inventory_items[0:28], key=lambda item: item['value'])  # Example: smelt lowest value item
        return worst_item['id']
