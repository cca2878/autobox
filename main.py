import os
import sys

# from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QApplication, QSplashScreen
# noinspection PyUnresolvedReferences
from main_res_rc import *

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # global MAIN_PATH
    # os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "127.0.0.1:9222"
    # print(QStyleFactory.keys())
    app = QApplication(sys.argv)
    splash = QSplashScreen()
    # pixmap = QPixmap(":/autobox.png")
    svg = QSvgWidget(":/autobox.svg", splash)
    # 设置QSvgWidget的大小和位置
    svg.setGeometry(0, 0, 320, 160)
    # 设置QSplashScreen的大小和背景色
    splash.resize(320, 160)
    screen_size = QGuiApplication.primaryScreen().size()
    # 获取QSplashScreen的大小
    splash_size = splash.size()
    # 使用move()方法将QSplashScreen移动到屏幕的中心位置
    splash.move((screen_size.width() - splash_size.width()) / 2, (screen_size.height() - splash_size.height()) / 2)
    splash.show()
    splash.raise_()
    # splash.showMessage("Loading...", alignment=Qt.AlignCenter)
    import ui
    mW = ui.MainWindowUi()
    mW.show()
    splash.finish(mW)
    sys.exit(app.exec())
    # app.exec()
