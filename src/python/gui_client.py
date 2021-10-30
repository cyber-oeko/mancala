from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
    QVBoxLayout, QCheckBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui
import requests
import time
import sys
from config import *
from gui import Window

App = QApplication(sys.argv)


class MenuWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('marbles_large/4.png'))
        self.title = TITLE
        self.top = 50
        self.left = 50
        self.width = 400
        self.height = 200
        self.InitWindow()

        self.createFormGroupBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)


    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        self.game_textbox = QLineEdit()
        self.checkbox = QCheckBox()
        layout.addRow(QLabel("User name:"), QLineEdit())
        layout.addRow(QLabel("Game name:"), self.game_textbox)
        layout.addRow(QLabel("Create game:"), self.checkbox)
        self.game_textbox.setEnabled(self.checkbox.checkState() != Qt.Unchecked)
        self.checkbox.stateChanged.connect(self.checkBoxClick)
        self.formGroupBox.setLayout(layout)

    def checkBoxClick(self):
        self.game_textbox.setEnabled(self.checkbox.checkState() != Qt.Unchecked)

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: #8E9B90;")
        self.show()

    def start_game(self, player_name, game=None):
        if not game:
            data = {"write": "newgame", "player": name}
            response = requests.post(API_URL, json=data)
            game_id = response.json()["game_id"]
#            print("GAME ID: {}".format(game_id))

            while(True):
                response = requests.get(API_URL + "?game_id={}&check_joined".format(game_id))
                player2 = response.json()["player2"]
                if player2:
                    break
                time.sleep(0.2)
            window = Window(0, game_id, name, player2)
            self.close()
        else:
            data = {"write": "joingame", "player": name, "game_id": game}
            response = requests.post(API_URL, json=data)
            player1 = response.json()["player1"]
            window = Window(1, game, player1, name)
            self.close()

menu_window = MenuWindow()

sys.exit(App.exec())

