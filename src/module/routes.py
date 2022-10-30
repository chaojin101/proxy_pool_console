import uuid

from flask import Flask, request

from . import global_vals

app = Flask(__name__)

@app.route("/proxy", methods=['get'])
def proxy():
    """
    Return a proxy ip if there is a useful proxy in proxy pool else empty string.
    
    withour token return a random useful proxy
    """
    token = request.args.get('token')
    if token is None:
        return global_vals.proxy_pool.random()

    index = global_vals.token_pool.lookup(token)
    if index is None:
        return "invalid token"

    return global_vals.proxy_pool.index(index)


@app.route("/token", methods=['get'])
def token():
    """
    Return a token, used to request /proxy?token={token}
    """
    token = uuid.uuid4().hex
    global_vals.token_pool.sign(token)
    return token


@app.route('/status', methods=['get'])
def status():
    """
    Return the proxy pool status
    """
    return {
        'total': global_vals.proxy_pool.amount,
        'active': global_vals.proxy_pool.useful_amount,
        'fail_ips': global_vals.proxy_pool.failed_proxies_info
    }


