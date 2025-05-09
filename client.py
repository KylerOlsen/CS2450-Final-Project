# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
from typing import TYPE_CHECKING
import socket
import select
import network_utilities

if TYPE_CHECKING:
    from ui import UI


class Game:

    __player: Player
    __server: socket.socket

    def __init__(self, player: Player, server: socket.socket):
        self.__player = player
        self.__server = server

    def start_game(self):
        data = network_utilities.pack_varint(2)
        self.__server.send(data)

    def start_round(self, difficulty: int):
        data = network_utilities.pack_varint(3)
        data += network_utilities.pack_varint(difficulty)
        self.__server.send(data)

    def guess_reference(self, url: str):
        data = network_utilities.pack_varint(4)
        data += network_utilities.pack_string(url)
        self.__server.send(data)

    def end_game(self):
        data = network_utilities.pack_varint(5)
        self.__server.send(data)

    def update(self):
        ready_to_read, _, _ = select.select([self.__server], [], [], 0)
        if ready_to_read:
            packet_id = network_utilities.unpack_varint(self.__server)
            if packet_id == 1:
                name = network_utilities.unpack_string(self.__server)
                admin = bool(network_utilities.unpack_varint(self.__server))
                self.__player.player_joined(name, admin)
            elif packet_id == 2:
                text = network_utilities.unpack_string(self.__server)
                self.__player.new_verse(text)
            elif packet_id == 3:
                self.__player.guess_incorrect()
            elif packet_id == 7:
                url = network_utilities.unpack_string(self.__server)
                self.__player.guess_partial_correct(url)
            elif packet_id == 4:
                self.__player.guess_correct()
            elif packet_id == 5:
                points = network_utilities.unpack_varint(self.__server)
                url = network_utilities.unpack_string(self.__server)
                player = network_utilities.unpack_string(self.__server)
                self.__player.verse_guessed(points, url, player)
            elif packet_id == 6:
                players = network_utilities.unpack_string_array(self.__server)
                scores = network_utilities.unpack_varint_array(self.__server)
                self.__player.game_over(players, scores)


class Player:

    __name: str
    __verse: str
    __score: int
    __game: Game | None
    __ui: UI
    __admin: bool

    def __init__(self, name: str, ui: UI):
        self.__name = name
        self.__verse = ""
        self.__score = 0
        self.__game = None
        self.__ui = ui
        self.__admin = False

    @property
    def name(self) -> str: return self.__name

    @property
    def verse(self) -> str: return self.__verse

    @property
    def score(self) -> int: return self.__score

    @property
    def admin(self) -> bool: return self.__admin

    def join_game(self, host: str = 'localhost', port: int = 7788):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        data = network_utilities.pack_varint(1)
        data += network_utilities.pack_string(self.name)
        conn.send(data)
        self.__game = Game(self, conn)

    def start_game(self):
        if self.__game is not None:
            self.__game.start_game()

    def guess_reference(self, url: str):
        if self.__game is not None:
            self.__game.guess_reference(url)

    def new_round(self, difficulty: int):
        if self.__game is not None:
            self.__game.start_round(difficulty)

    def end_game(self):
        if self.__game is not None:
            self.__game.end_game()

    def player_joined(self, name: str, admin: bool):
        if self.__game is not None:
            if name == self.name: self.__admin = admin or self.__admin
            self.__ui.player_joined(name, admin)

    def new_verse(self, text: str):
        if self.__game is not None:
            self.__verse = text
            self.__ui.new_verse(text)

    def guess_incorrect(self):
        if self.__game is not None:
            self.__ui.guess_incorrect()

    def guess_partial_correct(self, url):
        if self.__game is not None:
            self.__ui.guess_partial_correct(url)

    def guess_correct(self):
        if self.__game is not None:
            self.__ui.guess_correct()

    def verse_guessed(self, points: int, url: str, player: str):
        if self.__game is not None:
            self.__score += points
            self.__ui.verse_guessed(points, url, player)

    def game_over(self, players: list[str], scores: list[int]):
        if self.__game is not None:
            self.__ui.game_over(players, scores)

    def update(self):
        if self.__game is not None:
            self.__game.update()

