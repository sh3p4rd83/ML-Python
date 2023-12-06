"""
My first machine learning program, I love this ♥
"""
import sys

import requests
import csv
import pandas as pd

from src.Deck import Deck
from src.EtatPartie import EtatPartie
from src.EtatUnique import EtatUnique
from src.GameData import GameData
from src.LearningManager import LearningManager

url = "http://localhost:3000/"
partie = EtatPartie("", 0)
data = GameData(0, 0, 0, 0)
datafilepath = "../data/game_data.csv"
data_file = open(datafilepath, "a", newline='')
data_writer = csv.writer(data_file)
call = requests.session()
manager = LearningManager()
deck = Deck()

# Defini le nombre de sessions qui doivent être jouées avant de sauvegarder les données
session_save = 100

# Defini le nombre de sessions qui doivent être jouées avant de faire l'affichage des données
session_print = 50

printer_data_winrate = []
printer_data_games = []
printer_data_new = []
states = []


def main():
    """
    Program entry point
    """
    init()
    session()


def init():
    """
    Init data file. If no data exists, create headers, if it does, set total games played as last line amount
    """
    try:
        datafile = pd.read_csv(datafilepath)
        num_lines_data = len(datafile)
    except pd.errors.EmptyDataError:
        num_lines_data = 0

    if num_lines_data == 0:
        data_writer.writerow(["Total games played", "Session games played", "Wins", "Loses"])
        data.total_games_played = 0
    elif num_lines_data != 1:
        final = datafile.iloc[-1]["Total games played"]
        data.total_games_played = final


def session():
    """
    One game session, lasts while player still have money to play
    """
    session_played_print = 0
    session_played_save = 0
    while 1:
        deck.reset()
        load()
        while not partie.is_lose():
            if partie.is_flag():
                print("FLAG")  # PMC pourquoi ne print tu pas le flag pour vrai en faisant un POST sur /flag et en printant la réponse
            play()
        save_to_file()
        session_played_print += 1
        session_played_save += 1

        if session_played_print >= session_print:
            printer()
            session_played_print = 0

        printer_data_winrate.append(data.wins / data.session_games_played * 100)
        printer_data_games.append(data.session_games_played)
        printer_data_new.append(manager.newdata)
        manager.reset_new_data()

        if session_played_save >= 50:
            manager.save()
            session_played_save = 0


def printer():
    max_data_new = 0
    min_data_new = 100000

    max_data_games = 0
    min_data_games = 100000

    max_data_wins = 0
    min_data_wins = 100

    for data_ in printer_data_new:
        if data_ > max_data_new:
            max_data_new = data_
        if data_ < min_data_new:
            min_data_new = data_
    for data_ in printer_data_games:
        if data_ > max_data_games:
            max_data_games = data_
        if data_ < min_data_games:
            min_data_games = data_
    for data_ in printer_data_winrate:
        if data_ > max_data_wins:
            max_data_wins = data_
        if data_ < min_data_wins:
            min_data_wins = data_

    print(f" DATA FROM LAST {session_print} GAMES ".center(100, '='))
    print()
    print(f"Games:".center(100, "-"))
    print(f"Played: {sum(printer_data_games)} total games played".center(100, ' '))
    print(f"Max: {max_data_games} games played".center(100, ' '))
    print(f"Min: {min_data_games} games played".center(100, ' '))
    print(f"Avg: {sum(printer_data_games) / len(printer_data_games)}".center(100, ' '))
    print()
    if sum(printer_data_new) == 0:
        print("No new data found, hurray !")
    else:
        print(f"New data:".center(100, "-"))
        print(f"Played: {sum(printer_data_new)} total new data found".center(100, ' '))
        print(f"Max: {max_data_new} new data".center(100, ' '))
        print(f"Min: {min_data_new} new data".center(100, ' '))
        print(f"Avg: {sum(printer_data_new) / len(printer_data_new)}".center(100, ' '))
    print()
    print(f"Winrate:".center(100, "-"))
    print(f"Max: {max_data_wins}% wins.".center(100, ' '))
    print(f"Min: {min_data_wins}% wins.".center(100, ' '))
    print(f"Avg: {sum(printer_data_winrate) / len(printer_data_winrate)}%".center(100, ' '))
    print()
    print(f"".center(100, '='))
    print()

    printer_data_games.clear()
    printer_data_new.clear()
    printer_data_winrate.clear()


def play():
    """
    One game, hit or hold is set randomly, will be upgraded to be smarter in the future
    Also, print game result
    :return:
    """
    new_deal()
    states.clear()
    while partie.state == "IN_GAME":
        player_sum = partie.sum_player()
        dealer_sum = partie.sum_dealer()
        etat = EtatUnique(dealer_sum, player_sum, "", deck=deck.print_deck())
        calltype = manager.best_decision(etat)
        etat.action = calltype
        states.append(etat)
        response = call.post(url + calltype, headers={'Accept': 'application/json'}).json()
        if calltype == "hold":
            for i in response["dealerHand"][1:]:
                partie.add_dealer_card(i["rank"])
                deck.remove_card(i["rank"])
        else:
            player_card = response["playerHand"][-1]["rank"]
            partie.add_player_card(player_card)
            deck.remove_card(player_card)

        partie.state = response["state"]
    update_data()
    # print(partie)


def new_deal():
    """
    Create a new deal for a game.
    :return:
    """
    if deck.count_cards() < 18:
        deck.reset()
    partie.clear_partie()
    deal = call.post(url + "deal", json={'bet': 50}).json()
    dealer_card = deal["dealerHand"][0]["rank"]
    partie.add_dealer_card(dealer_card)
    deck.remove_card(dealer_card)

    partie.cash = deal["cash"]
    partie.state = deal["state"]
    for card in deal["playerHand"]:
        player_card = card["rank"]
        partie.add_player_card(player_card)
        deck.remove_card(player_card)


def save_to_file():
    """
    Save game data in the .csv file. Called once per session
    :return:
    """
    data_writer.writerow(data.get_game_data())


def load():
    """
    Load a new game, called when a new session start.
    :return:
    """
    call.cookies.clear()
    response = call.get(url + "load").json()
    partie.cash = response["cash"]
    partie.state = response["state"]
    data.session_games_played = 0
    data.wins = 0
    data.loses = 0


def update_data():
    """
    Update data when game is over.
    :return:
    """
    data.play_game()
    if partie.state == "WON":
        data.win_game()
    if partie.state == "LOST":
        data.lose_game()
    for s in states:
        if partie.state == "WON":
            manager.win_game(s)
        if partie.state == "LOST":
            manager.lose_game(s)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        manager.save()
        sys.exit(0)
