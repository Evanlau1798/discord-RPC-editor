from os import execlp,listdir,path
from time import time,sleep
from pypresence import Presence
from threading import Thread
from webbrowser import open_new
from json import load,dumps
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QMessageBox,QWidget, QApplication, QShortcut, QMainWindow,QSystemTrayIcon, QMenu, QAction
import qdarktheme
import sys
from pystray import Icon as pyicon, MenuItem as item
from PIL import Image

RPC_cur_stat = "狀態未啟動"
file_title = ""

class discord_act:
    def __init__(self,id,title):
        try:
            print("start init discord_act")
            self.cur_start = True
            self.app = Presence(id)
            self.app.connect()
            self.get_stored_data(id, title)
            self.stop = False
            self.cur_start = False
        except Exception as e:
            err_code = ['result','存取被拒','Could not find Discord installed and running on this machine.']
            for i in err_code:
                if i in str(e):
                    raise Exception(f"Discord似乎未正確啟動\n您可以嘗試以下方法進行問題排解\n\n1.請確保已啟動Discord\n2.若Discord已開啟，請重新啟動修改器\n3.若Discord是以管理員權限運行，請以正常權限啟動Discord，或是以管理員模式啟動修改器\n\n若問題持續發生\n請直接截圖並私訊作者 Evanlau#0857 回報問題\n\n錯誤碼:{e}")
            raise Exception(e)
    
    def get_stored_data(self,id,title):
        print("get_stored_data")
        with open(f'./data/{title}.json',encoding="UTF-8",mode="r") as json_file:
            data = load(json_file)
            print(data)
            self.detail = data.get("User_stored_stat",{}).get("detail","")
            self.stat = data.get("User_stored_stat",{}).get("stat","")
            self.pic = data.get("User_stored_stat",{}).get("pic","")
            self.pic_text = data.get("User_stored_stat",{}).get("pic_text","")
            self.small_pic = data.get("User_stored_stat",{}).get("small_pic","")
            self.small_pic_text = data.get("User_stored_stat",{}).get("small_pic_text","")
            self.time_count = data.get("User_stored_stat",{}).get("time_counting",False)
            self.button_1_title = data.get("User_stored_stat",{}).get("button_1_title","")
            self.button_1_url = data.get("User_stored_stat",{}).get("button_1_url","")
            self.button_1_activate = data.get("User_stored_stat",{}).get("button_1_activate",False)
            self.button_2_title = data.get("User_stored_stat",{}).get("button_2_title","")
            self.button_2_url = data.get("User_stored_stat",{}).get("button_2_url","")
            self.button_2_activate = data.get("User_stored_stat",{}).get("button_2_activate",False)
        json_file.close()
        print(self.stat,self.pic,self.pic_text)
        return

    def set_act(self,stat,detail,pic,pic_text,small_pic,small_pic_text,time_set,time_mode,time_stamp,buttons):
        print("set_act")
        global RPC_cur_stat
        instance = True
        try:
            if time_set == False:
                self.app.update(state=stat,details=detail,large_image=pic,large_text=pic_text,small_image=small_pic,small_text=small_pic_text,instance=instance,buttons=buttons)
            else:
                cur_time = int(time())
                if time_mode == "從零開始":
                    start_time_stamp = cur_time
                    end_time_stamp = None
                elif time_mode == "經過時間":
                    if time_stamp > cur_time:
                        msg_box.warning("錯誤", "經過時間為負數")
                        RPC_cur_stat = "狀態設定失敗"
                        return
                    start_time_stamp = time_stamp
                    end_time_stamp = None
                elif time_mode == "剩餘時間":
                    if time_stamp < cur_time:
                        msg_box.warning("錯誤", "剩餘時間為負數")
                        RPC_cur_stat = "狀態設定失敗"
                        return
                    start_time_stamp = None
                    end_time_stamp = time_stamp
                self.app.update(state=stat,details=detail,large_image=pic,large_text=pic_text,small_image=small_pic,small_text=small_pic_text,instance=instance,start=start_time_stamp,end=end_time_stamp,buttons=buttons)
            RPC_cur_stat = "狀態設定成功"
        except Exception as e:
            RPC_cur_stat = "狀態設定失敗"
            if 'must be a valid uri' in str(e):
                msg_box.warning('錯誤', '您輸入的網址不是正確的網址\n網址須加上http://或https://')
            else:
                msg_box.warning('錯誤', e)

    def state(self):
        print("start state")
        try:
            while 1:
                if self.stop == True:
                    self.stop = False
                    return
                else:
                    sleep(1/10)
        except Exception as e:
            e = str(e)
            if "result" in e:
                msg_box.warning("錯誤", f"狀態設定錯誤\n請重新啟動discord後再試一次\n若問題持續發生\n請私訊作者 Evanlau#0857 回報問題\n錯誤碼:{e}")
            else:
                raise Exception(e)
    
    def act_thread(self):
        print("start act thread")
        try:
            if self.state_thread:
                self.stop = True
                sleep(1/10)
                self.state_thread = Thread(target = self.state, daemon = True)
                self.state_thread.start()
        except:
            self.state_thread = Thread(target = self.state, daemon = True)
            self.state_thread.start()

class ctrl_GUI:
    def __init__(self,dir_list):
        print("start discord game state")
        self.dir_list = dir_list
        self.test = False
        self.stop = True
        self.save_window = None
        self._init_discord_act(file_title)

    '''def _init_system_tray(self):
        print("system_tray")
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setToolTip("Discord狀態修改器")
        self.tray.activated.connect(self.iconActivated)
        self.tray.setVisible(True)
        self.tray.hide()'''

    def show_system_tray(self):
        print("system_tray")
        self.ctrl_GUI.hide()
        image = Image.open("./lib/icon.png")
        self.stop = False
        menu=(item('開啟修改器視窗',self.iconActivated,checked=lambda item: self.test), item('關閉狀態修改器', self.close_all))
        self.icon = pyicon(name='discord狀態修改器', title='discord狀態修改器',icon=image, menu=menu)
        self.icon.run()

    def close_all(self):
        print("User Exit")
        self.ctrl_GUI = None
        self.icon.stop()
    
    def iconActivated(self):
        print("tray_menu_click")
        #self.tray.hide()
        self.ctrl_GUI.show()
        self.stop = True
        self.icon.stop()
        Thread(target = self.set_cur_status, daemon = True).start()

    def set_user(self):
        print("set_user")
        try:
            while self.stop:
                try:
                    self.cur_user.setText(file_title)
                    sleep(2)
                except:
                    print("錯誤")
                    break
            else:
                print("detect window destroyed")
                return
        except Exception as e:
            msg_box.warning("錯誤", e)
    
    def set_new_state(self):
        print("set_new_state")
        global RPC_cur_stat
        RPC_cur_stat = "狀態套用中..."
        stat = self.status_entry.text() if len(self.status_entry.text()) else None
        detail = self.detail_entry.text() if len(self.detail_entry.text()) else None
        pic = self.bigPicture_name_Entry.text() if len(self.bigPicture_name_Entry.text()) else None
        pic_text = self.bigPicture_Entry.text() if len(self.bigPicture_Entry.text()) else None
        small_pic_text = self.smallPicture_Entry.text() if len(self.smallPicture_Entry.text()) else None
        small_pic = self.smallPicture_name_Entry.text() if len(self.smallPicture_name_Entry.text()) else None
        buttons = []
        
        if self.button_activate_checkBox_1.isChecked():
            bt1_title = self.button_title_Entry_1.text()
            bt1_url = self.button_url_Entry_1.text()
            if bt1_title == ""  or bt1_url == "":
                msg_box.warning("錯誤", "按鈕一的標題或連結網址不可為空白")
                RPC_cur_stat = "狀態設定失敗"
                return
            buttons.append({"label": f"{bt1_title}", "url": f"{bt1_url}"})
            self.cur_button_1.setText(f"{bt1_title}({bt1_url})")

        if self.button_activate_checkBox_2.isChecked():
            bt2_title = self.button_title_Entry_2.text()
            bt2_url = self.button_url_Entry_2.text()
            if bt2_title == ""  or bt2_url == "":
                msg_box.warning("錯誤", "按鈕二的標題或連結網址不可為空白")
                RPC_cur_stat = "狀態設定失敗"
                return
            buttons.append({"label": f"{self.button_title_Entry_2.text()}", "url": f"{self.button_url_Entry_2.text()}"})
            self.cur_button_2.setText(f"{bt2_title}({bt2_url})")
        if len(buttons) == 0:
            buttons = None
        
        if self.open_time_counting_checkBox.isChecked():
            time_stamp = int(self.time_setting.dateTime().toPyDateTime().timestamp())
            time_set = True
            time_mode = self.time_mode.currentText()
        else:
            time_stamp = None
            time_set = False
            time_mode = None
        print(time_stamp)
        try:
            self.act.set_act(stat=stat,detail=detail,pic=pic,pic_text=pic_text,small_pic=small_pic,
            small_pic_text=small_pic_text,time_set=time_set,time_mode=time_mode,time_stamp=time_stamp,buttons=buttons)
        except Exception as e:
            print("錯誤")
            msg_box.warning("錯誤", e)
        
        self.cur_status.setText(stat)
        self.cur_detail.setText(detail)
        self.cur_BigPicture.setText(f"{pic}({pic_text})")
        self.cur_SmallPicture.setText(f"{small_pic}({small_pic_text})")
        return

    def overwrite_user_state(self):
        global RPC_cur_stat
        print("overwrite user state changes...")
        RPC_cur_stat = "正在覆蓋新的狀態設定檔..."
        sleep(0.5)
        dictionary = {"User_stored_stat":{
                "app_id": self.app_id,
                "detail": self.detail_entry.text(),
                "stat": self.status_entry.text(),
                "pic": self.bigPicture_name_Entry.text(),
                "pic_text": self.bigPicture_Entry.text(),
                "small_pic": self.smallPicture_name_Entry.text(),
                "small_pic_text": self.smallPicture_Entry.text(),
                "time_counting":self.open_time_counting_checkBox.isChecked(),
                "button_1_title":self.button_title_Entry_1.text(),
                "button_1_url":self.button_url_Entry_1.text(),
                "button_1_activate":self.button_activate_checkBox_1.isChecked(),
                "button_2_title":self.button_title_Entry_2.text(),
                "button_2_url":self.button_url_Entry_2.text(),
                "button_2_activate":self.button_activate_checkBox_2.isChecked()
                }}
        json_object = dumps(dictionary, indent = 3)
        with open(f'./data/{file_title}.json', "w", encoding="UTF-8") as json_file:
            json_file.write(json_object)
        json_file.close()
        RPC_cur_stat = "已儲存新的狀態設定檔"
    
    def _init_discord_act(self,file):
        print("_init_discord_act")
        try:
            if len(file) == 0:
                msg_box.warning("錯誤", "App ID不能為空")
                return
            if file in self.dir_list:
                with open(f'./data/{file}.json',encoding="UTF-8",mode="r") as json_file:
                    data = load(json_file)
                    self.app_id = data.get("User_stored_stat",{}).get("app_id","")
                json_file.close()
                self.act = discord_act(self.app_id,title=file)
                self.new_file = True
            else:
                self.app_id = file
                self.act = discord_act(id=self.app_id,title=int(self.app_id))
                self.new_file = False
            self.start()
        except Exception as e:
            print("錯誤")
            msg_box.warning("錯誤", e)

    def start(self):
        print("GUI start")
        self.ctrl_GUI = QMainWindow()
        QFontDatabase.addApplicationFont("./lib/SF-Pro-Display-Regular.otf")
        self.setupUi(self.ctrl_GUI)
        self.ctrl_GUI.show()
        Thread(target = self.set_cur_status, daemon = True).start()
        

    def setupUi(self, ctrl_GUI):
        ctrl_GUI.setObjectName("ctrl_GUI")
        ctrl_GUI.setWindowModality(QtCore.Qt.NonModal)
        ctrl_GUI.resize(1000, 380)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ctrl_GUI.sizePolicy().hasHeightForWidth())
        ctrl_GUI.setSizePolicy(sizePolicy)
        ctrl_GUI.setMinimumSize(QtCore.QSize(1000, 380))
        ctrl_GUI.setMaximumSize(QtCore.QSize(1000, 405))
        ctrl_GUI.setSizeIncrement(QtCore.QSize(1, 1))
        font = QtGui.QFont()
        font.setFamily("SF Pro Display")
        font.setPointSize(9)
        ctrl_GUI.setFont(font)
        ctrl_GUI.setMouseTracking(True)
        ctrl_GUI.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon(".\lib\icon.ico")
        ctrl_GUI.setWindowIcon(icon)
        ctrl_GUI.setAutoFillBackground(True)
        ctrl_GUI.setStyleSheet("")
        ctrl_GUI.setAnimated(True)
        ctrl_GUI.setDocumentMode(False)
        ctrl_GUI.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(ctrl_GUI)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1014, 341))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.main_status_grid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.main_status_grid.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.main_status_grid.setContentsMargins(15, 15, 20, 10)
        self.main_status_grid.setHorizontalSpacing(15)
        self.main_status_grid.setVerticalSpacing(20)
        self.main_status_grid.setObjectName("main_status_grid")
        self.cur_status_title_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.cur_status_title_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.cur_status_title_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_status_title_2.setObjectName("cur_status_title_2")
        self.main_status_grid.addWidget(self.cur_status_title_2, 1, 0, 1, 1)
        self.status_setting_grid = QtWidgets.QGridLayout()
        self.status_setting_grid.setContentsMargins(4, -1, -1, -1)
        self.status_setting_grid.setHorizontalSpacing(10)
        self.status_setting_grid.setVerticalSpacing(8)
        self.status_setting_grid.setObjectName("status_setting_grid")
        self.status_lable = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_lable.sizePolicy().hasHeightForWidth())
        self.status_lable.setSizePolicy(sizePolicy)
        self.status_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.status_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.status_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.status_lable.setObjectName("status_lable")
        self.status_setting_grid.addWidget(self.status_lable, 0, 2, 1, 1)
        self.detail_lable = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detail_lable.sizePolicy().hasHeightForWidth())
        self.detail_lable.setSizePolicy(sizePolicy)
        self.detail_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.detail_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.detail_lable.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setItalic(False)
        font.setStrikeOut(False)
        self.detail_lable.setFont(font)
        self.detail_lable.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.detail_lable.setAutoFillBackground(False)
        self.detail_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.detail_lable.setObjectName("detail_lable")
        self.status_setting_grid.addWidget(self.detail_lable, 0, 0, 1, 1)
        self.detail_entry = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detail_entry.sizePolicy().hasHeightForWidth())
        self.detail_entry.setSizePolicy(sizePolicy)
        self.detail_entry.setMinimumSize(QtCore.QSize(183, 24))
        self.detail_entry.setMaximumSize(QtCore.QSize(183, 24))
        self.detail_entry.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.detail_entry.setFont(font)
        self.detail_entry.setClearButtonEnabled(False)
        self.detail_entry.setObjectName("detail_entry")
        self.status_setting_grid.addWidget(self.detail_entry, 0, 1, 1, 1)
        self.status_entry = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_entry.sizePolicy().hasHeightForWidth())
        self.status_entry.setSizePolicy(sizePolicy)
        self.status_entry.setMinimumSize(QtCore.QSize(183, 24))
        self.status_entry.setMaximumSize(QtCore.QSize(183, 24))
        self.status_entry.setObjectName("status_entry")
        self.status_setting_grid.addWidget(self.status_entry, 0, 3, 1, 1)
        self.main_status_grid.addLayout(self.status_setting_grid, 1, 1, 1, 1)
        self.main_picture_setting_title = QtWidgets.QLabel(self.gridLayoutWidget)
        self.main_picture_setting_title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.main_picture_setting_title.setObjectName("main_picture_setting_title")
        self.main_status_grid.addWidget(self.main_picture_setting_title, 2, 0, 1, 1)
        self.small_picture_setting_title = QtWidgets.QLabel(self.gridLayoutWidget)
        self.small_picture_setting_title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.small_picture_setting_title.setObjectName("small_picture_setting_title")
        self.main_status_grid.addWidget(self.small_picture_setting_title, 3, 0, 1, 1)
        self.cur_user_title_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_user_title_2.sizePolicy().hasHeightForWidth())
        self.cur_user_title_2.setSizePolicy(sizePolicy)
        self.cur_user_title_2.setMaximumSize(QtCore.QSize(90, 24))
        self.cur_user_title_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_user_title_2.setObjectName("cur_user_title_2")
        self.main_status_grid.addWidget(self.cur_user_title_2, 0, 0, 1, 1)
        self.main_picture_setting_grid = QtWidgets.QGridLayout()
        self.main_picture_setting_grid.setContentsMargins(4, 0, -1, -1)
        self.main_picture_setting_grid.setHorizontalSpacing(10)
        self.main_picture_setting_grid.setObjectName("main_picture_setting_grid")
        self.bigPicture_name_lable = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bigPicture_name_lable.sizePolicy().hasHeightForWidth())
        self.bigPicture_name_lable.setSizePolicy(sizePolicy)
        self.bigPicture_name_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.bigPicture_name_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.bigPicture_name_lable.setObjectName("bigPicture_name_lable")
        self.main_picture_setting_grid.addWidget(self.bigPicture_name_lable, 0, 2, 1, 1)
        self.bigPicture_lable = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bigPicture_lable.sizePolicy().hasHeightForWidth())
        self.bigPicture_lable.setSizePolicy(sizePolicy)
        self.bigPicture_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.bigPicture_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.bigPicture_lable.setObjectName("bigPicture_lable")
        self.main_picture_setting_grid.addWidget(self.bigPicture_lable, 0, 0, 1, 1)
        self.bigPicture_Entry = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bigPicture_Entry.sizePolicy().hasHeightForWidth())
        self.bigPicture_Entry.setSizePolicy(sizePolicy)
        self.bigPicture_Entry.setMinimumSize(QtCore.QSize(183, 24))
        self.bigPicture_Entry.setMaximumSize(QtCore.QSize(183, 24))
        self.bigPicture_Entry.setClearButtonEnabled(False)
        self.bigPicture_Entry.setObjectName("bigPicture_Entry")
        self.main_picture_setting_grid.addWidget(self.bigPicture_Entry, 0, 1, 1, 1)
        self.bigPicture_name_Entry = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bigPicture_name_Entry.sizePolicy().hasHeightForWidth())
        self.bigPicture_name_Entry.setSizePolicy(sizePolicy)
        self.bigPicture_name_Entry.setMinimumSize(QtCore.QSize(183, 24))
        self.bigPicture_name_Entry.setMaximumSize(QtCore.QSize(183, 24))
        self.bigPicture_name_Entry.setTabletTracking(True)
        self.bigPicture_name_Entry.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.bigPicture_name_Entry.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.bigPicture_name_Entry.setClearButtonEnabled(False)
        self.bigPicture_name_Entry.setObjectName("bigPicture_name_Entry")
        self.main_picture_setting_grid.addWidget(self.bigPicture_name_Entry, 0, 3, 1, 1)
        self.main_status_grid.addLayout(self.main_picture_setting_grid, 2, 1, 1, 1)
        self.smallPicture_setting_grid = QtWidgets.QGridLayout()
        self.smallPicture_setting_grid.setContentsMargins(4, -1, -1, -1)
        self.smallPicture_setting_grid.setHorizontalSpacing(10)
        self.smallPicture_setting_grid.setObjectName("smallPicture_setting_grid")
        self.smallPicture_name_lable = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallPicture_name_lable.sizePolicy().hasHeightForWidth())
        self.smallPicture_name_lable.setSizePolicy(sizePolicy)
        self.smallPicture_name_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.smallPicture_name_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.smallPicture_name_lable.setObjectName("smallPicture_name_lable")
        self.smallPicture_setting_grid.addWidget(self.smallPicture_name_lable, 0, 2, 1, 1)
        self.smallPicture_lable = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallPicture_lable.sizePolicy().hasHeightForWidth())
        self.smallPicture_lable.setSizePolicy(sizePolicy)
        self.smallPicture_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.smallPicture_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.smallPicture_lable.setObjectName("smallPicture_lable")
        self.smallPicture_setting_grid.addWidget(self.smallPicture_lable, 0, 0, 1, 1)
        self.smallPicture_Entry = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallPicture_Entry.sizePolicy().hasHeightForWidth())
        self.smallPicture_Entry.setSizePolicy(sizePolicy)
        self.smallPicture_Entry.setMinimumSize(QtCore.QSize(183, 24))
        self.smallPicture_Entry.setMaximumSize(QtCore.QSize(183, 24))
        self.smallPicture_Entry.setClearButtonEnabled(False)
        self.smallPicture_Entry.setObjectName("smallPicture_Entry")
        self.smallPicture_setting_grid.addWidget(self.smallPicture_Entry, 0, 1, 1, 1)
        self.smallPicture_name_Entry = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallPicture_name_Entry.sizePolicy().hasHeightForWidth())
        self.smallPicture_name_Entry.setSizePolicy(sizePolicy)
        self.smallPicture_name_Entry.setMinimumSize(QtCore.QSize(183, 24))
        self.smallPicture_name_Entry.setMaximumSize(QtCore.QSize(183, 24))
        self.smallPicture_name_Entry.setStatusTip("")
        self.smallPicture_name_Entry.setWhatsThis("")
        self.smallPicture_name_Entry.setClearButtonEnabled(False)
        self.smallPicture_name_Entry.setObjectName("smallPicture_name_Entry")
        self.smallPicture_setting_grid.addWidget(self.smallPicture_name_Entry, 0, 3, 1, 1)
        self.main_status_grid.addLayout(self.smallPicture_setting_grid, 3, 1, 1, 1)
        self.button_setting_title_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.button_setting_title_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.button_setting_title_1.setObjectName("button_setting_title_1")
        self.main_status_grid.addWidget(self.button_setting_title_1, 4, 0, 1, 1)
        self.button_setting_title_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.button_setting_title_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.button_setting_title_2.setObjectName("button_setting_title_2")
        self.main_status_grid.addWidget(self.button_setting_title_2, 5, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cur_user = QtWidgets.QLabel(self.gridLayoutWidget)
        self.cur_user.setEnabled(True)
        self.cur_user.setMaximumSize(QtCore.QSize(376, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.cur_user.setFont(font)
        self.cur_user.setObjectName("cur_user")
        self.horizontalLayout_5.addWidget(self.cur_user)
        self.reload_file_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reload_file_button.sizePolicy().hasHeightForWidth())
        self.reload_file_button.setSizePolicy(sizePolicy)
        self.reload_file_button.setMaximumSize(QtCore.QSize(80, 30))
        self.reload_file_button.setObjectName("reload_file_button")
        self.horizontalLayout_5.addWidget(self.reload_file_button)
        self.go_to_dev_web_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go_to_dev_web_button.sizePolicy().hasHeightForWidth())
        self.go_to_dev_web_button.setSizePolicy(sizePolicy)
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
        self.horizontalLayout_5.addWidget(self.go_to_dev_web_button)
        self.main_status_grid.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)
        self.button_1_setting_grid_2 = QtWidgets.QGridLayout()
        self.button_1_setting_grid_2.setContentsMargins(4, -1, -1, -1)
        self.button_1_setting_grid_2.setHorizontalSpacing(10)
        self.button_1_setting_grid_2.setObjectName("button_1_setting_grid_2")
        self.button_title_Entry_1 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_title_Entry_1.sizePolicy().hasHeightForWidth())
        self.button_title_Entry_1.setSizePolicy(sizePolicy)
        self.button_title_Entry_1.setMinimumSize(QtCore.QSize(128, 24))
        self.button_title_Entry_1.setMaximumSize(QtCore.QSize(128, 24))
        self.button_title_Entry_1.setClearButtonEnabled(False)
        self.button_title_Entry_1.setObjectName("button_title_Entry_1")
        self.button_1_setting_grid_2.addWidget(self.button_title_Entry_1, 0, 1, 1, 1)
        self.button_url_lable_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_url_lable_1.sizePolicy().hasHeightForWidth())
        self.button_url_lable_1.setSizePolicy(sizePolicy)
        self.button_url_lable_1.setMinimumSize(QtCore.QSize(65, 24))
        self.button_url_lable_1.setMaximumSize(QtCore.QSize(65, 24))
        self.button_url_lable_1.setObjectName("button_url_lable_1")
        self.button_1_setting_grid_2.addWidget(self.button_url_lable_1, 0, 2, 1, 1)
        self.button_title_lable_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_title_lable_1.sizePolicy().hasHeightForWidth())
        self.button_title_lable_1.setSizePolicy(sizePolicy)
        self.button_title_lable_1.setMinimumSize(QtCore.QSize(65, 24))
        self.button_title_lable_1.setMaximumSize(QtCore.QSize(65, 24))
        self.button_title_lable_1.setObjectName("button_title_lable_1")
        self.button_1_setting_grid_2.addWidget(self.button_title_lable_1, 0, 0, 1, 1)
        self.button_activate_checkBox_1 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.button_activate_checkBox_1.setObjectName("button_activate_checkBox_1")
        self.button_1_setting_grid_2.addWidget(self.button_activate_checkBox_1, 0, 4, 1, 1)
        self.button_url_Entry_1 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_url_Entry_1.sizePolicy().hasHeightForWidth())
        self.button_url_Entry_1.setSizePolicy(sizePolicy)
        self.button_url_Entry_1.setMinimumSize(QtCore.QSize(128, 24))
        self.button_url_Entry_1.setMaximumSize(QtCore.QSize(128, 24))
        self.button_url_Entry_1.setStatusTip("")
        self.button_url_Entry_1.setWhatsThis("")
        self.button_url_Entry_1.setClearButtonEnabled(False)
        self.button_url_Entry_1.setObjectName("button_url_Entry_1")
        self.button_1_setting_grid_2.addWidget(self.button_url_Entry_1, 0, 3, 1, 1)
        self.main_status_grid.addLayout(self.button_1_setting_grid_2, 4, 1, 1, 1)
        self.button_2_setting_grid_3 = QtWidgets.QGridLayout()
        self.button_2_setting_grid_3.setContentsMargins(4, -1, -1, -1)
        self.button_2_setting_grid_3.setHorizontalSpacing(10)
        self.button_2_setting_grid_3.setObjectName("button_2_setting_grid_3")
        self.button_title_lable_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_title_lable_2.sizePolicy().hasHeightForWidth())
        self.button_title_lable_2.setSizePolicy(sizePolicy)
        self.button_title_lable_2.setMinimumSize(QtCore.QSize(65, 24))
        self.button_title_lable_2.setMaximumSize(QtCore.QSize(65, 24))
        self.button_title_lable_2.setObjectName("button_title_lable_2")
        self.button_2_setting_grid_3.addWidget(self.button_title_lable_2, 0, 0, 1, 1)
        self.button_title_Entry_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_title_Entry_2.sizePolicy().hasHeightForWidth())
        self.button_title_Entry_2.setSizePolicy(sizePolicy)
        self.button_title_Entry_2.setMinimumSize(QtCore.QSize(128, 24))
        self.button_title_Entry_2.setMaximumSize(QtCore.QSize(128, 24))
        self.button_title_Entry_2.setClearButtonEnabled(False)
        self.button_title_Entry_2.setObjectName("button_title_Entry_2")
        self.button_2_setting_grid_3.addWidget(self.button_title_Entry_2, 0, 1, 1, 1)
        self.button_url_lable_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_url_lable_2.sizePolicy().hasHeightForWidth())
        self.button_url_lable_2.setSizePolicy(sizePolicy)
        self.button_url_lable_2.setMinimumSize(QtCore.QSize(65, 24))
        self.button_url_lable_2.setMaximumSize(QtCore.QSize(65, 24))
        self.button_url_lable_2.setObjectName("button_url_lable_2")
        self.button_2_setting_grid_3.addWidget(self.button_url_lable_2, 0, 2, 1, 1)
        self.button_activate_checkBox_2 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.button_activate_checkBox_2.setObjectName("button_activate_checkBox_2")
        self.button_2_setting_grid_3.addWidget(self.button_activate_checkBox_2, 0, 4, 1, 1)
        self.button_url_Entry_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_url_Entry_2.sizePolicy().hasHeightForWidth())
        self.button_url_Entry_2.setSizePolicy(sizePolicy)
        self.button_url_Entry_2.setMinimumSize(QtCore.QSize(128, 24))
        self.button_url_Entry_2.setMaximumSize(QtCore.QSize(128, 24))
        self.button_url_Entry_2.setStatusTip("")
        self.button_url_Entry_2.setWhatsThis("")
        self.button_url_Entry_2.setClearButtonEnabled(False)
        self.button_url_Entry_2.setObjectName("button_url_Entry_2")
        self.button_2_setting_grid_3.addWidget(self.button_url_Entry_2, 0, 3, 1, 1)
        self.main_status_grid.addLayout(self.button_2_setting_grid_3, 5, 1, 1, 1)
        self.time_setting_title_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.time_setting_title_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time_setting_title_3.setObjectName("time_setting_title_3")
        self.main_status_grid.addWidget(self.time_setting_title_3, 6, 0, 1, 1)
        self.time_setting_grid_2 = QtWidgets.QGridLayout()
        self.time_setting_grid_2.setContentsMargins(0, -1, -1, -1)
        self.time_setting_grid_2.setHorizontalSpacing(10)
        self.time_setting_grid_2.setVerticalSpacing(8)
        self.time_setting_grid_2.setObjectName("time_setting_grid_2")
        self.open_time_counting_checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_time_counting_checkBox.sizePolicy().hasHeightForWidth())
        self.open_time_counting_checkBox.setSizePolicy(sizePolicy)
        self.open_time_counting_checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.open_time_counting_checkBox.setMaximumSize(QtCore.QSize(142, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.open_time_counting_checkBox.setFont(font)
        self.open_time_counting_checkBox.setObjectName("open_time_counting_checkBox")
        self.time_setting_grid_2.addWidget(self.open_time_counting_checkBox, 0, 5, 1, 1)
        self.time_setting = QtWidgets.QDateTimeEdit(self.gridLayoutWidget)
        self.time_setting.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_setting.sizePolicy().hasHeightForWidth())
        self.time_setting.setSizePolicy(sizePolicy)
        self.time_setting.setMinimumSize(QtCore.QSize(218, 24))
        self.time_setting.setMaximumSize(QtCore.QSize(218, 24))
        self.time_setting.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.time_setting.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.time_setting.setCalendarPopup(True)
        self.time_setting.setObjectName("time_setting")
        self.time_setting_grid_2.addWidget(self.time_setting, 0, 3, 1, 1)
        self.time_mode = QtWidgets.QComboBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_mode.sizePolicy().hasHeightForWidth())
        self.time_mode.setSizePolicy(sizePolicy)
        self.time_mode.setMinimumSize(QtCore.QSize(88, 24))
        self.time_mode.setMaximumSize(QtCore.QSize(88, 24))
        self.time_mode.setObjectName("time_mode")
        self.time_mode.addItem("")
        self.time_mode.addItem("")
        self.time_mode.addItem("")
        self.time_setting_grid_2.addWidget(self.time_mode, 0, 0, 1, 1)
        self.time_reset_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_reset_button.sizePolicy().hasHeightForWidth())
        self.time_reset_button.setSizePolicy(sizePolicy)
        self.time_reset_button.setMinimumSize(QtCore.QSize(80, 26))
        self.time_reset_button.setMaximumSize(QtCore.QSize(80, 26))
        self.time_reset_button.setObjectName("time_reset_button")
        self.time_setting_grid_2.addWidget(self.time_reset_button, 0, 4, 1, 1)
        self.main_status_grid.addLayout(self.time_setting_grid_2, 6, 1, 1, 1)
        self.RPC_state_1 = QtWidgets.QHBoxLayout()
        self.RPC_state_1.setObjectName("RPC_state_1")
        self.cur_detail_label = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_detail_label.sizePolicy().hasHeightForWidth())
        self.cur_detail_label.setSizePolicy(sizePolicy)
        self.cur_detail_label.setMinimumSize(QtCore.QSize(55, 24))
        self.cur_detail_label.setMaximumSize(QtCore.QSize(55, 24))
        self.cur_detail_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_detail_label.setObjectName("cur_detail_label")
        self.RPC_state_1.addWidget(self.cur_detail_label)
        self.cur_detail = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_detail.sizePolicy().hasHeightForWidth())
        self.cur_detail.setSizePolicy(sizePolicy)
        self.cur_detail.setMinimumSize(QtCore.QSize(260, 24))
        self.cur_detail.setMaximumSize(QtCore.QSize(260, 24))
        self.cur_detail.setSizeIncrement(QtCore.QSize(0, 0))
        self.cur_detail.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.cur_detail.setObjectName("cur_detail")
        self.RPC_state_1.addWidget(self.cur_detail)
        self.main_status_grid.addLayout(self.RPC_state_1, 1, 2, 1, 1)
        self.cur_status_grid_title = QtWidgets.QLabel(self.gridLayoutWidget)
        self.cur_status_grid_title.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_status_grid_title.sizePolicy().hasHeightForWidth())
        self.cur_status_grid_title.setSizePolicy(sizePolicy)
        self.cur_status_grid_title.setMinimumSize(QtCore.QSize(315, 26))
        self.cur_status_grid_title.setMaximumSize(QtCore.QSize(315, 26))
        self.cur_status_grid_title.setSizeIncrement(QtCore.QSize(170, 17))
        self.cur_status_grid_title.setBaseSize(QtCore.QSize(170, 17))
        self.cur_status_grid_title.setAlignment(QtCore.Qt.AlignCenter)
        self.cur_status_grid_title.setObjectName("cur_status_grid_title")
        self.main_status_grid.addWidget(self.cur_status_grid_title, 0, 2, 1, 1)
        self.RPC_state_2 = QtWidgets.QHBoxLayout()
        self.RPC_state_2.setObjectName("RPC_state_2")
        self.cur_status_label = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_status_label.sizePolicy().hasHeightForWidth())
        self.cur_status_label.setSizePolicy(sizePolicy)
        self.cur_status_label.setMinimumSize(QtCore.QSize(55, 24))
        self.cur_status_label.setMaximumSize(QtCore.QSize(55, 24))
        self.cur_status_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_status_label.setObjectName("cur_status_label")
        self.RPC_state_2.addWidget(self.cur_status_label)
        self.cur_status = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_status.sizePolicy().hasHeightForWidth())
        self.cur_status.setSizePolicy(sizePolicy)
        self.cur_status.setMinimumSize(QtCore.QSize(260, 24))
        self.cur_status.setMaximumSize(QtCore.QSize(260, 24))
        self.cur_status.setObjectName("cur_status")
        self.RPC_state_2.addWidget(self.cur_status)
        self.main_status_grid.addLayout(self.RPC_state_2, 2, 2, 1, 1)
        self.RPC_state_3 = QtWidgets.QHBoxLayout()
        self.RPC_state_3.setObjectName("RPC_state_3")
        self.cur_BigPicture_lable = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_BigPicture_lable.sizePolicy().hasHeightForWidth())
        self.cur_BigPicture_lable.setSizePolicy(sizePolicy)
        self.cur_BigPicture_lable.setMinimumSize(QtCore.QSize(55, 24))
        self.cur_BigPicture_lable.setMaximumSize(QtCore.QSize(55, 24))
        self.cur_BigPicture_lable.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_BigPicture_lable.setObjectName("cur_BigPicture_lable")
        self.RPC_state_3.addWidget(self.cur_BigPicture_lable)
        self.cur_BigPicture = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_BigPicture.sizePolicy().hasHeightForWidth())
        self.cur_BigPicture.setSizePolicy(sizePolicy)
        self.cur_BigPicture.setMinimumSize(QtCore.QSize(260, 24))
        self.cur_BigPicture.setMaximumSize(QtCore.QSize(260, 24))
        self.cur_BigPicture.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.cur_BigPicture.setObjectName("cur_BigPicture")
        self.RPC_state_3.addWidget(self.cur_BigPicture)
        self.main_status_grid.addLayout(self.RPC_state_3, 3, 2, 1, 1)
        self.RPC_state_4 = QtWidgets.QHBoxLayout()
        self.RPC_state_4.setObjectName("RPC_state_4")
        self.cur_SmallPicture_lable = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_SmallPicture_lable.sizePolicy().hasHeightForWidth())
        self.cur_SmallPicture_lable.setSizePolicy(sizePolicy)
        self.cur_SmallPicture_lable.setMinimumSize(QtCore.QSize(55, 24))
        self.cur_SmallPicture_lable.setMaximumSize(QtCore.QSize(55, 24))
        self.cur_SmallPicture_lable.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_SmallPicture_lable.setObjectName("cur_SmallPicture_lable")
        self.RPC_state_4.addWidget(self.cur_SmallPicture_lable)
        self.cur_SmallPicture = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_SmallPicture.sizePolicy().hasHeightForWidth())
        self.cur_SmallPicture.setSizePolicy(sizePolicy)
        self.cur_SmallPicture.setMinimumSize(QtCore.QSize(260, 24))
        self.cur_SmallPicture.setMaximumSize(QtCore.QSize(260, 24))
        self.cur_SmallPicture.setSizeIncrement(QtCore.QSize(0, 0))
        self.cur_SmallPicture.setBaseSize(QtCore.QSize(0, 0))
        self.cur_SmallPicture.setObjectName("cur_SmallPicture")
        self.RPC_state_4.addWidget(self.cur_SmallPicture)
        self.main_status_grid.addLayout(self.RPC_state_4, 4, 2, 1, 1)
        self.RPC_state_5 = QtWidgets.QHBoxLayout()
        self.RPC_state_5.setObjectName("RPC_state_5")
        self.cur_button_lable_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_button_lable_1.sizePolicy().hasHeightForWidth())
        self.cur_button_lable_1.setSizePolicy(sizePolicy)
        self.cur_button_lable_1.setMinimumSize(QtCore.QSize(55, 24))
        self.cur_button_lable_1.setMaximumSize(QtCore.QSize(55, 24))
        self.cur_button_lable_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_button_lable_1.setObjectName("cur_button_lable_1")
        self.RPC_state_5.addWidget(self.cur_button_lable_1)
        self.cur_button_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_button_1.sizePolicy().hasHeightForWidth())
        self.cur_button_1.setSizePolicy(sizePolicy)
        self.cur_button_1.setMinimumSize(QtCore.QSize(260, 24))
        self.cur_button_1.setMaximumSize(QtCore.QSize(260, 24))
        self.cur_button_1.setSizeIncrement(QtCore.QSize(0, 0))
        self.cur_button_1.setBaseSize(QtCore.QSize(0, 0))
        self.cur_button_1.setObjectName("cur_button_1")
        self.RPC_state_5.addWidget(self.cur_button_1)
        self.main_status_grid.addLayout(self.RPC_state_5, 5, 2, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.cur_button_lable_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_button_lable_2.sizePolicy().hasHeightForWidth())
        self.cur_button_lable_2.setSizePolicy(sizePolicy)
        self.cur_button_lable_2.setMinimumSize(QtCore.QSize(55, 24))
        self.cur_button_lable_2.setMaximumSize(QtCore.QSize(55, 24))
        self.cur_button_lable_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_button_lable_2.setObjectName("cur_button_lable_2")
        self.horizontalLayout_8.addWidget(self.cur_button_lable_2)
        self.cur_button_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_button_2.sizePolicy().hasHeightForWidth())
        self.cur_button_2.setSizePolicy(sizePolicy)
        self.cur_button_2.setMinimumSize(QtCore.QSize(260, 24))
        self.cur_button_2.setMaximumSize(QtCore.QSize(260, 24))
        self.cur_button_2.setSizeIncrement(QtCore.QSize(0, 0))
        self.cur_button_2.setBaseSize(QtCore.QSize(0, 0))
        self.cur_button_2.setObjectName("cur_button_2")
        self.horizontalLayout_8.addWidget(self.cur_button_2)
        self.main_status_grid.addLayout(self.horizontalLayout_8, 6, 2, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 340, 1001, 44))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.activate_button_grid = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.activate_button_grid.setContentsMargins(15, 0, 15, 15)
        self.activate_button_grid.setObjectName("activate_button_grid")
        self.save_data_button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.save_data_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.save_data_button.setDefault(False)
        self.save_data_button.setObjectName("save_data_button")
        self.activate_button_grid.addWidget(self.save_data_button, 0, 2, 1, 1)
        self.close_window_button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.close_window_button.setObjectName("close_window_button")
        self.activate_button_grid.addWidget(self.close_window_button, 0, 5, 1, 1)
        self.save_data_button_2 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.save_data_button_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.save_data_button_2.setDefault(False)
        self.save_data_button_2.setObjectName("save_data_button_2")
        self.activate_button_grid.addWidget(self.save_data_button_2, 0, 0, 1, 1)
        self.activate_status_button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.activate_status_button.setMinimumSize(QtCore.QSize(335, 0))
        self.activate_status_button.setMaximumSize(QtCore.QSize(335, 16777215))
        self.activate_status_button.setObjectName("activate_status_button")
        self.activate_button_grid.addWidget(self.activate_status_button, 0, 3, 1, 1)
        ctrl_GUI.setCentralWidget(self.centralwidget)
        self.white_mode = QtWidgets.QAction(ctrl_GUI)
        self.white_mode.setCheckable(True)
        self.white_mode.setObjectName("white_mode")
        self.dark_mode = QtWidgets.QAction(ctrl_GUI)
        self.dark_mode.setCheckable(True)
        self.dark_mode.setObjectName("dark_mode")
        self.hide_RPC_status = QtWidgets.QAction(ctrl_GUI)
        self.hide_RPC_status.setCheckable(True)
        self.hide_RPC_status.setObjectName("hide_RPC_status")

        self.retranslateUi(ctrl_GUI)
        ctrl_GUI.destroyed.connect(ctrl_GUI.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ctrl_GUI)
    
    def retranslateUi(self, ctrl_GUI):
        _translate = QtCore.QCoreApplication.translate
        ctrl_GUI.setWindowTitle(_translate("ctrl_GUI", "discord狀態修改器"))
        self.status_lable.setText(_translate("ctrl_GUI", "副標"))
        self.detail_lable.setText(_translate("ctrl_GUI", "主標"))
        self.detail_entry.setPlaceholderText(_translate("ctrl_GUI", "請輸入狀態標題"))
        self.status_entry.setPlaceholderText(_translate("ctrl_GUI", "請輸入狀態副標標題"))
        self.main_picture_setting_title.setText(_translate("ctrl_GUI", "主圖片設定"))
        self.small_picture_setting_title.setText(_translate("ctrl_GUI", "小圖片設定"))
        self.cur_status_title_2.setText(_translate("ctrl_GUI", "欲設定的狀態"))
        self.cur_user_title_2.setText(_translate("ctrl_GUI", "目前設定檔"))
        self.bigPicture_name_lable.setText(_translate("ctrl_GUI", "圖片名稱"))
        self.bigPicture_lable.setText(_translate("ctrl_GUI", "圖片標題"))
        self.bigPicture_Entry.setPlaceholderText(_translate("ctrl_GUI", "請輸入圖片標題"))
        self.bigPicture_name_Entry.setPlaceholderText(_translate("ctrl_GUI", "請輸入圖片名稱"))
        self.smallPicture_name_lable.setText(_translate("ctrl_GUI", "小圖名稱"))
        self.smallPicture_lable.setText(_translate("ctrl_GUI", "小圖標題"))
        self.smallPicture_Entry.setPlaceholderText(_translate("ctrl_GUI", "請輸入小圖標題"))
        self.smallPicture_name_Entry.setPlaceholderText(_translate("ctrl_GUI", "請輸入小圖名稱"))
        self.go_to_dev_web_button.setText(_translate("ctrl_GUI", "點我前往Dc Dev網站"))
        self.button_setting_title_1.setText(_translate("ctrl_GUI", "按鈕一設定"))
        self.button_setting_title_2.setText(_translate("ctrl_GUI", "按鈕二設定"))
        self.button_url_lable_1.setText(_translate("ctrl_GUI", "按鈕連結"))
        self.button_title_Entry_1.setPlaceholderText(_translate("ctrl_GUI", "請輸入按鈕名稱"))
        self.button_title_lable_1.setText(_translate("ctrl_GUI", "按鈕名稱"))
        self.button_url_Entry_1.setPlaceholderText(_translate("ctrl_GUI", "請輸入按鈕連結網址"))
        self.button_activate_checkBox_1.setText(_translate("ctrl_GUI", "開啟按鈕一"))
        self.button_url_lable_2.setText(_translate("ctrl_GUI", "按鈕連結"))
        self.button_title_lable_2.setText(_translate("ctrl_GUI", "按鈕名稱"))
        self.button_title_Entry_2.setPlaceholderText(_translate("ctrl_GUI", "請輸入按鈕名稱"))
        self.button_url_Entry_2.setPlaceholderText(_translate("ctrl_GUI", "請輸入按鈕連結網址"))
        self.button_activate_checkBox_2.setText(_translate("ctrl_GUI", "開啟按鈕二"))
        self.activate_status_button.setText(_translate("ctrl_GUI", "啟動狀態"))
        self.save_data_button.setText(_translate("ctrl_GUI", "儲存資料"))
        self.save_data_button_2.setText(_translate("ctrl_GUI", "另存新檔"))
        self.cur_status_grid_title.setText(_translate("ctrl_GUI", "目前狀態:狀態未啟動"))
        self.close_window_button.setText(_translate("ctrl_GUI", "最小化視窗"))
        self.cur_BigPicture_lable.setText(_translate("ctrl_GUI", "大圖:"))
        self.cur_detail_label.setText(_translate("ctrl_GUI", "主標:"))
        self.cur_status_label.setText(_translate("ctrl_GUI", "副標:"))
        self.cur_button_lable_1.setText(_translate("ctrl_GUI", "按鈕一:"))
        self.cur_button_lable_2.setText(_translate("ctrl_GUI", "按鈕二:"))
        self.cur_SmallPicture_lable.setText(_translate("ctrl_GUI", "小圖:"))
        self.time_setting_title_3.setText(_translate("ctrl_GUI", "時間設定"))
        self.time_reset_button.setText(_translate("ctrl_GUI", "重設時間"))
        self.time_setting.setDisplayFormat(_translate("ctrl_GUI", "yyyy年M月d日 AP hh:mm:ss"))
        self.time_setting.setDateTime(QtCore.QDateTime.currentDateTime())
        self.open_time_counting_checkBox.setText(_translate("ctrl_GUI", "開啟時間計數"))
        self.time_mode.setCurrentText(_translate("ctrl_GUI", "從零開始"))
        self.time_mode.setItemText(0, _translate("ctrl_GUI", "從零開始"))
        self.time_mode.setItemText(1, _translate("ctrl_GUI", "經過時間"))
        self.time_mode.setItemText(2, _translate("ctrl_GUI", "剩餘時間"))
        self.reload_file_button.setText(_translate("ctrl_GUI", "更換存檔"))
        
        status = self.act.stat
        detail = self.act.detail
        bigPicture = self.act.pic_text
        bigPicture_name = self.act.pic
        smallPicture = self.act.small_pic_text
        smallPicture_name = self.act.small_pic
        button_1_title = self.act.button_1_title
        button_1_url = self.act.button_1_url
        button_2_title = self.act.button_2_title
        button_2_url = self.act.button_2_url

        self.status_entry.setText(_translate("ctrl_GUI",status))
        self.detail_entry.setText(_translate("ctrl_GUI",detail))
        self.bigPicture_Entry.setText(_translate("ctrl_GUI",bigPicture))
        self.bigPicture_name_Entry.setText(_translate("ctrl_GUI",bigPicture_name))
        self.smallPicture_Entry.setText(_translate("ctrl_GUI",smallPicture))
        self.smallPicture_name_Entry.setText(_translate("ctrl_GUI",smallPicture_name))
        self.button_title_Entry_1.setText(_translate("ctrl_GUI",button_1_title))
        self.button_url_Entry_1.setText(_translate("ctrl_GUI",button_1_url))
        self.button_title_Entry_2.setText(_translate("ctrl_GUI",button_2_title))
        self.button_url_Entry_2.setText(_translate("ctrl_GUI",button_2_url))

        self.cur_status.setText(_translate("ctrl_GUI", status))
        self.cur_detail.setText(_translate("ctrl_GUI", detail))
        self.cur_BigPicture.setText(_translate("ctrl_GUI",f"{bigPicture_name}({bigPicture})"))
        self.cur_SmallPicture.setText(_translate("ctrl_GUI",f"{smallPicture_name}({smallPicture})"))
        self.cur_button_1.setText(_translate("ctrl_GUI", f"{button_1_title}({button_1_url})"))
        self.cur_button_2.setText(_translate("ctrl_GUI", f"{button_2_title}({button_2_url})"))
        self.cur_user.setText(_translate("ctrl_GUI", file_title))
        self.open_time_counting_checkBox.setChecked(self.act.time_count)

        if self.act.button_1_activate:
            self.button_activate_checkBox_1.setChecked(True)
            self.button_title_Entry_1.setEnabled(True)
            self.button_url_Entry_1.setEnabled(True)
        else:
            self.button_activate_checkBox_1.setChecked(False)
            self.button_title_Entry_1.setEnabled(False)
            self.button_url_Entry_1.setEnabled(False)
        
        if self.act.button_2_activate:
            self.button_activate_checkBox_2.setChecked(True)
            self.button_title_Entry_2.setEnabled(True)
            self.button_url_Entry_2.setEnabled(True)
        else:
            self.button_activate_checkBox_2.setChecked(False)
            self.button_title_Entry_2.setEnabled(False)
            self.button_url_Entry_2.setEnabled(False)
        self.save_data_button.setEnabled(self.new_file)

        if self.act.time_count:
            self.time_mode.setEnabled(True)
            if self.time_mode.currentText() != "從零開始":
                self.time_setting.setEnabled(True)
                self.time_reset_button.setEnabled(True)
            else:
                self.time_setting.setEnabled(False)
                self.time_reset_button.setEnabled(False)
        else:
            self.time_mode.setEnabled(False)
            self.time_setting.setEnabled(False)
            self.time_reset_button.setEnabled(False)

        self.add_button_connect(ctrl_GUI)       
    
    def add_button_connect(self,ctrl_GUI):
        self.save_data_button_2.clicked.connect(self.open_save_window)
        self.save_data_button.clicked.connect(self.overwrite_user_state)
        self.activate_status_button.clicked.connect(self.set_new_state)
        self.close_window_button.clicked.connect(self.show_system_tray)
        self.go_to_dev_web_button.clicked.connect(self.open_discord_dev)
        ctrl_GUI.destroyed.connect(self.close)
        self.time_mode.currentTextChanged.connect(self.on_Timemode_changed)
        self.time_reset_button.clicked.connect(self.reset_QDateTime)
        self.button_activate_checkBox_1.stateChanged.connect(self.button_activate_checkBox_1_changed)
        self.button_activate_checkBox_2.stateChanged.connect(self.button_activate_checkBox_2_changed)
        self.open_time_counting_checkBox.stateChanged.connect(self.time_activate_checkBox_changed)
        self.reload_file_button.clicked.connect(self.main_window_reload)

    def close(self):
        self.stop = False
        print("window closed")

    def main_window_reload(self):
        self.reload = Ui_restart_ui()

    def open_save_window(self):
        dictionary = {"User_stored_stat":{
                "app_id": self.app_id,
                "detail": self.detail_entry.text(),
                "stat": self.status_entry.text(),
                "pic": self.bigPicture_name_Entry.text(),
                "pic_text": self.bigPicture_Entry.text(),
                "small_pic": self.smallPicture_name_Entry.text(),
                "small_pic_text": self.smallPicture_Entry.text(),
                "time_counting":self.open_time_counting_checkBox.isChecked(),
                "button_1_title":self.button_title_Entry_1.text(),
                "button_1_url":self.button_url_Entry_1.text(),
                "button_1_activate":self.button_activate_checkBox_1.isChecked(),
                "button_2_title":self.button_title_Entry_2.text(),
                "button_2_url":self.button_url_Entry_2.text(),
                "button_2_activate":self.button_activate_checkBox_2.isChecked()
                }}
        if self.save_window is None:
            self.save_window = Ui_Save_As()
            self.save_window.show_window(dictionary)
        else:
            self.save_window.show_window(dictionary)
        self.save_data_button.setEnabled(True)
        self.cur_user.setText(file_title)

    def open_discord_dev(self):
        url=f"https://discord.com/developers/applications/{self.app_id}/rich-presence/assets"
        open_new(url)
        
    def set_cur_status(self):
        global RPC_cur_stat
        while self.stop:
            self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:{RPC_cur_stat}"))
            self.cur_user.setText(app.translate("ctrl_GUI", file_title))
            sleep(0.1)
        else:
            return

    def button_activate_checkBox_1_changed(self):
        if self.button_activate_checkBox_1.isChecked():
            self.button_title_Entry_1.setEnabled(True)
            self.button_url_Entry_1.setEnabled(True)
        else:
            self.button_title_Entry_1.setEnabled(False)
            self.button_url_Entry_1.setEnabled(False)

    def button_activate_checkBox_2_changed(self):
        if self.button_activate_checkBox_2.isChecked():
            self.button_title_Entry_2.setEnabled(True)
            self.button_url_Entry_2.setEnabled(True)
        else:
            self.button_title_Entry_2.setEnabled(False)
            self.button_url_Entry_2.setEnabled(False)
    
    def on_Timemode_changed(self, value):
        if self.open_time_counting_checkBox.isChecked():
            if value == "從零開始":
                self.time_setting.setEnabled(False)
                self.time_reset_button.setEnabled(False)
            else:
                self.time_setting.setEnabled(True)
                self.time_reset_button.setEnabled(True)

    def time_activate_checkBox_changed(self):
        if self.open_time_counting_checkBox.isChecked():
            self.time_mode.setEnabled(True)
            if self.time_mode.currentText() != "從零開始":
                self.time_reset_button.setEnabled(True)
                self.time_setting.setEnabled(True)
            else:
                self.time_setting.setEnabled(False)
                self.time_reset_button.setEnabled(False)
        else:
            self.time_mode.setEnabled(False)
            self.time_setting.setEnabled(False)
            self.time_reset_button.setEnabled(False)
    
    def reset_QDateTime(self):
        self.time_setting.setDateTime(QtCore.QDateTime.currentDateTime())

class UI_start_ui:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        app.setStyleSheet(qdarktheme.load_stylesheet())
        self.start_ui = QtWidgets.QWidget()
        self.setupUi(self.start_ui)
        self.start_ui.setWindowIcon(icon)
        self.get_file_name()
        self.start_ui.show()
        sys.exit(app.exec_())

    def close(self):
        print("start_ui closed")
        exit()

    def get_file_name(self):
        print("start get_file_name")
        self.dir_raw_list = listdir("./data")
        self.dir_list = []
        for i in self.dir_raw_list:
            self.dir_list.append(i.split(".")[0])
        self.comboBox.addItems(self.dir_list)

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
        self.go_to_dev_web_button.clicked.connect(self.open_discord_dev)
        self.Enter.clicked.connect(self._init_main_ui)
        QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self.comboBox, activated=self._init_main_ui)

    def open_discord_dev(self):
        open_new("https://discord.com/developers/applications/")

    def _init_main_ui(self):
        global file_title
        file_title = self.comboBox.currentText()
        ctrl_GUI(self.dir_list)
        self.start_ui = None

class Ui_Save_As:
    def __init__(self):
        super().__init__()
        self.Save_As = QWidget()
        self.Save_As.setWindowIcon(icon)
        self.setupUi(self.Save_As)

    def setupUi(self, Save_As):
        Save_As.setObjectName("Save_As")
        Save_As.setEnabled(True)
        Save_As.resize(400, 50)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Save_As.sizePolicy().hasHeightForWidth())
        Save_As.setSizePolicy(sizePolicy)
        Save_As.setMinimumSize(QtCore.QSize(0, 50))
        Save_As.setMaximumSize(QtCore.QSize(16777215, 50))
        self.horizontalLayoutWidget = QtWidgets.QWidget(Save_As)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(15, 0, 15, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QtCore.QSize(201, 24))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 28))
        self.pushButton.setMaximumSize(QtCore.QSize(55, 28))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(Save_As)
        QtCore.QMetaObject.connectSlotsByName(Save_As)

    def retranslateUi(self, Save_As):
        _translate = QtCore.QCoreApplication.translate
        Save_As.setWindowTitle(_translate("Save_As", "存檔設定"))
        self.label.setText(_translate("Save_As", "請輸入存檔標題:"))
        self.pushButton.setText(_translate("Save_As", "確定"))
        self.pushButton.clicked.connect(self.save_user_state)
        QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self.lineEdit, activated=self.save_user_state)

    def show_window(self,dictionary):
        self.dictionary = dictionary
        self.Save_As.show()

    def save_user_state(self):
        print("saving state changes...")
        if len(self.lineEdit.text()) == 0:
            msg_box.warning("錯誤", "檔名不能為空")
            return
        else:
            json_object = dumps(self.dictionary, indent = 3)
            save_title = self.lineEdit.text()
            print(save_title)
            with open(f'./data/{save_title}.json', "w", encoding="UTF-8") as json_file:
                json_file.write(json_object)
            json_file.close()
            self.Save_As.destroy()
            global file_title
            file_title = self.lineEdit.text()
            msg_box.information("discord狀態修改器", "儲存成功")
            

class Ui_restart_ui(object):
    def __init__(self):
        self.restart_ui = QtWidgets.QDialog()
        self.setupUi(self.restart_ui)
        self.restart_ui.setWindowIcon(icon)
        self.restart_ui.show()
       
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
        restart_ui.setWindowTitle(_translate("restart_ui", "Dialog"))
        self.label.setText(_translate("restart_ui", "確定要更換存檔嗎?"))
        self.No_button.setText(_translate("restart_ui", "否"))
        self.yes_button.setText(_translate("restart_ui", "是的!"))
        restart_ui.setWindowTitle(_translate("restart_ui", "更換確認"))
        self.yes_button.clicked.connect(self.reload)
        self.No_button.clicked.connect(self.close_window)

    def reload(self):
        execlp(sys.executable, sys.executable, *sys.argv)
        
    def close_window(self):
        self.restart_ui.destroy()

class msg_window(QWidget):
    def information(self,title:str,message):
        message = str(message)
        QMessageBox.information(self,title,message)

    def warning(self,title:str,message):
        print("錯誤")
        message = str(message)
        QMessageBox.warning(self,title,message)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    icon = QtGui.QIcon("./lib/icon.ico")
    msg_box = msg_window()
    msg_box.setWindowIcon(icon)
    print(sys.executable)
    print(path.abspath(__file__))
    UI_start_ui()