# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'autobox.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize)
from PySide6.QtWidgets import (QAbstractItemView, QCheckBox, QGroupBox,
                               QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpinBox, QStatusBar,
                               QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(570, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(0, 104))
        self.checkBoxSep = QCheckBox(self.groupBox)
        self.checkBoxSep.setObjectName(u"checkBoxSep")
        self.checkBoxSep.setGeometry(QRect(20, 70, 211, 31))
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkBoxSep.sizePolicy().hasHeightForWidth())
        self.checkBoxSep.setSizePolicy(sizePolicy1)
        self.btnEdit = QPushButton(self.groupBox)
        self.btnEdit.setObjectName(u"btnEdit")
        self.btnEdit.setGeometry(QRect(270, 20, 100, 30))
        self.labelThreads = QLabel(self.groupBox)
        self.labelThreads.setObjectName(u"labelThreads")
        self.labelThreads.setGeometry(QRect(20, 20, 51, 21))
        self.spboxThNum = QSpinBox(self.groupBox)
        self.spboxThNum.setObjectName(u"spboxThNum")
        self.spboxThNum.setGeometry(QRect(80, 20, 61, 22))
        self.spboxThNum.setMinimum(1)
        self.spboxThNum.setMaximum(8)
        self.btnSelectU = QPushButton(self.groupBox)
        self.btnSelectU.setObjectName(u"btnSelectU")
        self.btnSelectU.setGeometry(QRect(270, 60, 100, 30))
        self.checkBoxRaw = QCheckBox(self.groupBox)
        self.checkBoxRaw.setObjectName(u"checkBoxRaw")
        self.checkBoxRaw.setGeometry(QRect(20, 50, 201, 20))

        self.horizontalLayout.addWidget(self.groupBox)

        self.verticalWidget_2 = QWidget(self.centralwidget)
        self.verticalWidget_2.setObjectName(u"verticalWidget_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.verticalWidget_2.sizePolicy().hasHeightForWidth())
        self.verticalWidget_2.setSizePolicy(sizePolicy2)
        self.verticalLayout_2 = QVBoxLayout(self.verticalWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btnStart = QPushButton(self.verticalWidget_2)
        self.btnStart.setObjectName(u"btnStart")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btnStart.sizePolicy().hasHeightForWidth())
        self.btnStart.setSizePolicy(sizePolicy3)
        self.btnStart.setFlat(False)

        self.verticalLayout_2.addWidget(self.btnStart)

        self.btnOutput = QPushButton(self.verticalWidget_2)
        self.btnOutput.setObjectName(u"btnOutput")
        sizePolicy3.setHeightForWidth(self.btnOutput.sizePolicy().hasHeightForWidth())
        self.btnOutput.setSizePolicy(sizePolicy3)

        self.verticalLayout_2.addWidget(self.btnOutput)

        self.horizontalLayout.addWidget(self.verticalWidget_2)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy4)
        self.tableWidget.setMinimumSize(QSize(0, 470))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_3.addWidget(self.tableWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
        QWidget.setTabOrder(self.spboxThNum, self.checkBoxSep)
        QWidget.setTabOrder(self.checkBoxSep, self.btnEdit)
        QWidget.setTabOrder(self.btnEdit, self.btnSelectU)
        QWidget.setTabOrder(self.btnSelectU, self.btnStart)
        QWidget.setTabOrder(self.btnStart, self.btnOutput)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Autobox", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.checkBoxSep.setText(QCoreApplication.translate("MainWindow", u"Separate info&&data when export", None))
        self.btnEdit.setText(QCoreApplication.translate("MainWindow", u"Edit accounts...", None))
        self.btnEdit.setProperty("test", QCoreApplication.translate("MainWindow", u"abc", None))
        self.labelThreads.setText(QCoreApplication.translate("MainWindow", u"Threads:", None))
        self.btnSelectU.setText(QCoreApplication.translate("MainWindow", u"Select Units...", None))
        self.checkBoxRaw.setText(QCoreApplication.translate("MainWindow", u"Only export raw data json", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btnOutput.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Index", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Account", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"ManualVali", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"LastTime", None));
    # retranslateUi
