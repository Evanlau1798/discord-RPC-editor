# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logging.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_logging_ui(object):
    def setupUi(self, logging_ui):
        logging_ui.setObjectName("logging_ui")
        logging_ui.resize(600, 500)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(logging_ui)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(logging_ui)
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(logging_ui)
        QtCore.QMetaObject.connectSlotsByName(logging_ui)

    def retranslateUi(self, logging_ui):
        _translate = QtCore.QCoreApplication.translate
        logging_ui.setWindowTitle(_translate("logging_ui", "discord狀態修改器執行紀錄"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    logging_ui = QtWidgets.QWidget()
    ui = Ui_logging_ui()
    ui.setupUi(logging_ui)
    logging_ui.show()
    sys.exit(app.exec_())
