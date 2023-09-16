# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manual_vali.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QDialogButtonBox,
                               QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout)
# import validator_res_rc

class Ui_MValiDialog(object):
    def setupUi(self, MValiDialog):
        if not MValiDialog.objectName():
            MValiDialog.setObjectName(u"MValiDialog")
        MValiDialog.resize(380, 450)
        MValiDialog.setMinimumSize(QSize(380, 400))
        self.verticalLayout = QVBoxLayout(MValiDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(MValiDialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout.addWidget(self.label)

        self.buttonBox = QDialogButtonBox(MValiDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.webEngineView = QWebEngineView(MValiDialog)
        self.webEngineView.setObjectName(u"webEngineView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.webEngineView.sizePolicy().hasHeightForWidth())
        self.webEngineView.setSizePolicy(sizePolicy1)
        self.webEngineView.setMinimumSize(QSize(0, 400))

        self.verticalLayout.addWidget(self.webEngineView)


        self.retranslateUi(MValiDialog)

        QMetaObject.connectSlotsByName(MValiDialog)
    # setupUi

    def retranslateUi(self, MValiDialog):
        MValiDialog.setWindowTitle(QCoreApplication.translate("MValiDialog", u"Manual Validate", None))
        self.label.setText(QCoreApplication.translate("MValiDialog", u"Please complete the validation in 120s!", None))
    # retranslateUi

