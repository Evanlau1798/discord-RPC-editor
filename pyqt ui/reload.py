# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reload.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_restart_ui(object):
    def setupUi(self, restart_ui):
        restart_ui.setObjectName("restart_ui")
        restart_ui.resize(300, 75)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(restart_ui.sizePolicy().hasHeightForWidth())
        restart_ui.setSizePolicy(sizePolicy)
        restart_ui.setMinimumSize(QtCore.QSize(300, 75))
        restart_ui.setMaximumSize(QtCore.QSize(300, 75))
        self.horizontalLayoutWidget = QtWidgets.QWidget(restart_ui)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 301, 35))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(restart_ui)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 40, 301, 49))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(10, 0, 10, 20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.No_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.No_button.setObjectName("No_button")
        self.horizontalLayout_2.addWidget(self.No_button)
        self.yes_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.yes_button.setObjectName("yes_button")
        self.horizontalLayout_2.addWidget(self.yes_button)

        self.retranslateUi(restart_ui)
        QtCore.QMetaObject.connectSlotsByName(restart_ui)

    def retranslateUi(self, restart_ui):
        _translate = QtCore.QCoreApplication.translate
        restart_ui.setWindowTitle(_translate("restart_ui", "更換確認"))
        self.label.setText(_translate("restart_ui", "確定要更換存檔嗎?"))
        self.No_button.setText(_translate("restart_ui", "否"))
        self.yes_button.setText(_translate("restart_ui", "是的!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    restart_ui = QtWidgets.QDialog()
    ui = Ui_restart_ui()
    ui.setupUi(restart_ui)
    restart_ui.show()
    sys.exit(app.exec_())
