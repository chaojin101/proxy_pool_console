import requests

from module import utils

from . import global_vals

def update(remote_port: str, index: int):
    """
    Update every port's status
    """

    # Update PORT_ORDER
    # LRU move current remote_port to first position
    if remote_port in global_vals.port_order:
        global_vals.port_order.remove(remote_port)
    global_vals.port_order.insert(0, remote_port)

    # Update INDEX[remote_port]
    # every port's index is counted separately
    global_vals.index[remote_port] = index

    # Keep memory usage in a limited range
    if len(global_vals.index) > 100:
        port = global_vals.port_order.pop()
        del index[port]

def check_proxy_pool():
    """
    Move useless proxy ips to FAILED_PROXY_IPS
    """
    for ip in global_vals.proxy_pool:
        proxies = {
            'http': ip,
            'https': ip
        }
        url = 'https://httpbin.org/ip'
        try: 
            r = requests.get(url, proxies=proxies)
            return_ip = r.json()['origin']
            ip = ip.split(':')[0] # strip port
            if ip == return_ip:
                continue
            raise(f'{ip} is different from {return_ip}')
        except Exception as e:
            global_vals.proxy_pool.remove(ip)
            global_vals.failed_proxy_ips.append([ip, str(e), utils.current_time()])
    
    for ip in global_vals.failed_proxy_ips:
        proxies = {
            'http': ip,
            'https': ip
        }
        url = 'https://httpbin.org/ip'
        try: 
            r = requests.get(url, proxies=proxies)
            return_ip = r.json()['origin']
            ip = ip.split(':')[0] # strip port
            if ip == return_ip:
                global_vals.proxy_pool.append(ip)
                continue
            raise(f'{ip} is different from {return_ip}')
        except Exception as e:
            #TODO: Modify error message and check time
            pass
