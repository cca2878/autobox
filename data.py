import asyncio
import copy
import traceback
from datetime import datetime

import openpyxl
from openpyxl.cell import Cell
from openpyxl.styles import Alignment
from openpyxl.workbook import Workbook
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.worksheet.worksheet import Worksheet

from global_var import global_var
from pcrapi.core import pcrclient
from pcrapi.db import database, dbstart
from pcrapi.model import enums


# import openpyxl


class GameData(object):
    _inited = False

    def __init__(self):
        self._love_story_dict = None
        self._all_units_simple_dict = None
        if not self._inited:
            asyncio.get_event_loop().run_until_complete(dbstart.db_start())
            self._inited = True

    @property
    def all_units_simple_dict(self):
        if not self._all_units_simple_dict:
            temp_dict = {}
            for k, v in database.db.unlock_unit_dict.items():
                temp_dict[k] = v.unit_name
            self._all_units_simple_dict = temp_dict
        return self._all_units_simple_dict

    @property
    def all_units_dict(self):
        return database.db.unlock_unit_dict

    @property
    def unit_data_dict(self):
        return database.db.unit_data

    @property
    def pure_memory_to_unit_dict(self):
        return database.db.pure_memory_to_unit

    @property
    def unit_unique_equip_dict(self):
        return database.db.unit_unique_equip

    @property
    def love_story_dict(self):
        if self._love_story_dict is None:
            data = database.db.unit_story
            temp_dict = {}
            for item in data:
                temp_dict.setdefault(item.story_group_id, []).append(item.story_id)
            self._love_story_dict = temp_dict
        return self._love_story_dict


gamedata = GameData()


class Account(object):

    def __init__(self, username: str, password: str):
        self._game_data = gamedata
        self._user_info = None
        self._user_units_data = None
        self._account_data = {'username': username, 'password': password}
        self._client = self._get_client()

    @property
    def user_units_data(self):
        return self._user_units_data

    @property
    def user_info(self):
        return self._user_info

    @property
    def user_data_sum(self):
        """
        data sum
        :return: {'user_info': dict, 'user_units_data': dict, 'time': str}
        """
        return {'user_info': self._user_info, 'user_units_data': self._user_units_data,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    def _get_client(self):
        # Get Android Client
        _client = pcrclient(platform={
            'account': self._account_data['username'],
            'password': self._account_data['password'],
            'channel': 1,
            'platform': 2
        },
        )
        return _client

    async def login(self):
        try:
            await self._client.login()
            self._update_data()
        except Exception as _e:
            traceback.print_exc()
            return -1, str(_e)
        else:
            try:
                self._update_data()
            except Exception as _e:
                traceback.print_exc()
                return -2, str(_e)
            else:
                return 0, ''

    def check_login(func):
        def wrapper(self, *args, **kwargs):
            if self._client.name is None:
                raise Exception("Haven't Login!")
            return func(self, *args, **kwargs)

        return wrapper

    def _update_data(self):
        try:
            self._get_user_units_odict()
            self._gen_user_units_data()
            self._gen_user_info_dict()
        except Exception as _e:
            raise _e

    @check_login
    def _get_user_units_odict(self):
        """Get user's units origin dict"""
        try:
            self._read_story_ids = self._client.data.read_story_ids.copy()
            self._user_units_odict = self._client.data.unit.copy()
            # self._user_units_love_odict = self._client.data.unit_data.copy()
        except Exception as e:
            raise e

    def _gen_user_units_data(self):
        self._get_user_units_odict()
        _origin_data = self._user_units_odict.copy()
        # _love_origin_data = self._user_units_love_odict.copy()
        _read_story_ids = self._read_story_ids.copy()
        _new_data = {}
        _all_units_dict = self._game_data.all_units_dict

        # 'key' is unit_id
        for key in _all_units_dict.keys():
            if _origin_data.get(key, None) is None:
                _new_data[key] = {
                    'is_owned': False,
                    'status': '',
                    'star': self._game_data.unit_data_dict[key].rarity,
                    'memory': self._client.data.get_inventory(
                        (enums.eInventoryType.Item, 30000 + (key // 100))),
                    'pure_memory': self._client.data.get_inventory(
                        (enums.eInventoryType.Item, 31000 + (key // 100)))
                    if key in self._game_data.pure_memory_to_unit_dict.values() else None
                }
            else:
                _new_data[key] = {
                    'is_owned': True,
                    'status': '',
                    'star': _origin_data[key].unit_rarity,
                    'rank': _origin_data[key].promotion_level.value,
                    'level': _origin_data[key].unit_level,
                    'ub_level': _origin_data[key].union_burst[0].skill_level,
                    'sk1_level': 0 if len(_origin_data[key].main_skill) < 1 else
                    _origin_data[key].main_skill[0].skill_level,
                    'sk2_level': 0 if len(_origin_data[key].main_skill) < 2 else
                    _origin_data[key].main_skill[1].skill_level,
                    'skex_level': 0 if len(_origin_data[key].ex_skill) < 1 else
                    _origin_data[key].ex_skill[0].skill_level,
                    'equip': [],
                    'unique_equip': [],
                    # 'love': _love_origin_data[key // 100].love_level,
                    'love_story': len(set(self._game_data.love_story_dict[key // 100]) & set(_read_story_ids)),
                    'memory': self._client.data.get_inventory(
                        (enums.eInventoryType.Item, 30000 + (key // 100))),
                    'pure_memory': self._client.data.get_inventory(
                        (enums.eInventoryType.Item, 31000 + (key // 100)))
                    if key in self._game_data.pure_memory_to_unit_dict.values() else None
                }
                for item in _origin_data[key].equip_slot:
                    # None为没穿，穿了就是012345
                    if item.is_slot:
                        _new_data[key]['equip'].append(item.enhancement_level)
                    else:
                        _new_data[key]['equip'].append(None)

                if key in self._game_data.unit_unique_equip_dict.keys():
                    for item in _origin_data[key].unique_equip_slot:
                        # 加循环备战双专武甚至多专武
                        if item.is_slot:
                            _new_data[key]['unique_equip'].append(item.enhancement_level)
                        else:
                            _new_data[key]['unique_equip'].append(0)
                else:
                    _new_data[key]['unique_equip'].append(None)

        # 先这么写吧
        self._user_units_data = _new_data
        # return _new_data

    @check_login
    def _gen_user_info_dict(self):
        self._user_info = {
            'acc': self._account_data['username'],
            'name': self._client.name,
            'alias': global_var.ACCOUNTS[global_var.ACCMAP[self._account_data['username']]][2],
            'id': str(self._client.viewer_id),
            'mana': self._client.data.gold.gold_id_free + self._client.data.gold.gold_id_pay,
            'jewel': self._client.data.jewel.free_jewel + self._client.data.jewel.jewel,
            'stone': self._client.data.get_shop_gold(enums.eSystemId.MEMORY_PIECE_SHOP),  # 母猪石
            'star_cup': self._client.data.get_inventory((enums.eInventoryType.Item, 25001)),  # 星球杯
            'heart_debris': self._client.data.get_inventory((enums.eInventoryType.Equip, 140001)),  # 心碎
            'heart': self._client.data.get_inventory((enums.eInventoryType.Equip, 140000)),  # 公主心
            'master_coin': self._client.data.get_shop_gold(enums.eSystemId.COUNTER_STOP_SHOP),  # 大师币
        }


class ExcelExporter(object):
    def __init__(self, mode=1):
        """
        导出Excel表格
        :param mode: Int, 0,1,2。0为双格式，1为仅行账号，2为仅行角色
        """
        # self._data: Dict[int, dict] = copy.deepcopy(data)
        self._pre_processed = False
        self._data = None
        self._GameData = gamedata
        # self._preprocess_data()
        self._xlsx: Workbook = Workbook()
        self._mode = mode
        # self._init_template()

    def _init_template(self):
        _info_headers = [
            ('alias', '昵称'),
            ('name', '用户名'),
            ('id', 'uid'),
            ('time', '更新时间'),
            ('mana', 'mana数'),
            ('jewel', '钻石数'),
            ('stone', '母猪石数'),  # 母猪石
            ('star_cup', '星球杯数'),  # 星球杯
            ('all_hearts', '整心+心碎数'),  # 整心+心碎
            ('master_coin', '大师币数'),  # 大师币
        ]
        _unit_headers = [('status', '状态'), ('level', '等级'), ('rank', 'RANK'), ('equip', '装备'),
                         ('ub_level', 'UB'), ('sk1_level', 'sk1'), ('sk2_level', 'sk2'),
                         ('skex_level', 'skex'), ('unique_equip', '专武'), ('love_story', '好感等级'),
                         ('memory', '记忆碎片'),
                         # ('pure_memory', '纯净碎片')
                         ]
        _nicknames = global_var.NICKNAMES
        self._1_name = '行->账号'
        self._1_info_index = {}
        self._1_data_index = {}
        self._1_content_row = 3
        self._2_name = '行->角色'
        self._selected_units = global_var.SELECTEDUNITS
        wb: Workbook = Workbook()
        wb.remove(wb['Sheet'])
        _alignment = Alignment(vertical='center')

        def _row_account():
            ws: Worksheet = wb.create_sheet(title=self._1_name, index=0)
            # ColumnDimension(ws, bestFit=True, auto_size=True)
            # ws = wb.active
            for i in range(1, len(_info_headers) + 2):
                if i == 1:
                    ws.cell(row=1, column=i, value=f'序号')
                    self._1_info_index['index'] = i
                    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = 5
                    # ws.column_dimensions[openpyxl.utils.get_column_letter(i)].bestFit = True
                    # ws.column_dimensions[openpyxl.utils.get_column_letter(i)].auto_size = True
                else:
                    ws.cell(row=1, column=i, value=f'{_info_headers[i - 2][1]}')
                    self._1_info_index[_info_headers[i - 2][0]] = i
                    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = 10
                    # ws.column_dimensions[openpyxl.utils.get_column_letter(i)].bestFit = True
                    # ws.column_dimensions[openpyxl.utils.get_column_letter(i)].auto_size = True
                ws.merge_cells(start_row=1, end_row=2, start_column=i, end_column=i)
                cell: Cell = ws.cell(row=1, column=i)
                cell.alignment = _alignment
                if i == len(_info_headers) + 1:
                    ws.cell(row=1, column=i + 1, value=f'角色')
                    ws.merge_cells(start_row=1, end_row=2, start_column=i + 1, end_column=i + 1)
                    ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = 5
                    # ws.merge_cells(start_row=3, end_row=8192, start_column=i + 1, end_column=i + 1)
                    cell: Cell = ws.cell(row=1, column=i + 1)
                    cell.alignment = _alignment

            # 角色数据部分
            def _init_unit(_i, _item):
                # 获取区域&合并单元格
                if _i == 0:  # 角色之间间隔一列，前间隔
                    temp_start_col = ws.max_column + 1
                else:
                    temp_start_col = ws.max_column + 2
                    ws.column_dimensions[openpyxl.utils.get_column_letter(temp_start_col - 1)].width = 3
                ws.merge_cells(start_row=1, end_row=1, start_column=temp_start_col + 1,
                               end_column=temp_start_col + len(_unit_headers) - 1)
                # 填入名称
                if _nicknames and _item[0] in _nicknames.keys():
                    ws.cell(row=1, column=temp_start_col + 1,
                            value="-".join([str(_item[0]), str(_nicknames[_item[0]]), _item[1].unit_name]))
                else:
                    ws.cell(row=1, column=temp_start_col + 1, value="-".join([str(_item[0]), _item[1].unit_name]))
                # 建立索引
                self._1_data_index[_item[0]] = {}
                for j in range(len(_unit_headers)):
                    ws.cell(row=2, column=temp_start_col + j, value=_unit_headers[j][1])
                    ws.column_dimensions[openpyxl.utils.get_column_letter(temp_start_col + j)].width = 11.5
                    self._1_data_index[_item[0]][_unit_headers[j][0]] = temp_start_col + j

            if not self._selected_units:
                for i, item in enumerate(self._GameData.all_units_dict.items()):
                    _init_unit(i, item)
            else:
                for i in range(len(self._selected_units)):
                    unit_id = self._selected_units[i]
                    _init_unit(i, (unit_id, self._GameData.all_units_dict[unit_id]))

        def _row_unit():
            ws = wb.create_sheet(title=self._2_name, index=1)
            ColumnDimension(ws, bestFit=True, auto_size=True)

        if self._mode == 1:
            _row_account()
        elif self._mode == 2:
            _row_unit()
        else:
            _row_account()
            _row_unit()

        self._xlsx = wb

    def preprocess_data(self, force: bool = False):
        if force or (not self._pre_processed):
            self._data = global_var.RESULTS
            mem_list = [15, 30, 100, 120, 150, 50]
            for user in self._data.values():
                tmp_dict1: dict = user['user_info'].copy()
                tmp_dict2: dict = user['user_units_data'].copy()

                tmp_dict1['alias'] = tmp_dict1['alias'] if tmp_dict1['alias'] else tmp_dict1['name']

                tmp_dict1['all_hearts'] = str(tmp_dict1['heart']) + '+' + str(tmp_dict1['heart_debris'])
                tmp_dict1.pop('heart')
                tmp_dict1.pop('heart_debris')

                tmp_dict1['time'] = user['time']
                user.pop('time')
                # 角色部分
                for key, unit in tmp_dict2.items():
                    if unit['is_owned']:
                        tmp_status = f"{unit['star']}星"
                        # if unit['star'] < 6:
                        #     # mem_list = [15, 30, 100, 120, 150, 50]
                        #     if unit['pure_memory'] is not None:
                        #         if unit['pure_memory'] >= 50 and tmp_dict1['star_cup'] >= 100 and unit['memory'] >= sum(
                        #                 mem_list[unit['star']:]):
                        #             tmp_status = f"{unit['star']}可6"
                        #     elif unit['star'] < 5 and unit['memory'] >= mem_list[unit['star']]:
                        #         for i in range(unit['star'] + 2, len(mem_list)):
                        #             if unit['memory'] < sum(mem_list[unit['star']:i]):
                        #                 tmp_status = f"{unit['star']}可{i - 1}"
                        #                 break
                        #         else:
                        #             tmp_status = f"{unit['star']}可{len(mem_list) - 1}"

                        tmp_list1 = []
                        tmp_list2 = []
                        for item in unit['equip']:
                            if item is None:
                                tmp_list1.append('-')
                            else:
                                tmp_list1.append(str(item))
                        unit['equip'] = "/".join(tmp_list1)
                        for item in unit['unique_equip']:
                            if item is None:
                                tmp_list2.append('未实装')
                            else:
                                tmp_list2.append(str(item))
                        unit['unique_equip'] = "/".join(tmp_list2)
                    elif unit['memory'] >= self._GameData.all_units_dict[key].count_1:
                        tmp_status = '可拼'

                        # if unit['pure_memory'] is not None:
                        #     if unit['pure_memory'] >= 50 and tmp_dict1['star_cup'] >= 100 and unit['memory'] >= sum(
                        #             mem_list[unit['star']:]) + self._GameData.all_units_dict[key].count_1:
                        #         tmp_status = "可拼6"
                        # elif unit['memory'] >= self._GameData.all_units_dict[key].count_1:
                        #     tmp_status = f"可拼{unit['star']}"
                        #     if unit['memory'] - self._GameData.all_units_dict[key].count_1 >= mem_list[unit['star']]:
                        #         for i in range(unit['star'] + 2, len(mem_list)):
                        #             if unit['memory'] - self._GameData.all_units_dict[key].count_1 < sum(
                        #                     mem_list[unit['star']:i]):
                        #                 tmp_status = f"可拼{i - 1}"
                        #                 break
                        #         else:
                        #             tmp_status = f"可拼{len(mem_list) - 1}"
                    else:
                        tmp_status = '无'
                    unit.pop('star')
                    unit['status'] = tmp_status

                    if unit['pure_memory'] is None:
                        unit['pure_memory'] = '未实装'

                user['user_info'] = tmp_dict1
                user['user_units_data'] = tmp_dict2

            # self._data = sorted(self._data)
            self._pre_processed = True

    def _fill_content(self):
        wb = self._xlsx

        def _row_account():
            ws: Worksheet = wb[self._1_name]
            # ColumnDimension(ws, bestFit=True, auto_size=True)
            row = copy.deepcopy(self._1_content_row) - 1
            # tmp_list = sorted(self._data)
            for i in sorted(self._data):
                user = self._data[i]
                row += 1
                ws.cell(row=row, column=1, value=i + 1)
                for key, item in user['user_info'].items():
                    if self._1_info_index.get(key, None):
                        ws.cell(row=row, column=self._1_info_index[key],
                                value=row - self._1_content_row if key == 'index' else item)
                    else:
                        continue
                for key, unit in user['user_units_data'].items():
                    if key not in self._1_data_index.keys():
                        continue
                    # if unit['is_owned'] is False:
                    #     for col in self._1_data_index[key].values():
                    #         ws.cell(row=row, column=col, value='未拥有')
                    # else:
                    #     # tmp_dict = {}
                    for item in unit:
                        if self._1_data_index[key].get(item, None):
                            ws.cell(row=row, column=self._1_data_index[key][item], value=unit[item])
                        else:
                            continue
            # ColumnDimension(ws, bestFit=True)

        def _row_unit():
            pass

        if self._mode == 1:
            _row_account()
        elif self._mode == 2:
            _row_unit()
        else:
            _row_account()
            _row_unit()

        self._xlsx = wb

    def export_xlsx(self, path='export.xlsx'):
        self._xlsx.save(path)
        self._init_template()
        self.preprocess_data()
        self._fill_content()
        self._xlsx.save(path)


# Only for test
if __name__ == "__main__":
    pass
