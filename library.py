# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
from typing import TYPE_CHECKING
import json
import random

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
        print(self.__select_verse(difficulty))

    def __select_verse(self, difficulty: int) -> str:

        difficulty_verses = self.__get_verses_by_difficulty(difficulty)

        # print(len(difficulty_verses))

        return difficulty_verses[random.randint(0,len(difficulty_verses)-1)]

    def __get_verse_text(self, url: str) -> str:
        volume, book, chapter, verse = url[1:].split('/')

        if volume == 'ot': pass
        elif volume == 'nt': pass
        elif volume == 'bofm': pass
        elif volume == 'dc-testament': pass
        elif volume == 'pgp': pass

    def __get_verses_by_difficulty(self, difficulty: int) -> list[str]:
        real_difficulty_upper = pow((10-difficulty)/9, 2) * 500
        real_difficulty_lower = pow((9-difficulty)/9.55, 3) * 500

        difficulty_verses = []
        for key, value in self.__verses.items():
            for i, diff in enumerate(value):
                if real_difficulty_lower <= diff <= real_difficulty_upper:
                    difficulty_verses.append(f"{key}/{i}")

        return difficulty_verses


if __name__ == '__main__':

    lib = Library()
    for i in range(11): lib.get_verse(i)
