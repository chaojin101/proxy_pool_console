import random

from flask import Flask, request

from . import helpers, utils, global_vals


app = Flask(__name__)

@app.route("/proxy", methods=['get'])
def proxy():
    """
    Return a proxy ip
    """
    # the port of request
    remote_port = request.environ.get('REMOTE_PORT')

    # get PROXY_POOL index by remote_port, if not index, generate a random index
    if len(global_vals.proxy_pool) == 0:
        return "None of one proxy ip works"
    index = global_vals.index.get(remote_port, random.randint(0, len(global_vals.proxy_pool)-1))
    index = (index + 1) % len(global_vals.proxy_pool)

    helpers.update(remote_port, index)

    return global_vals.proxy_pool[index]



@app.route('/status', methods=['get'])
def status():
    """
    Return the proxy pool status
    """
    status = {
        'total': len(global_vals.proxy_pool) + len(global_vals.failed_proxy_ips),
        'active': len(global_vals.proxy_pool),
        'fail_ip': []
    }
    print(global_vals.failed_proxy_ips)
    for ip, error_message in global_vals.failed_proxy_ips:
        status['fail_ip'].append({
            'ip': ip,
            'error_message': error_message
        })
    return status


