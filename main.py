import os
import sys

from PySide6.QtWidgets import QApplication

import ui

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # global MAIN_PATH
    # os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "127.0.0.1:9222"
    # print(QStyleFactory.keys())
    app = QApplication(sys.argv)
    mW = ui.MainWindowUi()
    sys.exit(app.exec())
    # app.exec()
