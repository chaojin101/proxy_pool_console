from typing import List, Dict

####################
# Global Valuables #
####################

"""
These global values used for tracing proxy service status
"""

# All the useful proxy ips
proxy_pool: List[str] = []

# useless proxy ips
failed_proxy_ips: List[List[str]] = []

# Every port's index for proxy_pool is counted separately, make every port get proxy ips from proxy_pool in turn
# Key  : port
# Value: index
index: Dict[str, str] = {}

# The order of most recent request's port
# Use for delete port which have not been requested for long time
port_order: List[str] = []

class ProxyPool:
    """
    Used to monitor proxy pool status
    """
    def __init__(self, useful_ips: List[str]):
        self.useful_ips: List[str] = useful_ips
        self.useless_ips: List[str] = []

        # feature: a program should get every useful ip in turn.
        # every program request proxy_pool_console has different token
        # use token to identify different program
        # a program's index for self.useful_ips will increase one after asking for a useful ip.
        self.token_to_index: Dict[str, int] = {}

        # feature: remove token that has not been used for a long time,
        # in order to control memory space.
        # LRU most recent used token will be most front,
        # when hit the limitation of token's amount, will remove last token's status.
        self.token_order: List[str] = []