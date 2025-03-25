# import os
import sys
import ui
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QGuiApplication
# from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QApplication, QSplashScreen
# noinspection PyUnresolvedReferences
from main_res_rc import *



# Uncomment below for terminal log messages
# import logging
# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    # # os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "127.0.0.1:9222"
    app = QApplication(sys.argv)
    # splash = QSplashScreen()
    # svg = QSvgWidget(":/autobox.svg", splash)
    # svg.setGeometry(0, 0, 320, 160)
    # # 设置QSplashScreen的大小和背景色
    # splash.resize(320, 160)
    # screen_size = QGuiApplication.primaryScreen().size()
    # splash_size = splash.size()
    # splash.move(int((screen_size.width() - splash_size.width()) / 2),
    #             int((screen_size.height() - splash_size.height()) / 2))
    # splash.show()
    # splash.raise_()
    # # splash.showMessage("Loading...", alignment=Qt.AlignBaseline)

    mW = ui.MainWindowUi()
    mW.show()
    # splash.finish(mW)
    sys.exit(app.exec())
    # app.exec()
