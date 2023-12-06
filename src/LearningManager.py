import random
import pandas as pd
import csv
from EtatUnique import EtatUnique


def get_win_count(state_hit: EtatUnique, state_hold: EtatUnique):
    """
    Obtient le pourcentage de victoire suivant un état différent
    :param state_hit: Statistiques de hit
    :param state_hold: Statistique de hold
    :return: hit_p pourcentage de victoire en hit
    :return: hold_p pourcentage de victoire en hold
    """
    hit_wins = state_hit.wins if state_hit is not None else 0
    hold_wins = state_hold.wins if state_hold is not None else 0
    game_played = hit_wins + hold_wins + 20

    hit_p = (hit_wins + 10) / game_played * 100
    hold_p = (hold_wins + 10) / game_played * 100

    return hit_p, hold_p


class LearningManager:
    """
    Classe permettant la gestion de l'apprentissage
    """

    def __init__(self):
        self.learnfilepath = "../data/learn_data.csv"
        self.learn_file = open(self.learnfilepath, "a", newline='')
        self.learn_writer = csv.writer(self.learn_file)
        self.data = {}
        self.newdata = 0

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

    def load(self):
        """
        Charge les données dans le dictionnaire d'apprentissage
        :return: void
        """
        for line in self.learnfile.itertuples(index=False):
            self.set_data_to_array(line)

    def set_data_to_array(self, data):
        """
        Transforme une ligne de donnée CSV en Etat Unique
        :param data: Une ligne de données
        :return: void
        """
        new_data = EtatUnique(data[1], data[2], data[3], data[4], data[5], data[6])
        self.data[new_data.get_hashed_game_status()] = new_data


    def create_new_entry(self, etat: EtatUnique):
        """
        Crée une nouvelle donnée dans le dictionnaire
        :param etat: L'état a créer
        :return: void
        """
        self.newdata += 1
        self.data[etat.get_hashed_game_status()] = etat

    def win_game(self, etat: EtatUnique):
        """
        Effectue la vérification d'existence d'une partie, puis ajoute une victoire
        :param etat: L'état de la partie
        :return: void
        """
        try:
            self.data.get(etat.get_hashed_game_status()).win()
        except AttributeError:
            self.create_new_entry(etat)
            self.data.get(etat.get_hashed_game_status()).win()

    def lose_game(self, etat: EtatUnique):
        """
        Effectue la vérification d'existence d'une partie, puis ajoute une défaite
        :param etat: L'état de la partie
        :return: void
        """
        try:
            self.data.get(etat.get_hashed_game_status()).lose()
        except AttributeError:
            self.create_new_entry(etat)
            self.data.get(etat.get_hashed_game_status()).lose()

    def best_decision(self, etat: EtatUnique):
        """
        Vient définir la meilleure décision a prendre, peut être hit ou hold
        :param etat: L'état de la partie
        :return: String "Hit" ou "Hold"
        """
        if etat.player_points >= 20:
            choice = "hold"
        elif etat.player_points < 11:
            choice = "hit"
        else:
            hit_state = EtatUnique(etat.dealer_points, etat.player_points, "hit", deck=etat.deck)
            hold_state = EtatUnique(etat.dealer_points, etat.player_points, "hold", deck=etat.deck)
            data_hit_state = self.data.get(hit_state.get_hashed_game_status())
            data_hold_state = self.data.get(hold_state.get_hashed_game_status())
            (hit, hold) = get_win_count(data_hit_state, data_hold_state)
            rng = random.random() * 100

            choice = "hit" if rng < hit else "hold"
        return choice

    def save(self):
        """
        Sauvegarde l'état de l'apprentissage dans un CSV
        """
        self.learn_file.seek(0)
        self.learn_file.truncate()
        self.learn_writer.writerow(["hash_cards", "dealer_points", "player_points", "action", "wins", "loses", "deck"])
        for item in self.data.values():
            self.learn_writer.writerow(item.get_game_status())
        print("Saved learning state")


    def reset_new_data(self):
        self.newdata = 0