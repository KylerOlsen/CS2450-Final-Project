# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
from typing import TYPE_CHECKING, ClassVar
import select
import datetime
import network_utilities

if TYPE_CHECKING:
    from socket import socket
    from library import Library


class Game:

    FINAL_SCORE_LIST: ClassVar[int] = 50

    __library: Library
    __current_url: str
    __current_url_parts: list[str]
    __clients: list[Player]
    __round_points: list[int]
    __total_scores: list[int]
    __active: bool
    __finished: bool
    __created: datetime.datetime
    __difficulty: int

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
        self.__difficulty = 0

    @property
    def active(self) -> bool: return self.__active

    @property
    def finished(self) -> bool: return self.__finished

    def add_player(self, name: str, conn: socket):
        if not self.__active:
            new_player = Player(name, self, conn)
            if self.__clients:
                for player in self.__clients:
                    new_player.player_joined(player.name, False)
                self.__clients.append(new_player)
                self.__total_scores.append(0)
                for player in self.__clients:
                    player.player_joined(name, False)
            else:
                new_player.player_joined(new_player.name, True)
                self.__clients.append(new_player)
                self.__total_scores.append(0)

    def start_game(self):
        self.__active = True

    def start_round(self, difficulty: int):
        if self.__active and not self.__finished:
            self.__difficulty = difficulty
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
                self.__round_points[self.__clients.index(player)] = 4 + self.__difficulty
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
        items = sorted(
            [(i.name, j) for i, j in zip(self.__clients, self.__total_scores)],
            reverse=True,
            key=lambda o: o[1]
        )
        players = [i for i, _ in items]
        scores = [i for _, i in items]
        for player in self.__clients:
            if player.name in players[:Game.FINAL_SCORE_LIST]:
                player.game_over(
                    players[:Game.FINAL_SCORE_LIST],
                    scores[:Game.FINAL_SCORE_LIST]
                )
            else:
                player.game_over(
                    players[:Game.FINAL_SCORE_LIST] + [player.name],
                    scores[:Game.FINAL_SCORE_LIST] + [scores[players.index(player.name)]]
                )

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
    __connected: bool

    def __init__(self, name: str, game: Game, conn: socket):
        self.__name = name
        self.__game = game
        self.__client = conn
        self.__connected = True

    @property
    def name(self) -> str: return self.__name

    def player_joined(self, name: str, admin: bool):
        print(f">> (1, {self.name}) player_joined({name}, {admin})")
        data = network_utilities.pack_varint(1)
        data += network_utilities.pack_string(name)
        data += network_utilities.pack_varint(admin)
        self.__client.send(data)

    def new_verse(self, text: str):
        print(f">> (2, {self.name}) new_verse({text})")
        data = network_utilities.pack_varint(2)
        data += network_utilities.pack_string(text)
        self.__client.send(data)

    def guess_incorrect(self):
        print(f">> (3, {self.name}) guess_incorrect()")
        data = network_utilities.pack_varint(3)
        self.__client.send(data)

    def guess_partial_correct(self, url):
        print(f">> (7, {self.name}) guess_partial_correct({url})")
        data = network_utilities.pack_varint(7)
        data += network_utilities.pack_string(url)
        self.__client.send(data)

    def guess_correct(self):
        print(f">> (4, {self.name}) guess_correct()")
        data = network_utilities.pack_varint(4)
        self.__client.send(data)

    def verse_guessed(self, points: int, url: str, player: str):
        print(f">> (5, {self.name}) verse_guessed({points}, {url})")
        data = network_utilities.pack_varint(5)
        data += network_utilities.pack_varint(points)
        data += network_utilities.pack_string(url)
        data += network_utilities.pack_string(player)
        self.__client.send(data)

    def game_over(self, players: list[str], scores: list[int]):
        print(f">> (6, {self.name}) game_over({len(players)}, {len(scores)})")
        data = network_utilities.pack_varint(6)
        data += network_utilities.pack_string_array(players)
        data += network_utilities.pack_varint_array(scores)
        self.__client.send(data)
        self.__client.close()
        self.__connected = False

    def update(self):
        if self.__connected:
            ready_to_read, _, _ = select.select([self.__client], [], [], 0)
            if ready_to_read:
                packet_id = network_utilities.unpack_varint(self.__client)
                if packet_id == 2:
                    print(f"<< (2, {self.name}) start_game()")
                    self.__game.start_game()
                elif packet_id == 3:
                    difficulty = network_utilities.unpack_varint(self.__client)
                    print(f"<< (3, {self.name}) start_round({difficulty})")
                    self.__game.start_round(difficulty)
                elif packet_id == 4:
                    url = network_utilities.unpack_string(self.__client)
                    print(f"<< (4, {self.name}) guess_reference({url})")
                    self.__game.guess_reference(url, self)
                elif packet_id == 5:
                    print(f"<< (5, {self.name}) end_game()")
                    self.__game.end_game()

