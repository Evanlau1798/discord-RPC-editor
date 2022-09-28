# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chooseSavedFile.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_start_ui(object):
    def setupUi(self, start_ui):
        start_ui.setObjectName("start_ui")
        start_ui.resize(600, 50)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(start_ui.sizePolicy().hasHeightForWidth())
        start_ui.setSizePolicy(sizePolicy)
        start_ui.setMinimumSize(QtCore.QSize(600, 50))
        start_ui.setMaximumSize(QtCore.QSize(600, 50))
        self.horizontalLayoutWidget = QtWidgets.QWidget(start_ui)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 601, 58))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 5, 0, 15)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 28))
        self.label.setMaximumSize(QtCore.QSize(16777215, 28))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(144, 28))
        self.comboBox.setMaximumSize(QtCore.QSize(144, 28))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.Enter = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Enter.setMinimumSize(QtCore.QSize(0, 28))
        self.Enter.setMaximumSize(QtCore.QSize(50, 28))
        self.Enter.setObjectName("Enter")
        self.horizontalLayout.addWidget(self.Enter)
        self.go_to_dev_web_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go_to_dev_web_button.sizePolicy().hasHeightForWidth())
        self.go_to_dev_web_button.setSizePolicy(sizePolicy)
        self.go_to_dev_web_button.setMinimumSize(QtCore.QSize(0, 28))
        self.go_to_dev_web_button.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.go_to_dev_web_button.setFont(font)
        self.go_to_dev_web_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.go_to_dev_web_button.setStyleSheet("color: rgb(64, 78, 237);")
        self.go_to_dev_web_button.setAutoDefault(False)
        self.go_to_dev_web_button.setDefault(False)
        self.go_to_dev_web_button.setFlat(True)
        self.go_to_dev_web_button.setObjectName("go_to_dev_web_button")
        self.horizontalLayout.addWidget(self.go_to_dev_web_button)

        self.retranslateUi(start_ui)
        QtCore.QMetaObject.connectSlotsByName(start_ui)

    def retranslateUi(self, start_ui):
        _translate = QtCore.QCoreApplication.translate
        start_ui.setWindowTitle(_translate("start_ui", "初始設定"))
        self.label.setText(_translate("start_ui", "請選擇存檔或輸入Discord APP Id:"))
        self.Enter.setText(_translate("start_ui", "確定"))
        self.go_to_dev_web_button.setText(_translate("start_ui", "點我前往Dc Dev網站"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    start_ui = QtWidgets.QWidget()
    ui = Ui_start_ui()
    ui.setupUi(start_ui)
    start_ui.show()
    sys.exit(app.exec_())
