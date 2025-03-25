import os
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
# Load configuration from config.yaml
_config_path = os.path.join(ROOT_DIR, 'config.yml')
with open(_config_path, 'r', encoding='utf-8') as f:
    config = yaml.load(f)

CONSTANTS_PATH = os.path.join(ROOT_DIR, config['path']['constants'])
with open(CONSTANTS_PATH, 'r', encoding='utf-8') as f:
    constants = yaml.load(f)

###
# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
# NOTSET = 0
###

LOG_LEVEL = int(config['log_level'])

CLIENT_POOL_SIZE_MAX = 100
CLIENT_POOL_MAX_AGE = 3600 * 24
CLIENT_POOL_MAX_CLIENT_ALIVE = 10
SESSION_ERROR_MAX_RETRY = 2
MAX_API_RUNNING = 8

BSDK = '官服'
QSDK = '渠道服'

CHANNEL_OPTION = [BSDK, QSDK]

DEBUG_LOG = False
ERROR_LOG = True

CACHE_DIR = os.path.join(ROOT_DIR, config['path']['cache'])
RESULT_DIR = os.path.join(ROOT_DIR, config['path']['result'])
DATA_DIR = os.path.join(ROOT_DIR, config['path']['data'])
CONFIG_PATH = os.path.join(CACHE_DIR, config['path']['config'])
OLD_CONFIG_PATH = os.path.join(ROOT_DIR, config['path']['old_config'])
AUTH_KEY = config['auth_key']

LOG_PATH = os.path.join(ROOT_DIR, 'log/')

DEFAULT_HEADERS = dict(constants['headers']['android'])
IOS_HEADERS = dict(constants['headers']['ios'])

def update_app_ver(version: str = None):
    default_ver = '7.7.2'
    if version is not None:
        with open(CONSTANTS_PATH, 'rw', encoding='utf-8') as f:
            data = yaml.load(f)
            data['headers']['default']['APP-VER'] = version
            yaml.dump(data, f)
            # VERSION = version
    else:
        # try:
        #     with open(os.path.join(CACHE_DIR, 'version.txt'), 'r', encoding='utf-8') as f:
        #         VERSION = f.read()
        # except FileNotFoundError:
        #     update_app_ver(default_ver)
            return

#     DEFAULT_HEADERS['APP-VER'] = VERSION
#     IOS_HEADERS['APP-VER'] = VERSION
#
#
#
# update_app_ver()
