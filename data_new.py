import asyncio

import json
import os.path
import traceback
from datetime import datetime
from pcrapi.core import pcrclient
from pcrapi.model.requests import LoadIndexRequest
from data_db import result_db, acc_db
from re import sub as re_sub


class PcrAccount(object):
    def __init__(self, username: str, password: str):
        # self._game_data = gamedata
        # self._user_info = None
        # self._user_units_data = None
        self._time = ''
        self._user_json = ''
        self._account_data = {'username': username, 'password': password}
        self._client = self._get_client()

    def _get_client(self):
        # Get Android Client
        return pcrclient(platform={
            'account': self._account_data['username'],
            'password': self._account_data['password'],
            'channel': 1,
            'platform': 2
        })

    async def login(self):
        try:
            await self._client.login()
            await self._request_json()
            self._time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        except Exception as _e:
            traceback.print_exc()
            return -1, str(_e)
        else:
            return 0, ''

    async def _request_json(self):
        req = LoadIndexRequest()
        req.carrier = 'CR_NMSL'
        self._user_json = (await self._client.request(req)).json()

    @property
    def sum(self):
        return {'acc': self._account_data['username'], 'time': self._time, 'json': self._user_json}


class JsonExporter(object):
    def __init__(self):
        pass

    def export_json(self, path: str):
        # 匹配非法字符的正则表达式
        __pattern = r"[\/\\\:\*\?\"\<\>\|\u0000-\u001F\u007F-\u009F]"
        __results = result_db.db.all()
        if __results:
            try:
                for item in __results:
                    __query = acc_db.get_query()
                    __filename = acc_db.db.search(__query['acc'] == item['acc'])[0]['alias']
                    __filename = item['acc'] if not __filename else __filename

                    with open(os.path.join(path, re_sub(pattern=__pattern, string=f"{__filename}_{item['time']}.json",
                                                        repl='')), mode='w') as f:
                        f.write(item['json'])
            except Exception as e:
                raise e


if __name__ == "__main__":
    pass
