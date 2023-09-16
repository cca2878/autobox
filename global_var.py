import copy
import os

import msgpack

from main import MAIN_PATH


class GlobalVarMgr(object):
    def __init__(self, stor_mgr):
        # self._variables = {}  # 使用字典来存储全局变量
        self._storage_mgr = stor_mgr
        self._ACCOUNTS = self._storage_mgr.load_accounts()
        self._RESULTS = self._storage_mgr.load_results()
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

    def _refresh_ACCMAP(self):
        _tmp_dict = {}
        for key, value in self._ACCOUNTS.items():
            _tmp_dict[value[0]] = key
        self._ACCMAP = _tmp_dict

    def set_ACCOUNTS(self, val: dict):
        self._ACCOUNTS = copy.deepcopy(val)
        self._refresh_ACCMAP()
        self._remap_RESULTS()
        self._storage_mgr.save_accounts()

    # def add_result(self, key, val):
    #     if key in self._RESULTS:
    #         raise Exception('This key already exists.Use "mod_result" to modify it.')
    #     else:
    #         self._RESULTS[key] = copy.deepcopy(val)

    def set_RESULTS(self, val):
        self._RESULTS = copy.deepcopy(val)
        self._storage_mgr.save_results()

    def _remap_RESULTS(self):
        _results = {}
        for k, v in self._RESULTS.items():
            if v['user_info']['acc'] in self._ACCMAP.keys():
                _results[self._ACCMAP[v['user_info']['acc']]] = v
        self.set_RESULTS(_results)
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


class StorageMgr(object):
    def __init__(self):
        """
        持久化存储文件相关
        """
        _dirname = 'cache/data'
        self._acc_filename = 'accounts.mp'
        self._rst_filename = 'results.mp'
        self._path = os.path.join(MAIN_PATH, _dirname)
        if not os.path.exists(self._path):
            os.makedirs(self._path, exist_ok=True)

    def save_accounts(self):
        with open(os.path.join(self._path, self._acc_filename), "wb") as f:
            # pickle.dump(accounts, f)
            f.write(msgpack.packb(global_var.ACCOUNTS))

    def save_results(self):
        with open(os.path.join(self._path, self._rst_filename), "wb") as f:
            f.write(msgpack.packb(global_var.RESULTS))
            # pickle.dump(results, f)

    def load_accounts(self):
        try:
            with open(os.path.join(self._path, self._acc_filename), "rb") as f:
                return msgpack.unpackb(f.read(), strict_map_key=False)
        except FileNotFoundError:
            return {}
        # return data

    def load_results(self):
        try:
            with open(os.path.join(self._path, self._rst_filename), "rb") as f:
                return msgpack.unpackb(f.read(), strict_map_key=False)
        except FileNotFoundError:
            return {}


storage_mgr = StorageMgr()
global_var = GlobalVarMgr(storage_mgr)
