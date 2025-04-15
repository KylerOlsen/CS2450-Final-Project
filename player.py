# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socket import SocketIO


class Player:

    __name: str
    __verse: str
    __score: int
    __server: SocketIO | None

    def __init__(self, name: str):
        self.__name = name
        self.__verse = ""
        self.__score = 0
        self.__server = None

    def join_game(self):
        pass

    def start_game(self):
        pass

    def guess_referene(self, ref: str):
        pass

    def new_round(self, difficulty: int):
        pass

    def end_game(self):
        pass

    def player_joined(self, name: str):
        pass

    def new_verse(self, text: str):
        pass

    def guess_incorrect(self):
        pass

    def guess_correct(self, points: int):
        pass

    def verse_guessed(self, url: str, player: str):
        pass

    def game_over(self, players: list[str], scores: list[int]):
        pass

