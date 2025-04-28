# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

from client import Player
from reference import convert_reference, convert_url
from time import sleep
from blessed import Terminal


class UI:

    __player: Player
    __verse: str
    __in_game: bool
    __in_between_rounds: bool
    __game_over: bool
    __term: Terminal
    __buffer: str

    def __init__(self, playername: str, host: str='localhost', port: int=7788):
        self.__player = Player(playername, self)
        self.__player.join_game(host, port)
        self.__verse = ""
        self.__in_game = False
        self.__in_between_rounds = False
        self.__game_over = False
        self.__term = Terminal()
        self.__buffer = ""

    def get_line(self):
        with self.__term.cbreak():
            val = self.__term.inkey(timeout=0)
            if not val:
                return None
            if val.is_sequence:
                if val.name == 'KEY_ENTER':
                    line = self.__buffer
                    self.__buffer = ""
                    print()
                    return line
                elif val.name == 'KEY_BACKSPACE':
                    self.__buffer = self.__buffer[:-1]
                    print(f'\r{self.__term.clear_eol}{self.__buffer}', end='', flush=True)
            else:
                self.__buffer += val
                print(val, end='', flush=True)
        return None

    def __reset(self):
        self.__buffer = ""
        print()

    def loop(self):
        while not self.__game_over:
            self.__player.update()
            if text := self.get_line():
                if self.__in_between_rounds and self.__player.admin:
                    self.__next_round(text)
                elif self.__in_between_rounds:
                    print("Waiting for the next round to start...")
                elif self.__in_game: self.__guess_ref(text)
                elif self.__player.admin: self.__start_game(text)
                else:
                    print("Waiting for the game to start...")
            sleep(0.1)

    def __next_round(self, text: str):
        if text.isdigit() and 0 <= int(text) <= 10:
            print(f"Starting round with difficulty: {text}")
            self.__player.new_round(int(text))
        elif text.lower() == 'e':
            self.__player.end_game()
        else:
            print("Invalid input!\nPlease enter a difficulty level between 1 and 10.")

    def __guess_ref(self, text: str):
        try:
            url, possible = convert_reference(text)
        except Exception:
            print(
                "An Unknown Error Occurred.\n"
                "Please Check Your Reference and Try Again."
            )
        else:
            if url:
                try: ref = convert_url(url)
                except Exception: ref = url.upper().replace('/','.').strip('.')
                print(f"Your input was interpreted as: {ref}")
                self.__player.guess_reference(url)
                return
            elif possible:
                print(
                    "Sorry, that reference could not be found.\n"
                    "Did you mean one of these:"
                )
                for i in possible:
                    print(i)
            else:
                print(
                    "Sorry, that reference could not be found.\n"
                    "Please Check Your Reference and Try Again."
                )
        print(self.__verse)

    def __start_game(self, text: str = "1"):
        print("Starting game...")
        self.__in_between_rounds = True
        self.__player.start_game()
        self.__next_round(text)

    def player_joined(self, name: str, admin: bool):
        if name == self.__player.name:
            if admin:
                print("You are the game host.")
                print("Please enter the difficulty for the first round to start the game.")
                print("(Difficulty Range: 1 Easy - 10 Hard)")
            print(f"* {name} Joined the Game *")
        else: print(f"{name} Joined the Game")

    def new_verse(self, text: str):
        self.__reset()
        self.__in_game = True
        self.__in_between_rounds = False
        self.__verse = text
        print(self.__verse)

    def guess_incorrect(self):
        print("That guess was incorrect.")
        print(self.__verse)

    def guess_partial_correct(self, url):
        try: ref = convert_url(url)
        except Exception: ref = url.upper().replace('/','.').strip('.')
        print(f"That guess was partially correct: {ref}")
        print(self.__verse)

    def guess_correct(self):
        print("That guess was correct!")

    def verse_guessed(self, points: int, url: str, player: str):
        try: ref = convert_url(url)
        except Exception: ref = url.upper().replace('/','.').strip('.')
        print(
            f"\nThe verse has been guessed by {player}.\n"
            f"The reference is {ref}.\n"
            f"You have been awarded {points} points for your guess."
        )
        self.__in_between_rounds = True
        if self.__player.admin:
            print("Please enter the difficulty for the next round (1-10) or 'e' to end the game.")

    def game_over(self, players: list[str], scores: list[int]):
        self.__game_over = True
        print("\n--- THANKS FOR PLAYING! ---")
        for player, score in zip(players, scores):
            if player == self.__player.name:
                print(f"  * {player}: {score} *")
            else:
                print(f"    {player}: {score}")
