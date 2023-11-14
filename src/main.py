"""
My first machine learning program, I love this ♥
"""
import requests
import csv
import pandas as pd
import random

from src.EtatPartie import EtatPartie
from src.GameData import GameData

url = "http://localhost:3000/"
partie = EtatPartie("", 0)
data = GameData(0, 0, 0, 0)
datafilepath = "../data/game_data.csv"
file = open(datafilepath, "a", newline='')
writer = csv.writer(file)
call = requests.session()


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
        num_lines = len(datafile)
    except pd.errors.EmptyDataError:
        num_lines = 0

    if num_lines == 0:
        writer.writerow(["Total games played", "Session games played", "Wins", "Loses"])
        data.total_games_played = 0
    elif num_lines != 1:
        final = datafile.iloc[-1]["Total games played"]
        data.total_games_played = final


def session():
    """
    One game session, lasts while player still have money to play
    """
    while 1:
        load()
        while not partie.is_lose():
            play()
        save_to_file()


def play():
    """
    One game, hit or hold is set randomly, will be upgraded to be smarter in the future
    Also, print game result
    :return:
    """
    new_deal()
    while partie.state == "IN_GAME":
        calltype = "hit" if random.getrandbits(1) == 1 else "hold"
        response = call.post(url + calltype, headers={'Accept': 'application/json'}).json()
        if calltype == "hold":
            partie.add_dealer_card((response["dealerHand"][-1]["rank"]))
        else:
            partie.add_player_card(response["playerHand"][-1]["rank"])
        if partie.is_flag():
            response = requests.post(url + "flag")
            print(response)
            input()
        partie.state = response["state"]
    update_data()
    print(partie)


def new_deal():
    """
    Create a new deal for a game.
    :return:
    """
    partie.clear_partie()
    deal = call.post(url + "deal", json={'bet': 50}).json()
    partie.add_dealer_card(deal["dealerHand"][0]["rank"])
    partie.cash = deal["cash"]
    partie.state = deal["state"]
    for card in deal["playerHand"]:
        partie.add_player_card(card["rank"])


def save_to_file():
    """
    Save game data in the .csv file. Called once per session
    :return:
    """
    print("Saving data state")
    writer.writerow(data.get_game_data())


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
    print("Loaded new game session")


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


if __name__ == '__main__':
    main()
