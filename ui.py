# -*- coding: utf-8 -*-

# import os
from PySide6.QtCore import QUrl, Slot, Signal, Qt
# from PySide6.QtGui import QBrush
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import QMainWindow, QDialog, QTableWidgetItem, QFileDialog, QPushButton, QWidget, \
    QMessageBox, QListWidget, QListWidgetItem, QHeaderView

import webbridge
from global_var import global_var
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
        self._col_idx = {'index': 0, 'username': 1, 'status': 2, 'manual_vali': 3, 'last_time': 4}
        # self._exporter = ExcelExporter()
        self.setupUi(self)
        self.show()
        # self.statusBar.showMessage('Ready.')
        # self.set_status_text('Ready')
        self._startup()
        # self._load()

    def _startup(self):
        self._set_components_status(False)
        self.set_status_text('')
        self.btnStart.clicked.connect(self._start_tasks)
        self.btnEdit.clicked.connect(self._show_edit_dialog)
        self.btnOutput.clicked.connect(self._export_file)
        self.btnSelectU.clicked.connect(self._show_select_units_dialog)

        def _db_complete():
            self.set_status_text('Loading accounts')
            try:
                self._load()
                self.set_status_text('Ready')
                self._set_components_status(True)
            except Exception as e:
                self.set_status_text(f'Err! {str(e)}')
            del self._db_init

        self._db_init = DbInitializer()
        self._db_init.status_signal.connect(self.set_status_text)
        self._db_init.complete_signal.connect(_db_complete)
        self._db_init.start()

    def _show_edit_dialog(self):
        self._edit_dialog = EditDialogUi()
        self._edit_dialog.finished.connect(self._edit_dialog_finished)
        self._edit_dialog.show()

    def _show_select_units_dialog(self):
        self._selectU_dialog = SelectUnitsDialogUi()
        # self._selectU_dialog.finished.connect(self._edit_dialog_finished)
        self._selectU_dialog.show()

    def _export_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter('Excel Workbook (*.xlsx)')

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
            self._set_components_status(True)

        if file_dialog.exec() == QFileDialog.Accepted:
            self._set_components_status(False)
            self._exporter = AsyncExporter(file_dialog.selectedFiles()[0])
            self._exporter.result_signal.connect(_show_msgbox)
            self._exporter.status_signal.connect(self.set_status_text)
            self._exporter.start()
            # selected_file = file_dialog.selectedFiles()[0]
            # print("Selected file:", selected_file)
            # self._exporter.preprocess_data()
            # self._exporter.export_xlsx(file_dialog.selectedFiles()[0])
            # _show_success_msgbox('\n'.join(('Successfully export to', file_dialog.selectedFiles()[0])))
            # try:
            #     # self._exporter.preprocess_data()
            #     self._exporter.export_xlsx(file_dialog.selectedFiles()[0])
            #     _show_success_msgbox('\n'.join(('Successfully export to', file_dialog.selectedFiles()[0])))
            # except Exception as e:
            #     traceback.print_exc()
            #     _show_failed_msgbox('\n'.join(('Export failed.', str(e))))

    def _edit_dialog_finished(self, result):
        if result == QDialog.Accepted:
            self._load()
            if not self.tableWidget.rowCount() == 0:
                self.btnStart.setEnabled(True)

            # _acc = self._edit_dialog.get_accounts()
            # global_var.set_ACCOUNTS(_acc)
            # self._storage_mgr.save_accounts()
            # print(f"Dialog Info: {global_var.ACCOUNTS}")

        # self._load()

    def _load(self):
        if not global_var.ACCOUNTS:
            self.btnStart.setEnabled(False)
        if not global_var.RESULTS:
            self.btnOutput.setEnabled(False)
        self.tableWidget.setRowCount(0)
        self._buttons = {}

        def _add_table_item():
            results = global_var.RESULTS
            accounts = global_var.ACCOUNTS
            for key in accounts:
                if accounts[key]:
                    index_item = QTableWidgetItem(str(key + 1))
                    if len(accounts[key]) > 2:
                        if accounts[key][2]:
                            acc = f'{accounts[key][2]}({accounts[key][0]})'
                        else:
                            acc = accounts[key][0]
                    else:
                        acc = accounts[key][0]
                    username_item = QTableWidgetItem(str(acc))
                    status_item = QTableWidgetItem('Waiting…')
                    time_item = QTableWidgetItem(str(results[key]['time'] if key in results else ''))
                    # password_item = QTableWidgetItem(str(global_var.ACCOUNTS[key][1]))
                    self.tableWidget.insertRow(key)
                    self.tableWidget.setItem(key, self._col_idx['index'], index_item)
                    self.tableWidget.setItem(key, self._col_idx['username'], username_item)
                    self.tableWidget.setItem(key, self._col_idx['status'], status_item)
                    self.tableWidget.setItem(key, self._col_idx['last_time'], time_item)
                    self._buttons[accounts[key][0]] = ValidateBtn(acc=accounts[key][0])
                    self.tableWidget.setCellWidget(key, self._col_idx['manual_vali'], self._buttons[accounts[key][0]])

        self.tableWidget.horizontalHeader().setSectionResizeMode(self._col_idx['index'], QHeaderView.ResizeToContents)
        _add_table_item()

    @Slot(tuple)
    def set_acc_status_text(self, info: tuple):
        """
        设置status
        :param info: tuple, (self._idx, 'status_str', color: qt.color（可选）)
        :return:
        """
        # acc_map = global_var.ACCMAP
        if len(info) == 3:
            brush = info[2]
        else:
            brush = None
        status_item = QTableWidgetItem(info[1])
        # status_item.setForeground(brush)
        self.tableWidget.setItem(info[0], self._col_idx['status'], status_item)

    @Slot(str)
    def set_status_text(self, text):
        self.statusBar.showMessage(f'Status: {text}...')

    @Slot(tuple)
    def set_last_time(self, info):
        """
        设置last time
        :param info: tuple, (self._idx, str: datetime)
        :return:
        """
        time_item = QTableWidgetItem(info[1])
        self.tableWidget.setItem(info[0], self._col_idx['last_time'], time_item)

    @Slot(str, str)
    def acquire_m_vali(self, acc, url):
        acc_map = global_var.ACCMAP
        self._buttons[acc].set_url(url)
        self._buttons[acc].enable_self()
        self.set_acc_status_text((acc_map[acc], 'Need manual validate!', Qt.red))

    @Slot(str)
    def task_complete(self, text):
        self._set_components_status(True)
        self.set_status_text(text)
        if global_var.RESULTS:
            self.btnOutput.setEnabled(True)
        del self._worker

    def _set_components_status(self, status: bool):
        for item in self.groupBox.findChildren(QWidget):
            item.setEnabled(status)
        self.btnStart.setEnabled(status)
        self.btnOutput.setEnabled(status)

    def _start_tasks(self):
        self._set_components_status(False)
        self._worker = AsyncWorker(obj=self, max_size=self.spboxThNum.value())
        self._worker.status_signal.connect(self.set_status_text)
        self._worker.start()

        # from task import Starter
        # obj = Starter(max_size=self.spboxThNum.value(), mw_obj=self)
        # asyncio.run(obj.start(), debug=True)


class EditDialogUi(Ui_editDialog, QDialog):
    def __init__(self):
        super().__init__()
        self._accounts = {}
        self.setupUi(self)
        self._load()
        self.btnAdd.clicked.connect(self._add_account)
        self.btnRm.clicked.connect(self._remove_account)
        # self.btnSvts.clicked.connect(self._save_account)
        # self.tableWidget.cellClicked.connect(self._update_input)
        self.buttonBox.rejected.connect(self._discard)  # Discard 按钮点击事件
        self.buttonBox.accepted.connect(self._save)  # Save 按钮点击事件

    def _add_account(self):
        # username_item = QTableWidgetItem(str(self.inputUn.text()))
        # password_item = QTableWidgetItem(str(self.inputPw.text()))
        row_position = self.tableWidget.rowCount()  # 获取当前行数
        self.tableWidget.insertRow(row_position)  # 插入新行
        self.tableWidget.setItem(row_position, 2, QTableWidgetItem())
        # self.tableWidget.setItem(row_position, 1, password_item)
        self.tableWidget.setCurrentCell(row_position, 0)
        # self.inputUn.setText('')
        # self.inputPw.setText('')

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

        # if selected_items:
        #     self.tableWidget.removeRow(self.tableWidget.selectedItems()[0].row())
        # else:
        #     pass

    # def _update_input(self):
    #     selected_items = self.tableWidget.selectedItems()
    #     if selected_items:
    #         username = selected_items[0].text()
    #         password = selected_items[1].text()
    #         self.inputUn.setText(username)
    #         self.inputPw.setText(password)
    #     else:
    #         self.inputUn.setText("")
    #         self.inputPw.setText("")

    # def _save_account(self):
    #     if self.tableWidget.selectedItems():
    #         username_item = QTableWidgetItem(str(self.inputUn.text()))
    #         password_item = QTableWidgetItem(str(self.inputPw.text()))
    #         row_position = self.tableWidget.selectedItems()[0].row()  # 获取当前行数
    #         self.tableWidget.setItem(row_position, 0, username_item)
    #         self.tableWidget.setItem(row_position, 1, password_item)

    def _save(self):
        # cell_contents = []
        temp_set = set()
        temp_dict = {}
        index = -1
        for row in range(self.tableWidget.rowCount()):
            temp_list = []
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item and (item.text() != '' or col > 1):
                    temp_list.append(item.text())
                else:
                    break
            else:
                if temp_list[0] not in temp_set:
                    index += 1
                    temp_set.add(temp_list[0])
                    temp_dict[index] = temp_list
                # temp_dict[index] = temp_list
        global_var.set_ACCOUNTS(temp_dict)
        print("用户点击了保存按钮")
        self.accept()

    def _load(self):
        for key in global_var.ACCOUNTS:
            if global_var.ACCOUNTS[key]:
                username_item = QTableWidgetItem(str(global_var.ACCOUNTS[key][0]))
                password_item = QTableWidgetItem(str(global_var.ACCOUNTS[key][1]))
                alias_item = QTableWidgetItem(str(global_var.ACCOUNTS[key][2]
                                                  if len(global_var.ACCOUNTS[key]) >= 3 else ''))
                self.tableWidget.insertRow(key)
                self.tableWidget.setItem(key, 0, username_item)
                self.tableWidget.setItem(key, 1, password_item)
                self.tableWidget.setItem(key, 2, alias_item)

    def _discard(self):
        print("用户点击了放弃按钮")
        self.reject()

    def get_accounts(self):
        return self._accounts


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
        _nicknames = self._global_var.NICKNAMES
        all_units = self._game_data.all_units_simple_dict
        selected_units = self._global_var.SELECTEDUNITS if self._global_var.SELECTEDUNITS else all_units.keys()
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
        _units_selected = [self.listS.item(i).unit_id for i in range(self.listS.count())]
        self._global_var.set_SELECTEDUNITS(_units_selected)
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
