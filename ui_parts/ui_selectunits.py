# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_units.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QAbstractItemView, QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit,
                               QListWidget, QPushButton, QVBoxLayout, QWidget)


class Ui_selectUnitDialog(object):
    def setupUi(self, selectUnitDialog):
        if not selectUnitDialog.objectName():
            selectUnitDialog.setObjectName(u"selectUnitDialog")
        selectUnitDialog.setWindowModality(Qt.WindowModal)
        selectUnitDialog.resize(500, 500)
        selectUnitDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(selectUnitDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.vlayUnS = QVBoxLayout()
        self.vlayUnS.setObjectName(u"vlayUnS")
        self.labelUnS = QLabel(selectUnitDialog)
        self.labelUnS.setObjectName(u"labelUnS")

        self.vlayUnS.addWidget(self.labelUnS)

        self.editSchUnS = QLineEdit(selectUnitDialog)
        self.editSchUnS.setObjectName(u"editSchUnS")

        self.vlayUnS.addWidget(self.editSchUnS)

        self.listUnS = QListWidget(selectUnitDialog)
        self.listUnS.setObjectName(u"listUnS")
        self.listUnS.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listUnS.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listUnS.setSortingEnabled(True)

        self.vlayUnS.addWidget(self.listUnS)

        self.horizontalLayout.addLayout(self.vlayUnS)

        self.vlayBtn = QVBoxLayout()
        self.vlayBtn.setObjectName(u"vlayBtn")
        self.btnSAll = QPushButton(selectUnitDialog)
        self.btnSAll.setObjectName(u"btnSAll")

        self.vlayBtn.addWidget(self.btnSAll)

        self.btnS = QPushButton(selectUnitDialog)
        self.btnS.setObjectName(u"btnS")

        self.vlayBtn.addWidget(self.btnS)

        self.btnUnS = QPushButton(selectUnitDialog)
        self.btnUnS.setObjectName(u"btnUnS")

        self.vlayBtn.addWidget(self.btnUnS)

        self.btnUnSAll = QPushButton(selectUnitDialog)
        self.btnUnSAll.setObjectName(u"btnUnSAll")

        self.vlayBtn.addWidget(self.btnUnSAll)

        self.horizontalLayout.addLayout(self.vlayBtn)

        self.vlayS = QVBoxLayout()
        self.vlayS.setObjectName(u"vlayS")
        self.labelS = QLabel(selectUnitDialog)
        self.labelS.setObjectName(u"labelS")

        self.vlayS.addWidget(self.labelS)

        self.editSchS = QLineEdit(selectUnitDialog)
        self.editSchS.setObjectName(u"editSchS")

        self.vlayS.addWidget(self.editSchS)

        self.listS = QListWidget(selectUnitDialog)
        self.listS.setObjectName(u"listS")
        self.listS.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listS.setDragDropMode(QAbstractItemView.InternalMove)
        self.listS.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.vlayS.addWidget(self.listS)

        self.horizontalLayout.addLayout(self.vlayS)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(selectUnitDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.editSchUnS, self.listUnS)
        QWidget.setTabOrder(self.listUnS, self.btnSAll)
        QWidget.setTabOrder(self.btnSAll, self.btnS)
        QWidget.setTabOrder(self.btnS, self.btnUnS)
        QWidget.setTabOrder(self.btnUnS, self.btnUnSAll)
        QWidget.setTabOrder(self.btnUnSAll, self.editSchS)
        QWidget.setTabOrder(self.editSchS, self.listS)

        self.retranslateUi(selectUnitDialog)
        self.buttonBox.accepted.connect(selectUnitDialog.accept)
        self.buttonBox.rejected.connect(selectUnitDialog.reject)

        QMetaObject.connectSlotsByName(selectUnitDialog)

    # setupUi

    def retranslateUi(self, selectUnitDialog):
        selectUnitDialog.setWindowTitle(QCoreApplication.translate("selectUnitDialog", u"Select Units", None))
        self.labelUnS.setText(QCoreApplication.translate("selectUnitDialog", u"Unselected:", None))
        self.editSchUnS.setPlaceholderText(QCoreApplication.translate("selectUnitDialog", u"Search...", None))
        self.btnSAll.setText(QCoreApplication.translate("selectUnitDialog", u"->\n"
                                                                            "Add all\n"
                                                                            "->", None))
        self.btnS.setText(QCoreApplication.translate("selectUnitDialog", u"->\n"
                                                                         "Add\n"
                                                                         "->", None))
        self.btnUnS.setText(QCoreApplication.translate("selectUnitDialog", u"<-\n"
                                                                           "Remove\n"
                                                                           "<-", None))
        self.btnUnSAll.setText(QCoreApplication.translate("selectUnitDialog", u"<-\n"
                                                                              "Remove all\n"
                                                                              "<-", None))
        self.labelS.setText(QCoreApplication.translate("selectUnitDialog", u"Selected:", None))
        self.editSchS.setPlaceholderText(QCoreApplication.translate("selectUnitDialog", u"Search...", None))
    # retranslateUi
