import pandas as pd
import csv

from EtatUnique import EtatUnique


class LearningManager:

    def __init__(self):
        self.learnfilepath = "../data/learn_data.csv"
        self.learn_file = open(self.learnfilepath, "a", newline='')
        self.learn_writer = csv.writer(self.learn_file)
        self.data = {}

        try:
            self.learnfile = pd.read_csv(self.learnfilepath)
            num_lines_learn = len(self.learnfile)
            print(f'Loaded file of {num_lines_learn} lines')
        except pd.errors.EmptyDataError:
            num_lines_learn = -1
            print("failed")

        if num_lines_learn == -1:
            self.learn_writer.writerow(["hash_cards", "dealer_points", "player_points", "action", "wins", "loses"])
        else:
            self.load()

        input()


    def load(self):
        for line in self.learnfile.itertuples(index=False):
            self.set_data_to_array(line)

    def set_data_to_array(self, data):
        print(data)
        new_data = EtatUnique(data[1], data[2], data[3], data[4], data[5])
        self.data[new_data.get_hashed_game_status()] = new_data

    def exists(self, hashed_data):
        return hashed_data in self.data.keys()

    def create_new_entry(self, etat: EtatUnique):
        self.data[etat.get_hashed_game_status()] = etat

    def win_game(self, etat: EtatUnique):
        if not self.exists(etat.get_hashed_game_status()):
            self.create_new_entry(etat)

        self.data.get(etat.get_hashed_game_status()).win()

    def lose_game(self, etat: EtatUnique):
        if not self.exists(etat.get_hashed_game_status()):
            self.create_new_entry(etat)

        self.data.get(etat.get_hashed_game_status()).lose()


    def save(self):
        row = 1
        print("Save called")
        self.learn_file.seek(0)
        self.learn_file.truncate()
        self.learn_writer.writerow(["hash_cards", "dealer_points", "player_points", "action", "wins", "loses"])
        for item in self.data.values():
            print(f"saved {item.get_game_status()}")
            self.learn_writer.writerow(item.get_game_status())
            row += 1

