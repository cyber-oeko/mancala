from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
    QVBoxLayout, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui
import requests
import time
import sys
import os
from mancala.config import *
from mancala.gui import Window

App = QApplication(sys.argv)


class MenuWindow(QDialog):
    def __init__(self):
        super().__init__()
        print(__file__)
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(__file__) + '/assets/marbles_large/4.png'))
        self.title = TITLE
        self.top = 50
        self.left = 50
        self.width = 400
        self.height = 200
        self.InitWindow()

        self.waiting_game_id = None

        self.createFormGroupBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.layout = mainLayout


    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        self.url_textbox = QLineEdit(URL_DEFAULT)
        self.player_textbox = QLineEdit()
        self.game_textbox = QLineEdit()
        self.checkbox = QCheckBox()
        layout.addRow(QLabel("Server URL:"), self.url_textbox)
        layout.addRow(QLabel("User name:"), self.player_textbox)
        layout.addRow(QLabel("Join game:"), self.checkbox)
        layout.addRow(QLabel("Game ID:"), self.game_textbox)
        self.game_textbox.setEnabled(self.checkbox.checkState() != Qt.Unchecked)
        self.checkbox.stateChanged.connect(self.checkBoxClick)
        qssfile = open(os.path.dirname(__file__) + "/style/menu.qss").read()
        self.game_textbox.setStyleSheet(qssfile)
        self.formGroupBox.setLayout(layout)

    def checkBoxClick(self):
        self.game_textbox.setEnabled(self.checkbox.checkState() != Qt.Unchecked)

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: #8E9B90;")
        self.show()

    def accept(self):
        player_name = self.player_textbox.text()
        game_name = self.game_textbox.text()
        checked = self.checkbox.checkState() != Qt.Unchecked
        url = self.url_textbox.text()
        if game_name == "":
            if not checked:
                self.start_game(player_name, url)
        else:
            if checked:
                self.start_game(player_name, url, game_name)

    def check_other_player_joined(self):
        game_id = self.waiting_game_id
        name = self.waiting_name
        response = requests.get(self.waiting_url + "?game_id={}&check_joined".format(game_id))
        player2 = response.json()["player2"]
        if player2:
            window = Window(0, game_id, name, player2, self.waiting_url)
            self.timer.stop()
            self.close()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.print_game_id(self.waiting_game_id, qp)
        qp.end()

    def print_game_id(self, game_id, painter):
        global App
        if game_id:
            self.clearLayout()
            painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

            painter.setPen(QtGui.QPen(QtGui.QColor(182, 196, 162), 1))
            painter.setFont(QtGui.QFont("Futura", 40))
            painter.drawText(150, 120, str(game_id))
            App.setOverrideCursor(Qt.WaitCursor)

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def start_game(self, name, url, game=None):
        if not game:
            data = {"write": "newgame", "player": name}
            response = requests.post(url, json=data)
            print(response.content)
            self.waiting_game_id = response.json()["game_id"]
            self.waiting_name = name
            self.waiting_url = url
            self.update()
            print("GAME ID: {}".format(self.waiting_game_id))
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.check_other_player_joined)
            self.timer.start(1000)

        else:
            data = {"write": "joingame", "player": name, "game_id": game}
            response = requests.post(url, json=data)
            if "player1" in response.json():
                player1 = response.json()["player1"]
                window = Window(1, game, player1, name, url)
                self.close()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText("Game not found")
                msg.setWindowTitle("Error")
                msg.exec_()

menu_window = MenuWindow()

sys.exit(App.exec())

