import os
import json

import dotenv

from module.routes import app
from module import global_vals
from module.proxy_pool import ProxyPool
from module.token_pool import TokenPool

def init():
    """
    Load proxy pool from .env
    """
    dotenv.load_dotenv()
    proxy_pool_str = os.getenv('PROXY_POOL')
    proxy_pool_lst = json.loads(proxy_pool_str)
    global_vals.proxy_pool = ProxyPool(proxy_pool_lst)
    global_vals.token_pool = TokenPool(global_vals.proxy_pool)
    # utils.set_interval(global_vals.proxy_pool.check, [], 100)

def main():
    init()
    debug_mode = True if os.getenv('DEBUG') == 'True' else False 
    app.run(debug=debug_mode, host=os.getenv('HOST'), port=os.getenv('PORT'))

if __name__=='__main__':
    main()