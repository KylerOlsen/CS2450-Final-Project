# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from game import Game


class Library:

    __verses: dict
    __games: list[Game]

    def __init__(self):
        with open("data/scripture-frequencies.json", encoding='utf-8') as file:
            self.__verses = json.load(file)
        self.__games = []

    def join_game(self, name: str, game_num: int = -1):
        if game_num == -1:
            for i, game in enumerate(self.__games):
                if not game.active:
                    game_num = i
                    break
            else:
                self.__games.append(Game())
                game_num = len(self.__games) - 1
        self.__games[game_num].add_player(name)

    def get_verse(self, difficulty: int):
        pass

    def __select_verse(self, difficulty: int) -> str:
        pass

    def __get_verse_text(self, url: str) -> str:
        pass

    def __get_verses_by_difficulty(self, difficulty: int) -> list[str]:
        pass

