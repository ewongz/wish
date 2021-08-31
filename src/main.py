import random
import numpy as np
import os
import json
from collections import defaultdict

class Wish:
    def __init__(self, data_path):
        """
        Simulates wishes in Genshin Impact
        """
        self.four_star_pity_counter = 0
        self.five_star_pity_counter = 0
        self.total_rolls = 0
        self.item_data = self.load_data(data_path)
        self.roll_counts = defaultdict(int)
    
    def load_data(self, data_path):
        item_data = {}
        for item in ["weapons", "characters"]:
            rarity_map = defaultdict(list)
            item_files = os.listdir("{}/{}".format(data_path, item))
            for file_name in item_files:
                item_file = open("{}/{}/{}".format(data_path, item, file_name))
                data = json.load(item_file)
                rarity_map[int(data["rarity"])].append((data["name"], int(data["rarity"])))
                item_file.close()
            item_data[item] = rarity_map
        return item_data 
    
    def roll(self, n=1):
        items = []
        for i in range(n):
            if self.five_star_pity_counter == 89:
                result = 5
            elif self.four_star_pity_counter == 9:
                result = 4
            else:
                result = np.random.choice([3, 4, 5], size=1,
                replace=True, p=[0.943, 0.051, 0.006])[0]
            weapons_list = self.item_data["weapons"][result]
            characerts_list = self.item_data["characters"][result]
            item = random.sample(weapons_list + characerts_list, 1)
            items.append(item[0])
            self.roll_counts[item[0]] += 1
            if result == 3:
                self.four_star_pity_counter += 1
                self.five_star_pity_counter += 1
            elif result == 4:
                self.four_star_pity_counter = 0
                self.five_star_pity_counter += 1
            else:
                self.four_star_pity_counter = 0
                self.five_star_pity_counter = 0
        return items
        
        




