# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QAbstractItemView, QDialogButtonBox, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QVBoxLayout)


class Ui_editDialog(object):
    def setupUi(self, editDialog):
        if not editDialog.objectName():
            editDialog.setObjectName(u"editDialog")
        editDialog.setWindowModality(Qt.ApplicationModal)
        editDialog.resize(360, 460)
        self.verticalLayout = QVBoxLayout(editDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnImport = QPushButton(editDialog)
        self.btnImport.setObjectName(u"btnImport")

        self.verticalLayout.addWidget(self.btnImport)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnAdd = QPushButton(editDialog)
        self.btnAdd.setObjectName(u"btnAdd")

        self.horizontalLayout.addWidget(self.btnAdd)

        self.btnRm = QPushButton(editDialog)
        self.btnRm.setObjectName(u"btnRm")

        self.horizontalLayout.addWidget(self.btnRm)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(editDialog)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setTextElideMode(Qt.ElideRight)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.tableWidget)

        self.buttonBox = QDialogButtonBox(editDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(editDialog)

        QMetaObject.connectSlotsByName(editDialog)

    # setupUi

    def retranslateUi(self, editDialog):
        editDialog.setWindowTitle(QCoreApplication.translate("editDialog", u"Edit accounts", None))
        self.btnImport.setText(QCoreApplication.translate("editDialog", u"Import...", None))
        self.btnAdd.setText(QCoreApplication.translate("editDialog", u"Add", None))
        self.btnRm.setText(QCoreApplication.translate("editDialog", u"Remove", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("editDialog", u"Username", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("editDialog", u"Password", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("editDialog", u"[Alias]", None));
    # retranslateUi
