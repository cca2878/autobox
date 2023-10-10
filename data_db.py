import json
import os

import msgpack
from tinydb import TinyDB, Query, Storage
# from typing import Union
from zstandard import ZstdCompressor, ZstdDecompressor

import constants


class Zstd(object):
    level = 3

    @classmethod
    def compress(cls, data: bytes) -> bytes:
        return ZstdCompressor(level=cls.level).compress(data)

    @classmethod
    def decompress(cls, data: bytes) -> bytes:
        return ZstdDecompressor().decompress(data)


# import yaml

class _MsgpackStorage(Storage):
    def __init__(self, filename):  # (1)
        self.filename = filename

    def read(self):
        try:
            with open(self.filename, 'rb') as handle:
                return msgpack.unpackb(Zstd.decompress(handle.read()))
        except msgpack.FormatError:
            return None  # (3)
        except msgpack.StackError:
            return None
        except FileNotFoundError:
            return None

    def write(self, data):
        with open(self.filename, 'wb') as handle:
            handle.write(Zstd.compress(msgpack.packb(data)))

    def close(self):  # (4)
        pass


class __Db(object):
    def __init__(self, name: str, path: str, storage=None):
        if storage:
            self._db = TinyDB(os.path.join(path, name + '.tdb'), storage=storage)
        else:
            self._db = TinyDB(os.path.join(path, name + '.tdb'))

    @staticmethod
    def get_query():
        return Query()


class __DataDb(__Db):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def db(self):
        return self._db

    def clean(self, key, key_list):
        """
        Clean the db, according to key and value list.
        Items that match one of the values in list will be reserved, others will be removed.
        :param key: key search
        :param key_list: the values list
        """
        _query = Query()
        # 使用 remove 方法和 test 方法删除不在列表中的文档
        self._db.remove(_query[key].test(lambda x: x not in key_list))


class __ConfigDb(__Db):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_config_db = self.ConfigTable(db=self._db, name='config')
        self.selected_units_db = self.ConfigTable(db=self._db, name='selected_units')
        # self._table_list = ('config', 'selected_units')
        # self._default_table = self._table_list[0]

    class ConfigTable:
        def __init__(self, db: TinyDB, name: str):
            self.__db = db.table(name)

        def update(self, name: str, value: any):
            __query = Query()
            self.__db.upsert({'name': name, 'value': value}, __query.name == name)

        def query(self, name: str, default: any = None):
            __query = Query()
            try:
                return self.__db.search(__query.name == name)[0]['value']
            except IndexError:
                return default
            except KeyError:
                return default


class NicknameLoader(object):
    def __init__(self):
        filename = 'nickname.json'
        self._path = os.path.join(constants.CACHE_PATH, constants.DIRS['data'], filename)
        self._nicknames = {}
        self.__load()

    def __load(self):
        try:
            with open(self._path, 'r', encoding='utf-8') as f:
                tmp_dict = json.loads(f.read())
                self._nicknames = {int(key): value for key, value in tmp_dict.items()} if tmp_dict else tmp_dict
        except FileNotFoundError:
            pass

    @property
    def nicknames(self):
        return self._nicknames


acc_db = __DataDb(name='accounts', storage=_MsgpackStorage,
                  path=os.path.join(constants.CACHE_PATH, constants.DIRS['data']))
result_db = __DataDb(name='result', storage=_MsgpackStorage,
                     path=os.path.join(constants.CACHE_PATH, constants.DIRS['data']))
config_db = __ConfigDb(name='config', path=constants.MAIN_PATH)

nk = NicknameLoader()
