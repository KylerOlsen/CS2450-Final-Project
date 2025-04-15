# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socket import SocketIO

class Game:

    __difficulty: int
    __players: list[str]
    __clients: list[SocketIO]
    __scores: list[int]
    __active: bool
    __finished: bool

    def __init__(self):
        self.__difficulty = 0
        self.__players = []
        self.__clients = []
        self.__scores = []
        self.__active = False
        self.__finished = False

    @property
    def active(self) -> bool: return self.__active

    @property
    def finished(self) -> bool: return self.__finished

    def add_player(self, name: str):
        if not self.__active:
            self.__players.append(name)
            self.__scores.append(0)

    def start_game(self):
        self.__active = True

    def start_round(self, difficulty: int):
        if self.__active and not self.__finished:
            self.__difficulty = difficulty

    def new_verse(self, url: str, text: str):
        pass

    def guess_reference(self, ref: str, player: str):
        pass

    def end_game(self):
        self.__finished = True

