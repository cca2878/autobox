# -*- coding: utf-8 -*-
import copy
from traceback import print_exc

# import os
from PySide6.QtCore import QUrl, Slot, Signal, Qt
# from PySide6.QtGui import QBrush
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import QMainWindow, QDialog, QTableWidgetItem, QFileDialog, QPushButton, QWidget, \
    QMessageBox, QListWidget, QListWidgetItem, QHeaderView

import webbridge
from itertools import chain
from global_var import global_var
from data_db import acc_db, result_db, config_db, nk
from task import AsyncWorker, AsyncExporter, DbInitializer
from ui_parts.ui_autobox import Ui_MainWindow
from ui_parts.ui_edit import Ui_editDialog
from ui_parts.ui_manualvali import Ui_MValiDialog
from ui_parts.ui_selectunits import Ui_selectUnitDialog
# noinspection PyUnresolvedReferences
from ui_parts.validator_res_rc import *


class MainWindowUi(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self._components_status = {}
        self._col_idx = {'index': 0, 'username': 1, 'status': 2, 'manual_vali': 3, 'last_time': 4}
        self._table_item_dict = {}
        # self._exporter = ExcelExporter()
        self.setupUi(self)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._startup()

    def _startup(self):
        @Slot(int)
        def raw_check_bind(state):
            if state == Qt.Checked.value:
                self.btnSelectU.setDisabled(True)
            elif state == Qt.Unchecked.value:
                self.btnSelectU.setDisabled(False)

        self.checkBoxRaw.stateChanged.connect(raw_check_bind)

        def read_configs():
            self.spboxThNum.setValue(int(config_db.main_config_db.query(name='threads_num', default=1)))
            self.checkBoxRaw.setChecked(config_db.main_config_db.query(name='only_export_json', default=False))
            self.checkBoxSep.setChecked(config_db.main_config_db.query(name='sep_export', default=False))

        read_configs()
        self.set_status_text('')
        self._set_components_status(False)
        self.btnStart.clicked.connect(self._start_tasks)

        @Slot()
        def export_data():
            file_dialog = QFileDialog(self)

            @Slot(bool, str)
            def _show_msgbox(status: bool, text: str):
                # 创建一个QMessageBox实例
                message_box = QMessageBox(self)
                message_box.setText(text)
                message_box.setStandardButtons(QMessageBox.Ok)
                if status:
                    message_box.setWindowTitle("Export Success!")
                    message_box.setIcon(QMessageBox.Information)
                else:
                    message_box.setWindowTitle("Export Failed!")
                    message_box.setIcon(QMessageBox.Critical)
                message_box.exec()
                # self._set_components_status(True)

            if config_db.main_config_db.query(name='only_export_json', default=False):
                file_dialog.setFileMode(QFileDialog.Directory)
                file_dialog.setOption(QFileDialog.ShowDirsOnly)

                if file_dialog.exec() == QFileDialog.Accepted:
                    print(file_dialog.selectedFiles()[0])
                    self._exporter = AsyncExporter(file_dialog.selectedFiles()[0], json_only=True)
                    self._exporter.result_signal.connect(_show_msgbox)
                    self._exporter.status_signal.connect(self.set_status_text)
                    self._exporter.start()

            else:
                # file_dialog.setAcceptMode(QFileDialog.AcceptSave)
                # file_dialog.setNameFilter('Excel Workbook (*.xlsx)')
                #
                # if file_dialog.exec() == QFileDialog.Accepted:
                #     # self._set_components_status(False)
                #     self._exporter = AsyncExporter(file_dialog.selectedFiles()[0], mode=self.checkBoxSep.isChecked())
                #     self._exporter.result_signal.connect(_show_msgbox)
                #     self._exporter.status_signal.connect(self.set_status_text)
                #     self._exporter.start()
                _show_msgbox(False, 'This version cannot export xlsx .\nPlease check or wait for updates.')
                pass

        self.btnOutput.clicked.connect(export_data)

        @Slot(int, str)
        def raw_check_save(state, name: str):
            if state == Qt.Checked.value:
                config_db.main_config_db.update(name=name, value=True)
            elif state == Qt.Unchecked.value:
                config_db.main_config_db.update(name=name, value=False)

        self.checkBoxRaw.stateChanged.connect(lambda x: raw_check_save(x, 'only_export_json'))
        self.checkBoxSep.stateChanged.connect(lambda x: raw_check_save(x, 'sep_export'))

        @Slot(int)
        def set_threads(v: int):
            config_db.main_config_db.update(name='threads_num', value=v)

        self.spboxThNum.valueChanged.connect(set_threads)

        @Slot()
        def _db_complete():
            self.set_status_text('Loading accounts')
            try:
                self._load()
                self.set_status_text('Ready')
                self._set_components_status(True)
                pass
            except Exception as e:
                print_exc()
                self.set_status_text(f'Err! {str(e)}')
            del self._db_init

        self._db_init = DbInitializer()
        self._db_init.status_signal.connect(self.set_status_text)
        self._db_init.complete_signal.connect(_db_complete)
        self._db_init.start()

        # self._set_components_status(False)

        @Slot()
        def _show_edit_dialog():
            @Slot(int)
            def edit_dialog_finished(result):
                if result == QDialog.Accepted:
                    self._load()
                    if not self.tableWidget.rowCount() == 0:
                        self.btnStart.setEnabled(True)

            self._edit_dialog = EditDialogUi()
            self._edit_dialog.finished.connect(edit_dialog_finished)
            self._edit_dialog.show()

        self.btnEdit.clicked.connect(_show_edit_dialog)

        @Slot()
        def _show_select_units_dialog():
            self._selectU_dialog = SelectUnitsDialogUi()
            # self._selectU_dialog.finished.connect(self._edit_dialog_finished)
            self._selectU_dialog.show()

        self.btnSelectU.clicked.connect(_show_select_units_dialog)

    def _load(self):
        # _acc = acc_db.db.all()
        if not acc_db.db.all():
            self.btnStart.setEnabled(False)
        # if not global_var.RESULTS:
        #     self.btnOutput.setEnabled(False)
        self.tableWidget.setRowCount(0)

        # self._buttons = {}

        def _add_table_item():
            # results = global_var.RESULTS
            accounts = acc_db.db.all()
            _query = result_db.get_query()
            for key, item in enumerate(accounts):
                username_item = QTableWidgetItem(
                    str(item['acc'] if not item['alias'] else f"{item['alias']}({item['acc']})"))
                status_item = QTableWidgetItem('Waiting…')
                _acc_results = result_db.db.search(_query.acc == item['acc'])
                time_item = QTableWidgetItem(str(_acc_results[0]['time'] if _acc_results else ''))
                vali_btn = ValidateBtn(acc=item['acc'])
                self.tableWidget.insertRow(key)
                self.tableWidget.setItem(key, self._col_idx['index'], QTableWidgetItem(str(key + 1)))
                self.tableWidget.setItem(key, self._col_idx['username'], username_item)
                self.tableWidget.setItem(key, self._col_idx['status'], status_item)
                self.tableWidget.setItem(key, self._col_idx['last_time'], time_item)
                self.tableWidget.setCellWidget(key, self._col_idx['manual_vali'], vali_btn)
                self._table_item_dict[item['acc']] = {'status': status_item, 'vali_btn': vali_btn, 'time': time_item}

        self.tableWidget.horizontalHeader().setSectionResizeMode(self._col_idx['index'], QHeaderView.ResizeToContents)
        _add_table_item()

    @Slot(str, str, int)
    def set_acc_status_text(self, acc: str, text: str, color: int = None):
        """
        设置status
        :param color: (Unavail) Qt Color
        :param acc: account name,
        :param text: text
        """
        self._table_item_dict[acc]['status'].setText(text)
        # acc_map = global_var.ACCMAP
        # if len(info) == 3:
        #     brush = info[2]
        # else:
        #     brush = None
        # status_item = QTableWidgetItem(info[1])
        # status_item.setForeground(brush)
        # self.tableWidget.setItem(info[0], self._col_idx['status'], status_item)

    @Slot(str)
    def set_status_text(self, text):
        self.statusBar.showMessage(f'Status: {text}...')

    @Slot(str, str)
    def set_last_time(self, acc: str, time: str):
        """
        设置last time
        :param time: last time
        :param acc: account name
        """
        self._table_item_dict[acc]['time'].setText(time)

    @Slot(str, str)
    def acquire_m_vali(self, acc, url):
        self._table_item_dict[acc]['vali_btn'].set_url(url)
        self._table_item_dict[acc]['vali_btn'].enable_self()
        self.set_acc_status_text(acc, 'Need manual validate!')

    @Slot(str)
    def task_complete(self, text):
        self._set_components_status(True)
        self.set_status_text(text)
        if result_db.db.all():
            self.btnOutput.setEnabled(True)
        del self._worker

    def _set_components_status(self, status: bool):
        pass
        if status:
            self.groupBox.setEnabled(True)
            self.verticalWidget_2.setEnabled(True)
            # 遍历所有组件
            for widget in chain(self.groupBox.findChildren(QWidget), self.verticalWidget_2.findChildren(QWidget)):
                # 恢复当前组件的原始状态
                widget.setEnabled(self._components_status.get(widget, True))
            self._components_status = {}
        else:
            # 遍历所有组件
            for widget in chain(self.groupBox.findChildren(QWidget), self.verticalWidget_2.findChildren(QWidget)):
                # 保存当前组件的状态
                self._components_status[widget] = copy.deepcopy(widget.isEnabled())
                # 禁用当前组件
                # widget.setEnabled(False)
            self.groupBox.setEnabled(False)
            self.verticalWidget_2.setEnabled(False)

        # for item in self.groupBox.findChildren(QWidget):
        #     item.setEnabled(status)
        # self.btnStart.setEnabled(status)
        # self.btnOutput.setEnabled(status)

    def _start_tasks(self):
        self._set_components_status(False)
        self._worker = AsyncWorker(obj=self, max_size=self.spboxThNum.value())
        self._worker.status_signal.connect(self.set_status_text)
        self._worker.start()


class EditDialogUi(Ui_editDialog, QDialog):
    def __init__(self):
        super().__init__()
        self._cell_key = ('acc', 'pwd', 'alias')
        self.setupUi(self)
        self._load()
        self.btnAdd.clicked.connect(self._add_account)
        self.btnRm.clicked.connect(self._remove_account)
        self.buttonBox.rejected.connect(self._discard)  # Discard 按钮点击事件
        self.buttonBox.accepted.connect(self._save)  # Save 按钮点击事件

    def _add_account(self):
        row_position = self.tableWidget.rowCount()  # 获取当前行数
        self.tableWidget.insertRow(row_position)  # 插入新行
        for col in range(self.tableWidget.columnCount()):
            self.tableWidget.setItem(row_position, col, QTableWidgetItem())
        self.tableWidget.setCurrentCell(row_position, 0)

    def _remove_account(self):
        # selected_items = self.tableWidget.selectedItems()
        selected_ranges = self.tableWidget.selectedRanges()
        if selected_ranges:
            selected_items = []
            for item in selected_ranges:
                for i in range(item.topRow(), item.bottomRow() + 1):
                    selected_items.append(self.tableWidget.item(i, 2))
            for item in selected_items:
                self.tableWidget.removeRow(item.row())

    def _save(self):
        temp_set = set()
        _query = acc_db.get_query()
        for row in range(self.tableWidget.rowCount()):
            temp_dict = {}
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item and (item.text() != '' or col > 1):
                    temp_dict[self._cell_key[col]] = item.text()
                else:
                    break
            else:
                if temp_dict[self._cell_key[0]] not in temp_set:
                    temp_set.add(temp_dict[self._cell_key[0]])
                    acc_db.db.upsert(temp_dict, _query.acc == temp_dict[self._cell_key[0]])
                # temp_dict[index] = temp_list
        # global_var.set_ACCOUNTS(acc_dict)
        acc_db.clean(key='acc', key_list=temp_set)
        result_db.clean(key='acc', key_list=[item['acc'] for item in acc_db.db])
        print("用户点击了保存按钮")
        self.accept()

    def _load(self):
        for row, item in enumerate(acc_db.db.all()):
            self.tableWidget.insertRow(row)
            for i, key in enumerate(self._cell_key):
                self.tableWidget.setItem(row, i, QTableWidgetItem(str(item[key])))

    # for key in global_var.ACCOUNTS:
    #     if global_var.ACCOUNTS[key]:
    #         username_item = QTableWidgetItem(str(global_var.ACCOUNTS[key][0]))
    #         password_item = QTableWidgetItem(str(global_var.ACCOUNTS[key][1]))
    #         alias_item = QTableWidgetItem(str(global_var.ACCOUNTS[key][2]
    #                                           if len(global_var.ACCOUNTS[key]) >= 3 else ''))
    #         self.tableWidget.insertRow(key)
    #         self.tableWidget.setItem(key, 0, username_item)
    #         self.tableWidget.setItem(key, 1, password_item)
    #         self.tableWidget.setItem(key, 2, alias_item)

    def _discard(self):
        print("用户点击了放弃按钮")
        self.reject()


class ManualValiDialogUi(Ui_MValiDialog, QDialog):
    vali_complete = Signal()

    def __init__(self, acc, url):
        super().__init__()
        self.setupUi(self)
        self.id = acc
        self._url = url
        self.buttonBox.rejected.connect(self._discard)  # Discard 按钮点击事件

    def _load(self):
        _base_url = QUrl("qrc:/")
        self._web_bridge = webbridge.ManualValiBri()
        self._web_bridge.close_dialog.connect(self.close_self)
        self._channel = QWebChannel()
        self._channel.registerObject('manualValiBri', self._web_bridge)
        # self._channel.registerObject("dialog", self)
        self.webEngineView.page().setWebChannel(self._channel)
        self.webEngineView.load(_base_url.resolved(QUrl(self._url)))
        # self.webEngineView.load(_base_url.resolved(QUrl('test.html')))
        # self.webEngineView.load(QUrl(':/test.html'))
        pass
        # self.webEngineView.page().webChannel().registerObject("dialog", self)
        # self.webEngineView.page().setWebChannel(self._channel)

    # def _load_test(self):
    #     _base_url = QUrl("qrc:/")
    #     self._web_bridge = webbridge.MyObject()
    #     self._channel = QWebChannel()
    #     self._channel.registerObject("myObject", self._web_bridge)
    #     # self.webEngineView.page().setWebChannel(_channel)
    #     # self.webEngineView.load(_base_url.resolved(QUrl(self._url)))
    #     self.webEngineView.load(_base_url.resolved(QUrl('test.html')))
    #     # self.webEngineView.load(QUrl(':/test.html'))
    #     pass
    #     self.webEngineView.page().setWebChannel(self._channel)

    def show(self) -> None:
        self._load()
        super().show()

    def close_self(self):
        self.vali_complete.emit()
        self.accept()

    def _discard(self):
        print("用户点击了放弃按钮")
        self.reject()


class SelectUnitsDialogUi(Ui_selectUnitDialog, QDialog):
    def __init__(self):
        super().__init__()
        from data import gamedata
        self._game_data = gamedata
        self._global_var = global_var
        self.setupUi(self)
        self._load_list_items()
        self._connect_slot()

    def _connect_slot(self):
        self.buttonBox.accepted.connect(self._accepted)  # Accepted 按钮点击事件
        self.buttonBox.rejected.connect(self._discard)  # Discard 按钮点击事件

        self.btnS.clicked.connect(lambda: self._move_items(from_list_widget=self.listUnS, to_list_widget=self.listS))
        self.btnSAll.clicked.connect(
            lambda: self._move_items(from_list_widget=self.listUnS, to_list_widget=self.listS, is_all=True))
        self.btnUnS.clicked.connect(lambda: self._move_items(from_list_widget=self.listS, to_list_widget=self.listUnS))
        self.btnUnSAll.clicked.connect(
            lambda: self._move_items(from_list_widget=self.listS, to_list_widget=self.listUnS, is_all=True))

        self.editSchS.textChanged.connect(lambda: self._search(list_widget=self.listS, keyword=self.editSchS.text()))
        self.editSchUnS.textChanged.connect(
            lambda: self._search(list_widget=self.listUnS, keyword=self.editSchUnS.text()))

    def _load_list_items(self):
        # _nicknames = self._global_var.NICKNAMES
        _nicknames = nk.nicknames
        all_units = self._game_data.all_units_simple_dict
        # selected_units = self._global_var.SELECTEDUNITS if self._global_var.SELECTEDUNITS else all_units.keys()
        selected_units = config_db.selected_units_db.query('units', [])
        selected_units = selected_units if selected_units else all_units.keys()
        complement_keys = set(all_units.keys()) - set(selected_units)
        for k in complement_keys:
            item = UnitListItem((k, _nicknames[k], all_units[k])) if k in _nicknames.keys() else UnitListItem(
                (k, all_units[k]))
            item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
            self.listUnS.addItem(item)
            # self._unselected_items.add(item)
        for k in selected_units:
            item = UnitListItem((k, _nicknames[k], all_units[k])) if k in _nicknames.keys() else UnitListItem(
                (k, all_units[k]))
            item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
            self.listS.addItem(item)
            # self._selected_items.add(item)

    @Slot()
    def _accepted(self):
        # _units_selected = [self.listS.item(i).unit_id for i in range(self.listS.count())]
        config_db.selected_units_db.update('units', [self.listS.item(i).unit_id for i in range(self.listS.count())])
        pass

    @Slot()
    def _discard(self):
        print("用户点击了放弃按钮")
        self.reject()

    @Slot()
    def _move_items(self, from_list_widget: QListWidget, to_list_widget: QListWidget, is_all: bool = False):
        if is_all:
            moving_items: list = [item for item in [from_list_widget.item(x) for x in range(from_list_widget.count())]
                                  if not item.isHidden()]
        else:
            moving_items: list = [item for item in from_list_widget.selectedItems() if not item.isHidden()]

        for item in moving_items:
            # row = self.listS.row(item)
            from_list_widget.takeItem(from_list_widget.row(item))
            to_list_widget.addItem(item)

        self._search(list_widget=to_list_widget, keyword='')

    @Slot()
    def _search(self, list_widget: QListWidget, keyword: str):
        list_widget.clearSelection()
        # for row in range(list_widget.count()):
        #     item = list_widget.item(row)
        for item in [list_widget.item(x) for x in range(list_widget.count())]:
            item.setHidden(keyword not in item.text())


class UnitListItem(QListWidgetItem):
    def __init__(self, data: tuple):
        """
        Custom List Item
        :param data: tuple, (unit_id, unit_name)
        """
        super().__init__("-".join(map(str, data)))
        self.unit_id = data[0]


class ValidateBtn(QPushButton):
    def __init__(self, acc: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDisabled(True)
        self.setText('Validate')
        self._acc = acc
        self._url = ''
        self.clicked.connect(self._show_manual_vali_dialog)

    def set_url(self, url):
        self._url = url

    @Slot(tuple)
    def _show_manual_vali_dialog(self):
        """
        在需要时显示手动过码对话框
        :return:
        """
        self._manual_vali_dialog = ManualValiDialogUi(acc=self._acc, url=self._url)
        self._manual_vali_dialog.vali_complete.connect(self.disable_self)
        self._manual_vali_dialog.show()

    @Slot()
    def disable_self(self):
        self.setDisabled(True)

    @Slot()
    def enable_self(self):
        self.setDisabled(False)


# 调试代码
if __name__ == '__main__':
    pass
