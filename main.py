import os
import sys

# from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen
# noinspection PyUnresolvedReferences
from main_res_rc import *

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # global MAIN_PATH
    # os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "127.0.0.1:9222"
    # print(QStyleFactory.keys())
    app = QApplication(sys.argv)
    pixmap = QPixmap(":/autobox.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    splash.raise_()
    # splash.showMessage("Loading...", alignment=Qt.AlignCenter)
    import ui
    mW = ui.MainWindowUi()
    mW.show()
    splash.finish(mW)
    sys.exit(app.exec())
    # app.exec()
