from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPixmap, QMouseEvent, QFont
from PyQt5.QtCore import Qt, QTimer
import random
import numpy as np
from mancala.game import Game, GameState
from mancala.config import *
from mancala.helper import get_marble_positions, get_hole_positions
import sys
import os
import requests
import time


class Window(QMainWindow):
    def __init__(self, player_id, game_id, player1_name, player2_name, url):
        super().__init__()
        self.url = url
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(__file__) + '/assets/marbles_large/14.png'))
        self.game = Game(self)
        self.player_id = player_id
        self.game_id = game_id
        self.player_names = (player1_name, player2_name)
        self.title = TITLE
        self.top = 500*self.player_id
        self.left = 0
        self.width = (CIRCLE_RADIUS + HOLE_PADDING) * 2 * (1+self.game.width)
        self.height = (CIRCLE_RADIUS + HOLE_PADDING) * 8 + MID_PADDING
        self.InitWindow()
        self.directions = np.random.rand(4 * self.game.width) * 2 * np.pi
        self.start_hole_waiting = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_answer)
        self.move_id = -1
        QApplication.instance().setOverrideCursor(Qt.ArrowCursor)
        self.timer.start(500)

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: #8E9B90;")
        self.show()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setPen(QPen(0))

        if self.player_id == self.game.active_player:
            board = self.game.get_flipped()
        else:
            board = self.game.board
        for i in range(4):
            for j in range(self.game.width):
                x, y = get_hole_positions(i, j)
                if self.player_id == self.game.active_player:
                    hole = self.get_swap_coords(i, j)
                else:
                    hole = [i, j]
                if hole == self.game.active_hole:
                    painter.setBrush(QBrush(QColor(212, 205, 171), Qt.SolidPattern))
                elif hole == self.game.take_hole:
                    painter.setBrush(QBrush(QColor(205, 173, 180), Qt.SolidPattern))
                elif hole == self.start_hole_waiting:
                    painter.setBrush(QBrush(QColor(212, 205, 171), Qt.SolidPattern))
                else:
                    painter.setBrush(QBrush(QColor(147, 192, 164), Qt.SolidPattern))

                painter.drawEllipse(x, y, CIRCLE_RADIUS*2, CIRCLE_RADIUS*2)

                marbles = board[i, j]
                positions = get_marble_positions(len(marbles), i*self.game.width+j, self.directions)
                for k, pos in enumerate(positions):
                    marble = marbles[k]
                    marble_img = QPixmap(os.path.dirname(__file__) + "/assets/marbles/{}.png".format(marble))
                    painter.drawPixmap(x+pos[0], y+pos[1], MARBLE_SIZE, MARBLE_SIZE, marble_img)

        marbles = self.game.inventory
        x = self.game.width * (CIRCLE_RADIUS + HOLE_PADDING) * 2 + HOLE_PADDING
        y = (CIRCLE_RADIUS + HOLE_PADDING) * 2 * 1.5 + MID_PADDING / 2 + HOLE_PADDING
        painter.setBrush(QBrush(QColor(182, 196, 162), Qt.SolidPattern))
        painter.drawEllipse(x, y, CIRCLE_RADIUS*2, CIRCLE_RADIUS*2)
        positions = get_marble_positions(len(marbles), i*self.game.width+j, self.directions)
        for k, pos in enumerate(positions):
            marble = marbles[k]
            marble_img = QPixmap(os.path.dirname(__file__) + "/assets/marbles/{}.png".format(marble))
            painter.drawPixmap(x+pos[0], y+pos[1], MARBLE_SIZE, MARBLE_SIZE, marble_img)
        self.draw_text(0, painter)
        self.draw_text(1, painter)

    def draw_text(self, player_id, painter):
        if self.game.active_player == player_id:
            painter.setPen(QPen(QColor(212, 205, 171), 1))
        else:
            painter.setPen(QPen(QColor(182, 196, 162), 1))
        painter.setFont(QFont("Futura", FONT_SIZE))
        x = self.game.width * (CIRCLE_RADIUS + HOLE_PADDING) * 2 + HOLE_PADDING
        if not self.player_id == player_id:
            y = HOLE_PADDING + CIRCLE_RADIUS
            painter.drawText(x, y, self.player_names[(self.player_id+1)%2])
        else:
            y = self.height - HOLE_PADDING - CIRCLE_RADIUS
            painter.drawText(x, y, self.player_names[self.player_id])


    def mousePressEvent(self, event: QMouseEvent):
        if not event.button() == Qt.LeftButton:
             return
        for i in range(4):
            for j in range(self.game.width):
                x, y = get_hole_positions(*self.get_swap_coords(i, j))
                x += CIRCLE_RADIUS
                y += CIRCLE_RADIUS
                if (x-event.x())**2 + (y-event.y())**2 < CIRCLE_RADIUS**2:
                    self.hole_click(i, j)
                    return

    def hole_click(self, i, j):
        if not self.player_id == self.game.active_player:
            return
        if self.game.state == GameState.WAITING_FOR_MOVE_DECISION:
            if not self.start_hole_waiting:
                if i < 2 and len(self.game._at([i, j])) > 1:  # TODO: add this rule check also to game!
                    self.start_hole_waiting = [i, j]
                    self.repaint()
            else:
                if self.game._get_next_hole([i, j], 1) == self.start_hole_waiting:
                    i, j = self.start_hole_waiting
                    self.start_hole_waiting = False
                    data = {"write": "move",
                            "game_id": self.game_id,
                            "player": self.player_names[self.player_id],
                            "type": 0,
                            "x": i, "y": j, "data": -1}
                    response = requests.post(self.url, json=data)
                    self.move_id = response.json()["move_id"]
                    self.game.turn(i, j, -1)
                elif self.game._get_next_hole([i, j], -1) == self.start_hole_waiting:
                    i, j = self.start_hole_waiting
                    self.start_hole_waiting = False
                    data = {"write": "move",
                            "game_id": self.game_id,
                            "player": self.player_names[self.player_id],
                            "type": 0,
                            "x": i, "y": j, "data": 1}
                    response = requests.post(self.url, json=data)
                    self.move_id = response.json()["move_id"]
                    self.game.turn(i, j, 1)
                else:
                    self.start_hole_waiting = False
                    self.repaint()
            return
        if self.game.state == GameState.WAITING_FOR_TAKE_DECISION:
            if [i, j] == self.game.active_hole:
                data = {"write": "move",
                        "game_id": self.game_id,
                        "player": self.player_names[self.player_id],
                        "type": 1,
                        "x": i, "y": j, "data": 0}
                is_sent = False
                while not is_sent:
                    try:
                        response = requests.post(self.url, json=data)
                    except:
                        time.sleep(2)
                        response = None
                    if response:
                        is_sent = True
                    else:
                        time.sleep(2)
                self.move_id = response.json()["move_id"]
                self.game.take_decision(False)
            elif [i, j] == self.game.take_hole:
                data = {"write": "move",
                        "game_id": self.game_id,
                        "player": self.player_names[self.player_id],
                        "type": 1,
                        "x": i, "y": j, "data": 1}
                is_sent = False
                while not is_sent:
                    try:
                        response = requests.post(self.url, json=data)
                    except:
                        time.sleep(2)
                        response = None
                    if response:
                        is_sent = True
                    else:
                        time.sleep(2)
                self.move_id = response.json()["move_id"]
                self.game.take_decision(True)
            return


    def check_for_answer(self):
        if self.player_id == self.game.active_player:
            return
        try:
            response = requests.get(self.url + "?game_id={}".format(self.game_id), timeout=5)
        except:
            return
        if int(response.json()["id"]) > self.move_id:
            r = response.json()
            if r["player"] == self.player_names[(self.player_id+1)%2]:
                if self.game.state == GameState.WAITING_FOR_MOVE_DECISION and int(r["type"]) == 0:
                    self.move_id = int(r["id"])
                    self.game.turn(int(r["x"]), int(r["y"]), int(r["data"]))
                    #self.timer.stop()
                elif self.game.state == GameState.WAITING_FOR_TAKE_DECISION and int(r["type"]) == 1:
                    self.move_id = int(r["id"])
                    self.game.take_decision(int(r["data"]))
                    #self.timer.stop()


    def get_swap_coords(self, i, j):
        return [3-i, self.game.width-j-1]

