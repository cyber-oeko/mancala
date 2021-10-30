from PyQt5.QtWidgets import QApplication
import requests
import argparse
import time
import sys
from config import *
from gui import Window

parser = argparse.ArgumentParser(description='Start the Steinchenspiel game.')
parser.add_argument("name", type=str, help="choose a name")
parser.add_argument("--game", type=int, help="if joining a game, enter game id")

args = parser.parse_args()

App = QApplication(sys.argv)
if not args.game:
    data = {"write": "newgame", "player": args.name}
    response = requests.post(API_URL, json=data)
    game_id = response.json()["game_id"]
    print("GAME ID: {}".format(game_id))

    while(True):
        response = requests.get(API_URL + "?game_id={}&check_joined".format(game_id))
        player2 = response.json()["player2"]
        if player2:
            break
        time.sleep(0.2)
    window = Window(0, game_id, args.name, player2)
else:
    data = {"write": "joingame", "player": args.name, "game_id": args.game}
    response = requests.post(API_URL, json=data)
    player1 = response.json()["player1"]
    window = Window(1, args.game, player1, args.name)


sys.exit(App.exec())
