# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class Library:

    __verses: dict
    __games: Game

    def __init__(self):
        pass

    def join_game(self, name: str):
        pass

    def get_verse(self, difficulty: int):
        pass

    def __select_verse(self, difficulty: int) -> str:
        pass

    def __get_verse_text(self, url: str) -> str:
        pass

    def __get_verses_by_difficulty(self, difficulty: int) -> list[str]:
        pass

