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
