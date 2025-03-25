import asyncio
from asyncio import Queue
from traceback import print_exc

from PySide6.QtCore import QThread, Signal, QObject, Slot
from PySide6.QtCore import Qt  # 导入Qt模块

# from datetime import datetime, timezone
from data import ExcelExporter, gamedata
from data import PcrAccount, JsonExporter
# from global_var import global_var
from data_db import acc_db, result_db, TimeUtils
from pcrapi.bsdk.validator import validate_dict


# from PySide6.QtGui import QColor

class DbInitializer(QThread):
    # start_signal = Signal()
    status_signal = Signal(str)
    complete_signal = Signal()

    def run(self):
        self.status_signal.emit('Initializing database')
        gamedata.db_initializer()
        self.complete_signal.emit()


class AsyncExporter(QThread):
    result_signal = Signal(bool, str)
    status_signal = Signal(str)

    # fail = Signal
    def __init__(self, file: str, json_only: bool = False, mode: bool = False):
        """
        Export Files
        :param file:
        :param mode:
        """
        super().__init__()
        self._exporter = None
        self._file = file
        self._mode = mode
        self._json_only = json_only
        # self._exporter = ExcelExporter(mode)
        # self._obj = obj
        # self._max_size = max_size

    def run(self):
        def export_xlsx():
            print("Selected file:", self._file)
            try:
                self._exporter = ExcelExporter(self._mode)
                self.status_signal.emit('Exporting')
                self._exporter.export_xlsx(self._file)
                self.result_signal.emit(True, '\n\n'.join(('Successfully export xlsx to', self._file)))
                self.status_signal.emit('Export success.')
            except Exception as e:
                print_exc()
                self.result_signal.emit(False, '\n\n'.join(('Export failed.', str(e))))
                self.status_signal.emit('Export failed')

        def export_json():
            print("Selected path:", self._file)
            try:
                self._exporter = JsonExporter()
                self.status_signal.emit('Exporting')
                self._exporter.export_json(self._file)
                self.result_signal.emit(True, '\n\n'.join(('Successfully export json to', self._file)))
                self.status_signal.emit('Export success.')
            except Exception as e:
                self.result_signal.emit(False, '\n\n'.join(('Export failed.', str(e))))
                self.status_signal.emit('Export failed')

        if self._json_only:
            export_json()
        else:
            export_xlsx()

    def export_json(self):
        print("Selected path:", self._file)


class AsyncWorker(QThread):
    status_signal = Signal(str)

    def __init__(self, obj, max_size):
        super().__init__()
        self._obj = obj
        self._max_size = max_size

    def run(self):
        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        asyncio.set_event_loop(loop)
        obj = Starter(max_size=self._max_size, mw_obj=self._obj)
        obj.status_signal.connect(lambda x: self.status_signal.emit(x))
        # Starter.complete_signal.connect(self.task_complete)
        # self._loop = asyncio.new_event_loop()
        # self._loop.set_debug(True)
        # self._loop.create_task(obj.start())
        # self._loop.run_forever()
        loop.run_until_complete(obj.start())

        loop.close()
        # self.finished.emit()


class Starter(QObject):
    complete_signal = Signal(str)
    status_signal = Signal(str)

    def __init__(self, max_size, mw_obj):
        super().__init__()
        self.complete_signal.connect(mw_obj.task_complete)
        self._queue = asyncio.Queue()
        self._max_size = max_size
        self._mw_obj = mw_obj

    async def start(self):
        try:
            _poller = DataPoller()
            _poller.m_vali_signal.connect(self._mw_obj.acquire_m_vali)
            _producer = Producer.produce(self._queue)
            self.status_signal.emit(f'Adding accounts to queue...')
            await _producer

            self.status_signal.emit(f'Starting poller...')
            _poller_task = asyncio.create_task(_poller.poll_dict())
            _consumers = []
            # Consumer.status_signal.connect(self._mw_obj.set_acc_status_text)
            # Consumer.time_signal.connect(self._mw_obj.set_last_time)
            for i in range(self._max_size):
                self.status_signal.emit(f'Creating thread {i}...')
                obj = Consumer(self._queue)
                obj.status_signal.connect(self._mw_obj.set_acc_status_text)
                obj.time_signal.connect(self._mw_obj.set_last_time)
                _consumers.append(asyncio.create_task(obj.consume()))

            self.status_signal.emit(f'Gathering results...')
            _rst_tup: tuple = await asyncio.gather(*_consumers)

            # _poller_task.cancel()
            self.status_signal.emit(f'Stopping poller...')
            try:
                _poller.stop()
                # _poller_task.cancel()
                await _poller_task
            except Exception as e:
                raise e

            # _results = {}
            # self.status_signal.emit('Updating results...')
            # for dic in _rst_tup:
            #     # 将字典更新
            #     _results.update(dic)
            # global_var.set_RESULTS(_results)
        except Exception as e:
            print_exc()
            try:
                _poller.stop()
                # _poller_task.cancel()
                await _poller_task
            except Exception:
                pass
            self.complete_signal.emit(f'Failed! {str(e)}')
        else:
            self.complete_signal.emit('Success!')


class DataPoller(QObject):
    # item_signal = Signal(str)
    m_vali_signal = Signal(str, str)

    def __init__(self):
        super().__init__()
        # self._btn_dict = btn_dict
        self._running = True

    @Slot()
    def stop(self):
        self._running = False

    async def poll_dict(self):
        while self._running:
            if validate_dict:
                temp_dict = validate_dict.copy()
                for acc in temp_dict:
                    if temp_dict[acc] != 'ok':
                        self.m_vali_signal.emit(acc, validate_dict[acc])
                        validate_dict.pop(acc)
            await asyncio.sleep(1)  # 1秒钟轮询一次


class Producer(object):
    @staticmethod
    async def produce(queue):
        # _data = global_var.ACCOUNTS
        for item in acc_db.db.all():
            await queue.put(item)


class Consumer(QObject):
    # 定义一个协程函数，用于消费数据
    status_signal = Signal(str, str, int)
    time_signal = Signal(str, str)

    def __init__(self, queue: Queue):
        super().__init__()
        self._queue = queue

    def _emit_status_signal(self, acc: str, text: str, color=None):
        self.status_signal.emit(acc, text, color)

    async def consume(self):
        results = []
        # 循环直到队列为空
        while not self._queue.empty():
            # 从队列中获取数据
            _item = await self._queue.get()  # 'accounts': acc, 'password': pwd
            # _acc = _item[1]  # 0:username, 1:password
            _acc_obj = PcrAccount(_item['acc'], _item['pwd'])
            self._emit_status_signal(_item['acc'], 'Login...')
            ret_val = await _acc_obj.login()
            if ret_val[0] != 0:
                self._emit_status_signal(_item['acc'], f'Err {ret_val[0]}: {ret_val[1]}', Qt.GlobalColor.red)
                self._queue.task_done()
                continue
            # await _acc_obj.login()
            self._emit_status_signal(_item['acc'], 'Gathering data...')
            _sum = _acc_obj.sum
            _query = result_db.get_query()
            result_db.db.remove(_query.acc == _item['acc'])
            result_db.db.upsert(_sum, _query.acc == _item['acc'])
            self.time_signal.emit(_item['acc'], TimeUtils.obj_localtime(_sum['time']).strftime("%Y-%m-%d %H:%M:%S"))
            self._emit_status_signal(_item['acc'], 'Complete!', Qt.GlobalColor.green)
            # results.append(_sum)
            # 任务完成
            self._queue.task_done()
            await asyncio.sleep(2)
        # return results
