import json

from PySide6.QtCore import QObject, Slot, Signal

from pcrapi.bsdk.validator import validate_ok_dict


class ManualValiBri(QObject):
    close_dialog = Signal()

    def __init__(self):
        super().__init__()

    # 槽函数，vali成功时触发。
    @Slot(str)
    def vali_complete(self, text):
        # data = await request.get_json()
        # validate_ok_dict
        data = json.loads(text)
        print(data)
        if 'id' not in data:
            raise Exception('Invalid Data')
            # return "incorrect", 403
        else:
            # print(data)
            acc = data['id']
            validate_ok_dict[acc] = data
            self.close_dialog.emit()

# class MyObject(QObject):
#     def __init__(self):
#         super().__init__()
#
#     # 定义一个信号，它将在Web页面上的按钮点击时发射
#     my_signal = Signal(str)
#
#     @Slot(str)
#     def webButtonClicked(self, text):
#         # 当Web页面上的按钮点击时，这个方法会被调用
#         print(f"Button clicked on the web page: {text}")
#         self.my_signal.emit(f"Button clicked on the web page: {text}")
