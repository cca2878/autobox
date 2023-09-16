# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit.ui_parts'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt)
from PySide6.QtWidgets import (QAbstractItemView, QDialogButtonBox, QLabel, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem)


class Ui_editDialog(object):
    def setupUi(self, editDialog):
        if not editDialog.objectName():
            editDialog.setObjectName(u"editDialog")
        editDialog.setWindowModality(Qt.ApplicationModal)
        editDialog.resize(341, 458)
        self.tableWidget = QTableWidget(editDialog)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 90, 321, 361))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.btnAdd = QPushButton(editDialog)
        self.btnAdd.setObjectName(u"btnAdd")
        self.btnAdd.setGeometry(QRect(10, 10, 75, 24))
        self.btnRm = QPushButton(editDialog)
        self.btnRm.setObjectName(u"btnRm")
        self.btnRm.setGeometry(QRect(90, 10, 75, 24))
        self.inputUn = QLineEdit(editDialog)
        self.inputUn.setObjectName(u"inputUn")
        self.inputUn.setGeometry(QRect(10, 60, 113, 20))
        self.labelUn = QLabel(editDialog)
        self.labelUn.setObjectName(u"labelUn")
        self.labelUn.setGeometry(QRect(10, 40, 71, 16))
        self.labelPw = QLabel(editDialog)
        self.labelPw.setObjectName(u"labelPw")
        self.labelPw.setGeometry(QRect(130, 40, 71, 16))
        self.inputPw = QLineEdit(editDialog)
        self.inputPw.setObjectName(u"inputPw")
        self.inputPw.setGeometry(QRect(130, 60, 113, 20))
        self.buttonBox = QDialogButtonBox(editDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(260, 10, 71, 71))
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.btnSvts = QPushButton(editDialog)
        self.btnSvts.setObjectName(u"btnSvts")
        self.btnSvts.setGeometry(QRect(170, 10, 75, 24))

        self.retranslateUi(editDialog)

        QMetaObject.connectSlotsByName(editDialog)

    # setupUi

    def retranslateUi(self, editDialog):
        editDialog.setWindowTitle(QCoreApplication.translate("editDialog", u"Edit accounts", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("editDialog", u"Username", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("editDialog", u"Password", None))
        self.btnAdd.setText(QCoreApplication.translate("editDialog", u"Add", None))
        self.btnRm.setText(QCoreApplication.translate("editDialog", u"Remove", None))
        self.labelUn.setText(QCoreApplication.translate("editDialog", u"Username:", None))
        self.labelPw.setText(QCoreApplication.translate("editDialog", u"Password:", None))
        self.btnSvts.setText(QCoreApplication.translate("editDialog", u"Save this", None))
    # retranslateUi
