
from client import Player

class UI:

    __player: Player

    def __init__(self, playername: str, host: str='localhost', port: int=7788):
        self.__player = Player(playername)
        self.__player.join_game()
