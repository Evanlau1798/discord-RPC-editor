# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'script_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_script_setting_ui(object):
    def setupUi(self, script_setting_ui):
        script_setting_ui.setObjectName("script_setting_ui")
        script_setting_ui.resize(712, 695)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(script_setting_ui)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rpc_edit_Description = QtWidgets.QLabel(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rpc_edit_Description.sizePolicy().hasHeightForWidth())
        self.rpc_edit_Description.setSizePolicy(sizePolicy)
        self.rpc_edit_Description.setObjectName("rpc_edit_Description")
        self.horizontalLayout.addWidget(self.rpc_edit_Description)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.script_textEdit = QtWidgets.QTextEdit(script_setting_ui)
        self.script_textEdit.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.script_textEdit.setFont(font)
        self.script_textEdit.setObjectName("script_textEdit")
        self.horizontalLayout_3.addWidget(self.script_textEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 10, -1, 10)
        self.horizontalLayout_6.setSpacing(5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.script_list_lable = QtWidgets.QLabel(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_list_lable.sizePolicy().hasHeightForWidth())
        self.script_list_lable.setSizePolicy(sizePolicy)
        self.script_list_lable.setObjectName("script_list_lable")
        self.horizontalLayout_6.addWidget(self.script_list_lable)
        self.script_list_combobox = QtWidgets.QComboBox(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_list_combobox.sizePolicy().hasHeightForWidth())
        self.script_list_combobox.setSizePolicy(sizePolicy)
        self.script_list_combobox.setMinimumSize(QtCore.QSize(0, 24))
        self.script_list_combobox.setMaximumSize(QtCore.QSize(16777215, 24))
        self.script_list_combobox.setObjectName("script_list_combobox")
        self.script_list_combobox.addItem("")
        self.script_list_combobox.addItem("")
        self.script_list_combobox.addItem("")
        self.script_list_combobox.addItem("")
        self.script_list_combobox.addItem("")
        self.script_list_combobox.addItem("")
        self.script_list_combobox.addItem("")
        self.script_list_combobox.addItem("")
        self.script_list_combobox.addItem("")
        self.script_list_combobox.addItem("")
        self.horizontalLayout_6.addWidget(self.script_list_combobox)
        spacerItem1 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.script_quantity_label = QtWidgets.QLabel(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_quantity_label.sizePolicy().hasHeightForWidth())
        self.script_quantity_label.setSizePolicy(sizePolicy)
        self.script_quantity_label.setObjectName("script_quantity_label")
        self.horizontalLayout_6.addWidget(self.script_quantity_label)
        self.show_script_quantity = QtWidgets.QLabel(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_script_quantity.sizePolicy().hasHeightForWidth())
        self.show_script_quantity.setSizePolicy(sizePolicy)
        self.show_script_quantity.setObjectName("show_script_quantity")
        self.horizontalLayout_6.addWidget(self.show_script_quantity)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.time_change_text_1 = QtWidgets.QLabel(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_change_text_1.sizePolicy().hasHeightForWidth())
        self.time_change_text_1.setSizePolicy(sizePolicy)
        self.time_change_text_1.setObjectName("time_change_text_1")
        self.horizontalLayout_6.addWidget(self.time_change_text_1)
        self.time_change_spinBox = QtWidgets.QSpinBox(script_setting_ui)
        self.time_change_spinBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_change_spinBox.sizePolicy().hasHeightForWidth())
        self.time_change_spinBox.setSizePolicy(sizePolicy)
        self.time_change_spinBox.setMaximumSize(QtCore.QSize(53, 16777215))
        self.time_change_spinBox.setSizeIncrement(QtCore.QSize(55, 0))
        self.time_change_spinBox.setMinimum(1)
        self.time_change_spinBox.setMaximum(9999)
        self.time_change_spinBox.setProperty("value", 1)
        self.time_change_spinBox.setObjectName("time_change_spinBox")
        self.horizontalLayout_6.addWidget(self.time_change_spinBox)
        self.time_change_text_2 = QtWidgets.QLabel(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_change_text_2.sizePolicy().hasHeightForWidth())
        self.time_change_text_2.setSizePolicy(sizePolicy)
        self.time_change_text_2.setObjectName("time_change_text_2")
        self.horizontalLayout_6.addWidget(self.time_change_text_2)
        spacerItem3 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.script_enable_checkBox = QtWidgets.QCheckBox(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_enable_checkBox.sizePolicy().hasHeightForWidth())
        self.script_enable_checkBox.setSizePolicy(sizePolicy)
        self.script_enable_checkBox.setObjectName("script_enable_checkBox")
        self.horizontalLayout_6.addWidget(self.script_enable_checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.close_script_editor_button = QtWidgets.QPushButton(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_script_editor_button.sizePolicy().hasHeightForWidth())
        self.close_script_editor_button.setSizePolicy(sizePolicy)
        self.close_script_editor_button.setMinimumSize(QtCore.QSize(0, 55))
        self.close_script_editor_button.setMaximumSize(QtCore.QSize(16777215, 55))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.close_script_editor_button.setFont(font)
        self.close_script_editor_button.setObjectName("close_script_editor_button")
        self.horizontalLayout_5.addWidget(self.close_script_editor_button)
        self.save_script_button = QtWidgets.QPushButton(script_setting_ui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_script_button.sizePolicy().hasHeightForWidth())
        self.save_script_button.setSizePolicy(sizePolicy)
        self.save_script_button.setMinimumSize(QtCore.QSize(0, 55))
        self.save_script_button.setMaximumSize(QtCore.QSize(16777215, 55))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_script_button.setFont(font)
        self.save_script_button.setObjectName("save_script_button")
        self.horizontalLayout_5.addWidget(self.save_script_button)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.retranslateUi(script_setting_ui)
        QtCore.QMetaObject.connectSlotsByName(script_setting_ui)

    def retranslateUi(self, script_setting_ui):
        _translate = QtCore.QCoreApplication.translate
        script_setting_ui.setWindowTitle(_translate("script_setting_ui", "狀態腳本設定"))
        self.rpc_edit_Description.setText(_translate("script_setting_ui", "格式說明 : 單行為單個狀態，多行狀態將會輪流接替"))
        self.script_list_lable.setText(_translate("script_setting_ui", "編輯的項目 :"))
        self.script_list_combobox.setItemText(0, _translate("script_setting_ui", "主標"))
        self.script_list_combobox.setItemText(1, _translate("script_setting_ui", "副標"))
        self.script_list_combobox.setItemText(2, _translate("script_setting_ui", "大圖標題"))
        self.script_list_combobox.setItemText(3, _translate("script_setting_ui", "大圖名稱"))
        self.script_list_combobox.setItemText(4, _translate("script_setting_ui", "小圖標題"))
        self.script_list_combobox.setItemText(5, _translate("script_setting_ui", "小圖名稱"))
        self.script_list_combobox.setItemText(6, _translate("script_setting_ui", "按鈕一標題"))
        self.script_list_combobox.setItemText(7, _translate("script_setting_ui", "按鈕一網址"))
        self.script_list_combobox.setItemText(8, _translate("script_setting_ui", "按鈕二標題"))
        self.script_list_combobox.setItemText(9, _translate("script_setting_ui", "按鈕二網址"))
        self.script_quantity_label.setText(_translate("script_setting_ui", "狀態總數 :"))
        self.show_script_quantity.setText(_translate("script_setting_ui", "1"))
        self.time_change_text_1.setText(_translate("script_setting_ui", "每"))
        self.time_change_text_2.setText(_translate("script_setting_ui", "秒更新下一個狀態"))
        self.script_enable_checkBox.setText(_translate("script_setting_ui", "啟用腳本"))
        self.close_script_editor_button.setText(_translate("script_setting_ui", "關閉編輯器"))
        self.save_script_button.setText(_translate("script_setting_ui", "儲存腳本並關閉編輯器"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    script_setting_ui = QtWidgets.QWidget()
    ui = Ui_script_setting_ui()
    ui.setupUi(script_setting_ui)
    script_setting_ui.show()
    sys.exit(app.exec_())