"""
ProxyPool definition.
"""

import random
from typing import List, Dict
from threading import Lock
import requests

from module import utils

class ProxyPool:
    """
    Used to monitor proxy pool status
    """
    def __init__(self, useful_proxies: List[str]):
        self.__useful_proxies: List[str] = useful_proxies
        self.__useless_proxies: List[str] = []
        self.__failed_proxies_info: List[Dict] = []  # failed proxies' error message

        # feature: a program should get every useful ip in turn.
        # every program request proxy_pool_console has different token
        # use token to identify different program
        # a program's index for self.useful_proxies will increase one after asking for a useful ip.
        self.token_to_index: Dict[str, int] = {}

        # TODO
        # feature: remove token that has not been used for a long time,
        # in order to control memory space.
        # LRU most recent used token will be most front,
        # when hit the limitation of token's amount, will remove last token's status.
        self.token_order: List[str] = []

        self.__lock = Lock()

    @property
    def amount(self) -> int:
        """
        Return total amount of proxies.
        """
        return len(self.__useful_proxies) + len(self.__useless_proxies)

    @property
    def useful_amount(self) -> int:
        """
        Return total amount of useful proxies.
        """
        return len(self.__useful_proxies)

    @property
    def useless_amount(self) -> int:
        """
        Return total amount of useless proxies.
        """
        return len(self.__useless_proxies)

    @property
    def failed_proxies_info(self) -> List[Dict]:
        """
        Return all failed proxies info
        """
        return self.__failed_proxies_info

    def random(self) -> str:
        """
        Return a random useful proxy if useful amount > 0 else empty string.
        """
        if self.useful_amount > 0:
            index = random.randint(0, self.useful_amount - 1)
            return self.__useful_proxies[index]
        else:
            return ""
    
    def index(self, i: int) -> str:
        """
        Return a useful proxy with index i
        """
        with self.__lock:
            i = i % self.useful_amount
            return self.__useful_proxies[i]
    
    def check(self) -> None:
        """
        Check all the proxy.

        Move useful proxies to self.useful_proxies
        Move useless proxies to self.useless_proxies
        """
        proxies = self.__useful_proxies + self.__useless_proxies
        useful_proxies = []
        useless_proxies = []
        failed_proxies_info = []

        for proxy in proxies:
            err_msg = self.__check_a_proxy(proxy)
            if not err_msg:
                useful_proxies.append(proxy)
            else:
                useless_proxies.append(proxy)
                failed_proxies_info.append({
                    'proxy': proxy,
                    'error_message': str(err_msg),
                    'test_time': utils.current_time()
                })

        with self.__lock:
            self.__useful_proxies = useful_proxies
            self.__useless_proxies = useless_proxies
            self.__failed_proxies_info = failed_proxies_info

    def __check_a_proxy(self, proxy: str) -> str:
        """
        Return empty string if proxy is useful else error message.
        """

        url = 'https://httpbin.org/ip'
        proxies = {'https': proxy}
        try:
            response = requests.get(url, proxies=proxies)
        except Exception as e:
            return e
        request_ip = response.json()['origin']
        proxy_ip = proxy.split(':')[0]
        if proxy_ip == request_ip:
            return ""
        return "proxy_ip is not equal to request ip"