import os

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(MAIN_PATH, 'cache')

DIRS = {'data': 'data'}
for d in DIRS:
    _dir = os.path.join(CACHE_PATH, d)
    if not os.path.exists(_dir):
        os.makedirs(_dir, exist_ok=True)
