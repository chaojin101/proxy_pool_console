from typing import Dict, List
from threading import Lock
import random

from .proxy_pool import ProxyPool

class TokenPool:
    """
    Manage all the tokens.
    """

    def __init__(self, proxy_pool: ProxyPool):
        self.__proxy_pool = proxy_pool

        # feature: a program should get every useful ip in turn.
        # every program request proxy_pool_console has different token
        # use token to identify different program
        # a program's index for self.useful_proxies will increase one after asking for a useful ip.
        self.__token_to_index: Dict[str, int] = {}

        # feature: remove token that has not been used for a long time,
        # in order to control memory space.
        # LRU most recent used token will be most front,
        # when hit the limitation of token's amount, will move the last token to database, remove it from memory.
        self.__token_order: List[str] = []

        self.__lock = Lock()

    def sign(self, token: str) -> None:
        """
        Register a token

        assign a random index to the token
        append to the token order list
        """
        random_index = random.randint(0, self.__proxy_pool.useful_amount - 1)
        with self.__lock:
            self.__token_to_index[token] = random_index
            self.__token_order.append(token)

    def lookup(self, token: str) -> int:
        """
        Return an index of the token's record
        """
        index = self.__token_to_index.get(token)
        if index is None:
            return None

        #TODO return first
        with self.__lock:
            self.__move_front(token)
            self.__token_to_index[token] = (index + 1) % self.__proxy_pool.useful_amount
        return index

    def __move_front(self, token: str) -> None:
        """
        Move a token to the most front of self.__token_order
        """
        if token not in self.__token_order:
            return None
        self.__token_order.remove(token)
        self.__token_order.insert(0, token)
