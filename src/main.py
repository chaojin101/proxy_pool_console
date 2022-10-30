import os
import json

import dotenv

from module.routes import app
from module import utils, helpers, global_vals

def init():
    """
    Load proxy pool from .env
    """
    dotenv.load_dotenv()
    proxy_pool_str = os.getenv('PROXY_POOL')
    global_vals.proxy_pool = json.loads(proxy_pool_str)
    utils.set_interval(helpers.check_proxy_pool, [], 10)

def main():
    init()
    debug_mode = True if os.getenv('DEBUG') == 'True' else False 
    app.run(debug=debug_mode, host=os.getenv('HOST'), port=os.getenv('PORT'))

if __name__=='__main__':
    main()