import copy
import json
import os

import msgpack

from main import MAIN_PATH


# from data import gamedata


class StorageMgr(object):
    def __init__(self):
        """
        持久化存储文件相关
        """
        _dirname = ['cache', 'data']
        self._suffix = {'mp': '.mp', 'json': '.json'}
        self._path = os.path.join(MAIN_PATH, *_dirname)
        if not os.path.exists(self._path):
            os.makedirs(self._path, exist_ok=True)
        self._filenames = set([os.path.splitext(f)[0] for f in os.listdir(self._path) if
                               os.path.isfile(os.path.join(self._path, f)) and f.endswith(
                                   tuple(self._suffix.values()))])

    def save(self, filename: str, data, method: str = 'mp'):
        if method not in self._suffix.keys():
            raise ValueError
        else:
            with open(os.path.join(self._path, f'{filename}{self._suffix[method]}'), "wb") as f:
                if method == 'mp':
                    f.write(msgpack.packb(data))
                elif method == 'json':
                    f.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        if filename not in self._filenames:
            self._filenames.add(filename)

    def load(self, filename: str, default=None, method: str = 'mp'):
        if method not in self._suffix.keys():
            raise ValueError
        if default is None:
            default = {}
        if filename in self._filenames:
            try:
                with open(os.path.join(self._path, f'{filename}{self._suffix[method]}'), "rb") as f:
                    if method == 'mp':
                        return msgpack.unpackb(f.read(), strict_map_key=False)
                    elif method == 'json':
                        return json.load(f)
            except FileNotFoundError:
                return default
        else:
            return default

    # def save_accounts(self):
    #     with open(os.path.join(self._path, self._acc_filename), "wb") as f:
    #         # pickle.dump(accounts, f)
    #         f.write(msgpack.packb(global_var.ACCOUNTS))
    #
    # def save_results(self):
    #     with open(os.path.join(self._path, self._rst_filename), "wb") as f:
    #         f.write(msgpack.packb(global_var.RESULTS))
    #         # pickle.dump(results, f)
    #
    # def load_accounts(self):
    #     try:
    #         with open(os.path.join(self._path, self._acc_filename), "rb") as f:
    #             return msgpack.unpackb(f.read(), strict_map_key=False)
    #     except FileNotFoundError:
    #         return {}
    #     # return data
    #
    # def load_results(self):
    #     try:
    #         with open(os.path.join(self._path, self._rst_filename), "rb") as f:
    #             return msgpack.unpackb(f.read(), strict_map_key=False)
    #     except FileNotFoundError:
    #         return {}


class GlobalVarMgr(object):
    def __init__(self, stor_mgr: StorageMgr):
        # self._variables = {}  # 使用字典来存储全局变量
        self._storage_mgr = stor_mgr
        self._acc_filename = 'accounts'
        self._rst_filename = 'results'
        self._selected_units_filename = 'selected_units'
        self._nicknames_filename = 'nickname'
        # self._ACCOUNTS = self._storage_mgr.load_accounts()
        # self._RESULTS = self._storage_mgr.load_results()
        self._load()

    def _load(self):
        self._ACCOUNTS = self._storage_mgr.load(self._acc_filename)
        self._RESULTS = self._storage_mgr.load(self._rst_filename)
        self._SELECTEDUNITS = self._storage_mgr.load(self._selected_units_filename, default=set(), method='json')
        _temp_dict = self._storage_mgr.load(self._nicknames_filename, method='json')
        self._NICKNAMES = {int(key): value for key, value in _temp_dict.items()} if _temp_dict else _temp_dict
        self._ACCMAP = {}
        self._refresh_ACCMAP()

    @property
    def ACCOUNTS(self):
        """
        获取ACCOUNTS
        :return: ACCOUNTS, Dict, {int: [username, password]}
        """
        return copy.deepcopy(self._ACCOUNTS)

    @property
    def ACCMAP(self) -> dict:
        """
        获取ACCMAP
        :return: ACCOUNTS:idx, Dict, {username: idx}
        """
        return copy.deepcopy(self._ACCMAP)

    @property
    def RESULTS(self) -> dict:
        """
        获取RESULTS
        :return: RESULTS, Dict, {idx: account.user_data_sum}
        """
        return copy.deepcopy(self._RESULTS)

    @property
    def SELECTEDUNITS(self) -> list:
        """
        获取SELECTED UNITS
        :return: SELECTED UNITS, list, [unit_id]
        """
        # if not self._SELECTEDUNITS:
        #     self.set_SELECTEDUNITS(gamedata.all_units_simple_dict)
        return copy.deepcopy(self._SELECTEDUNITS)

    @property
    def NICKNAMES(self) -> dict:
        """
        获取NICKNAMES
        :return: nicknames, dict, [unit_id: nickname]
        """

        return copy.deepcopy(self._NICKNAMES)

    def _refresh_ACCMAP(self):
        _tmp_dict = {}
        for key, value in self._ACCOUNTS.items():
            _tmp_dict[value[0]] = key
        self._ACCMAP = _tmp_dict

    def set_ACCOUNTS(self, val: dict):
        self._ACCOUNTS = copy.deepcopy(val)
        self._refresh_ACCMAP()
        self._remap_RESULTS()
        self._storage_mgr.save(filename=self._acc_filename, data=self._ACCOUNTS)

    # def add_result(self, key, val):
    #     if key in self._RESULTS:
    #         raise Exception('This key already exists.Use "mod_result" to modify it.')
    #     else:
    #         self._RESULTS[key] = copy.deepcopy(val)

    def set_RESULTS(self, val):
        self._RESULTS = copy.deepcopy(val)
        # self._storage_mgr.save_results()
        self._storage_mgr.save(filename=self._rst_filename, data=self._RESULTS)

    def _remap_RESULTS(self):
        _results = {}
        for k, v in self._RESULTS.items():
            if v['user_info']['acc'] in self._ACCMAP.keys():
                _results[self._ACCMAP[v['user_info']['acc']]] = v
        self.set_RESULTS(_results)

    def set_SELECTEDUNITS(self, val):
        self._SELECTEDUNITS = copy.deepcopy(val)
        # self._storage_mgr.save_results()
        self._storage_mgr.save(filename=self._selected_units_filename, data=self._SELECTEDUNITS, method='json')

    # def mod_result(self, key, val):
    #     if key in self._RESULTS:
    #         self._RESULTS[key] = copy.deepcopy(val)
    #     else:
    #         raise Exception('This key does not exist.Use "add_result" to add it.')
    #
    # def del_result(self, key):
    #     if key in self._RESULTS:
    #         self._RESULTS.pop(key)
    #     else:
    #         raise Exception('This key does not exist.')


storage_mgr = StorageMgr()
global_var = GlobalVarMgr(storage_mgr)
