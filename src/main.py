import random
import numpy as np
import pandas as pd
import os
import json
import copy
from collections import defaultdict
from data import item_pools

class Wish:
    def __init__(self, data_path="data"):
        """
        Simulates wishes in Genshin Impact
        """
        self.four_star_pity_counter = 0
        self.five_star_pity_counter = 0
        self.item_pool, self.item_data = self.load_data(data_path)
        self.cumulative_roll_counts = defaultdict(int)
        self.default_item_probabilities = {3: 0.943,
                                           4: 0.051,
                                           5: 0.006}
        self.item_probabilities = copy.deepcopy(self.default_item_probabilities)
            
    def get_roll_summary(self, roll_counts):
        summary = {}
        for item_name, roll_count in roll_counts.items():
            summary[item_name] = {"rarity": self.item_data[item_name]["rarity"],
                                  "count": roll_count,
                                  "item_type": self.item_data[item_name]["item_type"]}
        summary_df = pd.DataFrame(summary).T
        return summary_df
    
    def load_data(self, data_path):
        item_data = {}
        item_pool = defaultdict(list)
        for item in ["weapons", "characters"]:
            item_files = os.listdir("{}/{}".format(data_path, item))
            for file_name in item_files:
                item_file = open("{}/{}/{}".format(data_path, item, file_name))
                data = json.load(item_file)    
                data["item_type"] = item
                is_available = self.check_available_item(data["name"])
                if is_available:
                    item_pool[int(data["rarity"])].append(data["name"])
                    item_data[data["name"]] = data
                item_file.close()
        return item_pool, item_data 

    def check_available_item(self, item_name):
        """
        Allow all items to be available
        """
        return True
    
    def apply_pity(self):
        """
        Returns integer value of 3, 4, or 5,
        the outcome of which will be affected by soft and hard pity rules
        """
        soft_pity_step_size = (1 - 0.006)/(89 - 74)
        if self.five_star_pity_counter >= 74:
            # apply soft pity rules for 5 star
            # - linear increase of probability from 0.06% at 74th roll to 100% at 89th roll 
            # - subtract the probability of 3 star by the same step size
            # - keep the 4 star probability the same
            self.item_probabilities[5] += soft_pity_step_size
            self.item_probabilities[3] -= soft_pity_step_size
        rarity = np.random.choice([3, 4, 5], size=1,
            replace=True, p=[self.item_probabilities[3],
                self.item_probabilities[4],
                self.item_probabilities[5]])[0]
        if rarity < 4 and self.four_star_pity_counter >= 9:
            # hard pity for 4 star
            rarity = 4
        return rarity
    
    def roll(self, n=1):
        """
        Use pity rules and probabilities for getting 3/4/5 star item rarity.
        Based on the item rarity returned, sample from an item pool containing
        weapons and characters of the same rarity. 
        """
        items = []
        roll_counts = defaultdict(int)
        for i in range(n):
            rarity = self.apply_pity()
            item_pool = self.item_pool[rarity]
            item = random.sample(item_pool, 1)
            items.append(item[0])
            roll_counts[item[0]] += 1
            self.cumulative_roll_counts[item[0]] += 1
            if rarity == 3:
                self.four_star_pity_counter += 1
                self.five_star_pity_counter += 1
            elif rarity == 4:
                #  Reset the four start pity counter
                self.four_star_pity_counter = 0
                self.five_star_pity_counter += 1
            else:
                # Does 4 star pity counter reset if 5 star pity resets? 
                # Assume that it doesn't 
                self.five_star_pity_counter = 0
                # Reset the soft-pity affected probability distribution for 3 star/4 star/5 star item rarities
                self.item_probabilities = copy.deepcopy(self.default_item_probabilities)
        self.print_summary_stats(roll_counts)
        return items
    

    def print_summary_stats(self, roll_counts):
        print(self.get_roll_summary(roll_counts))
        print("==================================================")
        for item_rarity, probability in self.item_probabilities.items():
            print("{}* item rate: {}".format(item_rarity, probability))
        print("==================================================")
        cumulative_rolls = sum(self.cumulative_roll_counts.values())
        print("cumulative rolls: {}".format(cumulative_rolls))
        print("primogems: {}".format(160 * cumulative_rolls))
        print("4 star pity count: {}".format(self.four_star_pity_counter))
        print("5 star pity count: {}".format(self.five_star_pity_counter))

    def cost_calculator(self, gems):
        """
        returns the least cost in USD based on the number of gems
        """
        usd_to_gem_conversion = {1: 60,
                                 5: 300,
                                 15: 980,
                                 30: 1980,
                                 50: 3280,
                                 100: 6480}
        [6480, 3280, 1980, 980, 300, 60]
        return

    
class StandardBanner(Wish):
    def __init__(self, **kwargs):
        self.weapons = item_pools.standard_weapons
        self.characters = item_pools.standard_characters
        super().__init__(**kwargs)
        
    def check_available_item(self, item_name):
        """
        generates the character and weapons pool to pull from for
        the standard banner
        """
        item_pool = set(self.weapons + self.characters)
        if item_name in item_pool:
            return True
    

class WeaponBanner(Wish):
    def __init__(self, **kwargs):
        self.version = 2.1
        super().__init__(**kwargs)


class CharacterBanner(Wish):
    def __init__(self, **kwargs):
        self.version = 2.1
        super().__init__(**kwargs)
        

    def get_item_list(self, rarity):
        """
        generates the character and weapons pool to pull from for
        the limited banner
        """
        weapons_list = self.rarity_data["weapons"][rarity]
        characerts_list = self.rarity_data["characters"][rarity]
        item_list = weapons_list + characerts_list
        return item_list



