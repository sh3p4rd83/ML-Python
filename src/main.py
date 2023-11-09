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
    init()
    session()


def init():
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
    while 1:
        load()
        while not partie.is_lose():
            play()
        save_to_file()


def play():
    new_deal()
    while partie.state == "IN_GAME":
        calltype = "hit" if random.getrandbits(1) == 1 else "hold"
        response = call.post(url + calltype, headers={'Accept': 'application/json'}).json()
        if calltype == "hold":
            partie.add_dealer_card((response["dealerHand"][-1]["rank"]))
        else:
            partie.add_player_card(response["playerHand"][-1]["rank"])
        partie.state = response["state"]
    update_data()
    print(partie)


def new_deal():
    partie.clear_partie()
    deal = call.post(url + "deal", json={'bet': 25}).json()
    partie.add_dealer_card(deal["dealerHand"][0]["rank"])
    partie.cash = deal["cash"]
    partie.state = deal["state"]
    for card in deal["playerHand"]:
        partie.add_player_card(card["rank"])


def save_to_file():
    print("Saving data state")
    writer.writerow(data.get_game_data())


def load():
    call.cookies.clear()
    response = call.get(url + "load").json()
    partie.cash = response["cash"]
    partie.state = response["state"]
    data.session_games_played = 0
    data.wins = 0
    data.loses = 0
    print("Loaded new game session")


def update_data():
    data.play_game()
    if partie.state == "WON":
        data.win_game()
    if partie.state == "LOST":
        data.lose_game()


if __name__ == '__main__':
    main()
