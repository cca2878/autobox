import asyncio
from asyncio import Queue

from PySide6.QtCore import QThread, Signal, QObject, Slot
from PySide6.QtCore import Qt  # 导入Qt模块

from data import Account, ExcelExporter, gamedata
from global_var import global_var
from pcrapi.bsdk.validator import validate_dict


# from PySide6.QtGui import QColor

class DbInitializer(QThread):
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
    def __init__(self, file: str):
        super().__init__()
        self._file = file
        self._exporter = ExcelExporter()
        # self._obj = obj
        # self._max_size = max_size

    def run(self):
        # selected_file = file_dialog.selectedFiles()[0]
        print("Selected file:", self._file)
        # self._exporter.preprocess_data()
        # self._exporter.export_xlsx(file_dialog.selectedFiles()[0])
        # _show_success_msgbox('\n'.join(('Successfully export to', file_dialog.selectedFiles()[0])))
        try:
            # self._exporter.preprocess_data()
            self.status_signal.emit('Exporting')
            self._exporter.export_xlsx(self._file)
            self.result_signal.emit(True, '\n'.join(('Successfully export to', self._file)))
            self.status_signal.emit('Export success.')
            # _show_success_msgbox('\n'.join(('Successfully export to', file_dialog.selectedFiles()[0])))
        except Exception as e:
            self.result_signal.emit(False, '\n'.join(('Export failed.', str(e))))
            self.status_signal.emit('Export failed')
            # traceback.print_exc()
            # _show_failed_msgbox('\n'.join(('Export failed.', str(e))))


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

            _results = {}
            self.status_signal.emit('Updating results...')
            for dic in _rst_tup:
                # 将字典更新
                _results.update(dic)
            global_var.set_RESULTS(_results)
        except Exception as e:
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
        # 生成limit个数据
        _data = global_var.ACCOUNTS
        # 将数据放入队列中
        for item in _data.items():
            await queue.put(item)


class Consumer(QObject):
    # 定义一个协程函数，用于消费数据
    status_signal = Signal(tuple)
    time_signal = Signal(tuple)

    def __init__(self, queue: Queue):
        super().__init__()
        self._queue = queue

    async def consume(self):
        results = {}
        # 循环直到队列为空
        while not self._queue.empty():
            # 从队列中获取数据
            _item = await self._queue.get()  # 0: idx, 1: acc list
            _acc = _item[1]  # 0:username, 1:password
            _acc_obj = Account(_acc[0], _acc[1])
            self.status_signal.emit((_item[0], 'Login...'))
            ret_val = await _acc_obj.login()
            if ret_val[0] != 0:
                self.status_signal.emit((_item[0], f'Err {ret_val[0]}: {ret_val[1]}', Qt.red))
                self._queue.task_done()
                continue
            # await _acc_obj.login()
            self.status_signal.emit((_item[0], 'Gathering data...'))
            _sum = _acc_obj.user_data_sum
            self.time_signal.emit((_item[0], _sum['time']))
            self.status_signal.emit((_item[0], 'Complete!', Qt.green))
            results[_item[0]] = _sum
            # 任务完成
            self._queue.task_done()
            await asyncio.sleep(2)
        return results


"""
class TaskThread(QThread):
    m_vali_signal = Signal()
    status_signal = Signal(tuple)
    time_signal = Signal(tuple)

    def __init__(self, idx: int, user: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_flag = True
        self._idx = idx
        self._user = user
        self._acc = Account(username=user[0], password=user[1])

    async def check_vali_dict(self):
        while not self._stop_flag:
            if self._user[0] in validate_dict:
                self.m_vali_signal.emit()
                self.status_signal.emit((self._idx, 'Waiting for manual validate!', Qt.red))
                break
            await asyncio.sleep(1)

    async def start_login(self):
        await self.status_signal.emit((self._idx, 'Login…'))
        return await self._acc.login()

    def run(self):

        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)

        async def main():
            task_login = _loop.create_task(_start_login())
            task_chk_dict = _loop.create_task(_check_vali_dict())

            await asyncio.gather(task_login, task_chk_dict)
            result = task_login.result()
            if result[0] != 0:
                self.status_signal.emit((self._idx, f'Err：{result[1]}', Qt.red))
                self._stop_flag = True
            else:
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._stop_flag = True
                self.status_signal.emit((self._idx, 'Complete!', Qt.green))
                self.time_signal.emit((self._idx, time))
                return {self._idx: [time, self._acc.user_data_sum]}

        _loop.run_until_complete(main())
        # asyncio.get_event_loop().create_task(self._acc.login())
"""
