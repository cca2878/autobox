# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_acc.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QAbstractScrollArea, QCheckBox,
                               QDialogButtonBox, QLabel, QPlainTextEdit,
                               QVBoxLayout)


class Ui_importAccDialog(object):
    def setupUi(self, importAccDialog):
        if not importAccDialog.objectName():
            importAccDialog.setObjectName(u"importAccDialog")
        importAccDialog.resize(380, 400)
        importAccDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(importAccDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(importAccDialog)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.MarkdownText)

        self.verticalLayout.addWidget(self.label)

        self.checkBoxOverwrite = QCheckBox(importAccDialog)
        self.checkBoxOverwrite.setObjectName(u"checkBoxOverwrite")

        self.verticalLayout.addWidget(self.checkBoxOverwrite)

        self.editImport = QPlainTextEdit(importAccDialog)
        self.editImport.setObjectName(u"editImport")
        self.editImport.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.verticalLayout.addWidget(self.editImport)

        self.buttonBox = QDialogButtonBox(importAccDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(importAccDialog)
        self.buttonBox.accepted.connect(importAccDialog.accept)
        self.buttonBox.rejected.connect(importAccDialog.reject)

        QMetaObject.connectSlotsByName(importAccDialog)

    # setupUi

    def retranslateUi(self, importAccDialog):
        importAccDialog.setWindowTitle(QCoreApplication.translate("importAccDialog", u"Import Accounts", None))
        self.label.setText(QCoreApplication.translate("importAccDialog",
                                                      u"Input only one account as \"username|password[|alias]\" per line.\n"
                                                      "\n"
                                                      "Example: \"acc_a|pwd_a\" or \"acc_b|pwd_b|alias_b\".", None))
        self.checkBoxOverwrite.setText(
            QCoreApplication.translate("importAccDialog", u"Overwrite existing accounts", None))
        self.editImport.setPlaceholderText(
            QCoreApplication.translate("importAccDialog", u"username|password[|alias]", None))
    # retranslateUi
