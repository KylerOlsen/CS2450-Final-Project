# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
from typing import TYPE_CHECKING
import select
import datetime
import network_utilities

if TYPE_CHECKING:
    from socket import socket
    from library import Library


class Game:

    __library: Library
    __current_url: str
    __current_url_parts: list[str]
    __clients: list[Player]
    __round_points: list[int]
    __total_scores: list[int]
    __active: bool
    __finished: bool
    __created: datetime.datetime

    def __init__(self, library: Library):
        self.__library = library
        self.__current_url = ""
        self.__current_url_parts = []
        self.__clients = []
        self.__round_points = []
        self.__total_scores = []
        self.__active = False
        self.__finished = False
        self.__created = datetime.datetime.now()

    @property
    def active(self) -> bool: return self.__active

    @property
    def finished(self) -> bool: return self.__finished

    def add_player(self, name: str, conn: socket):
        if not self.__active:
            self.__clients.append(Player(name, self, conn))
            self.__total_scores.append(0)
            for player in self.__clients:
                player.player_joined(name)

    def start_game(self):
        self.__active = True

    def start_round(self, difficulty: int):
        if self.__active and not self.__finished:
            self.__round_points = [0] * len(self.__clients)
            self.__library.get_verse(difficulty, self)

    def new_verse(self, url: str, text: str):
        for player in self.__clients:
            self.__current_url = url
            self.__current_url_parts = url.strip('/').split('/')
            player.new_verse(text)

    def guess_reference(self, url: str, player: Player):
        if self.__active and not self.__finished:
            if url == self.__current_url:
                player.guess_correct()
                self.__round_points[self.__clients.index(player)] = 4
                for i, points in enumerate(self.__round_points):
                    self.__total_scores[i] += points
                    self.__clients[i].verse_guessed(
                        points, self.__current_url, player.name)
            else:
                partially_correct = []
                for player_url, current_url in zip(url.strip('/').split('/'), self.__current_url_parts):
                    if player_url == current_url:
                        partially_correct.append(current_url)
                if partially_correct:
                    player.guess_partial_correct(f"/{'/'.join(partially_correct)}")
                    self.__round_points[self.__clients.index(player)] = len(partially_correct)
                else: player.guess_incorrect()

    def end_game(self):
        self.__finished = True
        for player in self.__clients:
            player.game_over(
                [i.name for i in self.__clients], self.__total_scores)

    def update(self):
        if not self.__active and (
            datetime.datetime.now() - self.__created >=
            datetime.timedelta(minutes=10)
        ) or (
            datetime.datetime.now() - self.__created >=
            datetime.timedelta(1)
        ): self.__finished = True
        if not self.__finished:
            for player in self.__clients:
                player.update()


class Player:

    __name: str
    __game: Game
    __client: socket

    def __init__(self, name: str, game: Game, conn: socket):
        self.__name = name
        self.__game = game
        self.__client = conn

    @property
    def name(self) -> str: return self.__name

    def player_joined(self, name: str):
        print(f">> (1) player_joined({name})")
        data = network_utilities.pack_varint(1)
        data += network_utilities.pack_string(name)
        self.__client.send(data)

    def new_verse(self, text: str):
        print(f">> (2) new_verse({text})")
        data = network_utilities.pack_varint(2)
        data += network_utilities.pack_string(text)
        self.__client.send(data)

    def guess_incorrect(self):
        print(">> (3) guess_incorrect()")
        data = network_utilities.pack_varint(3)
        self.__client.send(data)

    def guess_partial_correct(self, url):
        print(f">> (7) guess_partial_correct({url})")
        data = network_utilities.pack_varint(7)
        data += network_utilities.pack_string(url)
        self.__client.send(data)

    def guess_correct(self):
        print(">> (4) guess_correct()")
        data = network_utilities.pack_varint(4)
        self.__client.send(data)

    def verse_guessed(self, points: int, url: str, player: str):
        print(f">> (5) verse_guessed({points}, {url})")
        data = network_utilities.pack_varint(5)
        data += network_utilities.pack_varint(points)
        data += network_utilities.pack_string(url)
        data += network_utilities.pack_string(player)
        self.__client.send(data)

    def game_over(self, players: list[str], scores: list[int]):
        print(f">> (6) game_over({len(players)}, {len(scores)})")
        data = network_utilities.pack_varint(6)
        data += network_utilities.pack_string_array(players)
        data += network_utilities.pack_varint_array(scores)
        self.__client.send(data)
        self.__client.close()

    def update(self):
        ready_to_read, _, _ = select.select([self.__client], [], [], 0)
        if ready_to_read:
            packet_id = network_utilities.unpack_varint(self.__client)
            if packet_id == 2:
                print("<< (2) start_game()")
                self.__game.start_game()
            elif packet_id == 3:
                difficulty = network_utilities.unpack_varint(self.__client)
                print(f"<< (3) start_round({difficulty})")
                self.__game.start_round(difficulty)
            elif packet_id == 4:
                url = network_utilities.unpack_string(self.__client)
                print(f"<< (4) guess_reference({url}, {self.name})")
                self.__game.guess_reference(url, self)
            elif packet_id == 5:
                print("<< (5) end_game()")
                self.__game.end_game()

