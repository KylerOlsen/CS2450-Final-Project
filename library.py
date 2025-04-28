# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from __future__ import annotations
import json
import random
import socket
import select
import network_utilities
from server import Game
from time import sleep


class Library:

    __verses: dict
    __games: list[Game]
    __host: str
    __port: int
    __socket: socket.socket
    __bible_only: bool

    def __init__(self, host: str = '', port: int = 7788, *, bible_only: bool = False):
        with open("data/scripture-frequencies.json", encoding='utf-8') as file:
            self.__verses = json.load(file)
        self.__games = []

        self.__host = host
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__bible_only = bible_only

    def serve_forever(self):
        try:
            print(f"Starting server at {self.__host}:{self.__port}")
            if self.__bible_only: print("Bible-only mode active.")
            with self.__socket as s:
                s.bind((self.__host, self.__port))
                s.listen(1)
                s.setblocking(False)
                while True:
                    ready_to_read, _, _ = select.select([s], [], [], 0)
                    for game in self.__games[:]:
                        if not game.finished: game.update()
                        else: self.__games.remove(game)
                    if ready_to_read:
                        conn, addr = s.accept()
                        conn.setblocking(False)
                        if network_utilities.unpack_varint(conn) == 1:
                            name = network_utilities.unpack_string(conn)
                            print(f"<< (1) join_game({name}, {addr})")
                            self.join_game(name, conn)
                    sleep(0.1)
        except KeyboardInterrupt:
            print("KeyboardInterrupt\nExiting...")
            return

    def join_game(self, name: str, conn: socket.socket):
        for i, game in enumerate(self.__games):
            if not game.active:
                game_num = i
                break
        else:
            self.__games.append(Game(self))
            game_num = len(self.__games) - 1
        self.__games[game_num].add_player(name, conn)

    def get_verse(self, difficulty: int, game: Game):
        url = self.__select_verse(difficulty)
        print(f"Verse Selected: {url}")
        text = self.__get_verse_text(url)

        game.new_verse(url, text)

    def __select_verse(self, difficulty: int) -> str:

        difficulty_verses = self.__get_verses_by_difficulty(difficulty)

        return difficulty_verses[random.randint(0,len(difficulty_verses)-1)]

    def __get_verse_text(self, url: str) -> str:
        lang = 'eng'
        volume, book_url, chapter_url, verse_url = url[1:].split('/')

        if volume == 'ot':
            filename = f"data/{lang}.old-testament.json"
        elif volume == 'nt':
            filename = f"data/{lang}.new-testament.json"
        elif volume == 'bofm':
            filename = f"data/{lang}.book-of-mormon.json"
        elif volume == 'dc-testament':
            filename = f"data/{lang}.doctrine-and-covenants.json"
        elif volume == 'pgp':
            filename = f"data/{lang}.pearl-of-great-price.json"

        with open(filename, encoding='utf-8') as file:
            data = json.load(file)
        for book in data['books']:
            if book['lds_slug'] == book_url:
                for chapter in book['chapters']:
                    if chapter['chapter'] == int(chapter_url):
                        for verse in chapter['verses']:
                            if verse['verse'] == int(verse_url):
                                return verse['text']
        raise ValueError(f'ERROR: VERSE NOT FOUND ({url})')

    def __get_verses_by_difficulty(self, difficulty: int) -> list[str]:
        real_difficulty_upper = pow((10-difficulty)/9, 2) * 500
        real_difficulty_lower = pow((9-difficulty)/9.55, 3) * 500

        difficulty_verses = []
        for key, value in self.__verses.items():
            if self.__bible_only and not (key.startswith('/ot') or key.startswith('/nt')):
                continue
            for i, diff in enumerate(value):
                if real_difficulty_lower <= diff <= real_difficulty_upper:
                    difficulty_verses.append(f"{key}/{i+1}")

        if not difficulty_verses: difficulty_verses.append('/pgp/js-h/1/17')

        return difficulty_verses


if __name__ == '__main__':
    lib = Library(bible_only=False)
    lib.serve_forever()
