from os import execlp,listdir,path
from pypresence import Presence
from threading import Thread
from json import load,dumps,loads
from PyQt5 import QtCore, QtGui, QtWidgets,QtTest
from PyQt5.QtCore import QUrl,QThread
from PyQt5.QtGui import QFontDatabase,QTextCursor,QDesktopServices
from PyQt5.QtWidgets import QMessageBox,QWidget, QApplication, QShortcut, QMainWindow,QSystemTrayIcon
import qdarktheme
import sys
import requests

file_title = ""
version = "discord狀態修改器 v1.1 beta公開測試版"

class ctrl_GUI:
    def __init__(self,dir_list):
        log.info("start discord game state")
        self.dir_list = dir_list
        self.test = False
        self.stop = True
        self.save_window = None
        if len(file_title) == 0:
            msg_box.warning("錯誤", "App ID不能為空")
            return
            
        try:
            if file_title in self.dir_list:
                with open(f'.\data\{file_title}.json',encoding="UTF-8",mode="r") as json_file:
                    data = load(json_file)
                    self.app_id = data.get("User_stored_stat",{}).get("app_id","")
                json_file.close()
                self.act = self.start_discord_act(self.app_id,title=file_title)
                self.new_file = True
            else:
                self.app_id = file_title
                self.act = self.start_discord_act(id=self.app_id,title=int(self.app_id))
                self.new_file = False
        except:
            raise Exception("檔案內容為不支援的資料形式\n請重新選擇或重新建立存檔")
        
        self.ctrl_GUI = QMainWindow()
        self.setupUi(self.ctrl_GUI)
        self.add_picture()
        self.statusMessage.setText("尚未啟動狀態")
        self.ctrl_GUI.show()
        self.init_script_setting_window()
        self._init_system_tray()
        Thread(target=self.thread_checker,daemon=True).start()
        return

    def thread_checker(self):
        while True:
            sleep(1000)
            if not self.istray:
                window = 0
                for tl in QtWidgets.QApplication.topLevelWidgets():
                    if not tl.isHidden():
                        window += 1
                if window == 0:
                    self.script_stat_activate = False
                    app.quit()
                    self.app.close()
                    return

    def start_discord_act(self,id,title):
        try:
            log.info("start init discord_act")
            self.cur_start = True
            self.app = Presence(id)
            self.app.connect()
            self.get_stored_data(id, title)
            self.stop = False
            self.cur_start = False
            self.istray = False
        except Exception as e:
            err_code = ['result','存取被拒','Could not find Discord installed and running on this machine.']
            for i in err_code:
                if i in str(e):
                    raise Exception(f"Discord似乎未正確啟動\n您可以嘗試以下方法進行問題排解\n\n1.請確保已啟動Discord\n2.若Discord已開啟，請重新啟動修改器\n3.若Discord是以管理員權限運行，請以正常權限啟動Discord，或是以管理員模式啟動修改器\n\n若問題持續發生\n請直接截圖並私訊作者 Evanlau#0857 回報問題\n\n錯誤碼:{e}")
            raise Exception(e)
    
    def get_stored_data(self,id,title):
        log.info("get_stored_data")
        with open(f'./data/{title}.json',encoding="UTF-8",mode="r") as json_file:
            data = load(json_file)
            self.is_script = data.get("User_stored_stat",{}).get("is_script",False)
            self.detail = data.get("User_stored_stat",{}).get("detail","")
            self.stat = data.get("User_stored_stat",{}).get("stat","")
            self.pic = data.get("User_stored_stat",{}).get("pic","")
            self.pic_text = data.get("User_stored_stat",{}).get("pic_text","")
            self.small_pic = data.get("User_stored_stat",{}).get("small_pic","")
            self.small_pic_text = data.get("User_stored_stat",{}).get("small_pic_text","")
            self.time_count = data.get("User_stored_stat",{}).get("time_counting",True)
            self.button_1_title = data.get("User_stored_stat",{}).get("button_1_title","")
            self.button_1_url = data.get("User_stored_stat",{}).get("button_1_url","")
            self.button_1_activate = data.get("User_stored_stat",{}).get("button_1_activate",False)
            self.button_2_title = data.get("User_stored_stat",{}).get("button_2_title","")
            self.button_2_url = data.get("User_stored_stat",{}).get("button_2_url","")
            self.button_2_activate = data.get("User_stored_stat",{}).get("button_2_activate",False)

            self.scripted_detail:list = data.get("Scripted_stored_data",{}).get("detail",[])
            self.scripted_stat:list = data.get("Scripted_stored_data",{}).get("stat",[])
            self.scripted_pic:list = data.get("Scripted_stored_data",{}).get("pic",[])
            self.scripted_pic_text:list = data.get("Scripted_stored_data",{}).get("pic_text",[])
            self.scripted_small_pic:list = data.get("Scripted_stored_data",{}).get("small_pic",[])
            self.scripted_small_pic_text:list = data.get("Scripted_stored_data",{}).get("small_pic_text",[])
            self.scripted_button_1_title:list = data.get("Scripted_stored_data",{}).get("button_1_title",[])
            self.scripted_button_1_url:list = data.get("Scripted_stored_data",{}).get("button_1_url",[])
            self.scripted_button_2_title:list = data.get("Scripted_stored_data",{}).get("button_2_title",[])
            self.scripted_button_2_url:list = data.get("Scripted_stored_data",{}).get("button_2_url",[])
            self.scripted_time = data.get("Scripted_stored_data",{}).get("time_counting",1)
        json_file.close()
        log.info(f"File Read:{title}")
        return

    def set_act(self,stat,detail,pic,pic_text,small_pic,small_pic_text,time_set,time_mode,time_stamp,buttons):
        log.info("set_act")
        instance = True
        cur_time = int(QtCore.QDateTime.currentDateTime().toPyDateTime().timestamp())
        try:
            if time_set == False:
                self.app.update(state=stat,details=detail,large_image=pic,large_text=pic_text,small_image=small_pic,small_text=small_pic_text,instance=instance,buttons=buttons)
            else:
                if time_mode == "從零開始":
                    start_time_stamp = cur_time
                    end_time_stamp = None
                elif time_mode == "經過時間":
                    if time_stamp > cur_time:
                        msg_box.warning("錯誤", "經過時間為負數")
                        self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:狀態設定失敗"))
                        return
                    start_time_stamp = time_stamp
                    end_time_stamp = None
                elif time_mode == "剩餘時間":
                    if time_stamp < cur_time:
                        msg_box.warning("錯誤", "剩餘時間為負數")
                        self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:狀態設定失敗"))
                        return
                    start_time_stamp = None
                    end_time_stamp = time_stamp
                self.app.update(state=stat,details=detail,large_image=pic,large_text=pic_text,small_image=small_pic,small_text=small_pic_text,instance=instance,start=start_time_stamp,end=end_time_stamp,buttons=buttons)
            self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:狀態設定成功"))
        except Exception as e:
            self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:狀態設定失敗"))
            if 'must be a valid uri' in str(e):
                msg_box.warning('錯誤', '您輸入的網址不是正確的網址\n網址須加上http://或https://')
            else:
                msg_box.warning('錯誤', e)

    def _init_system_tray(self):
        log.info("system_tray")
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setToolTip("Discord狀態修改器")
        self.tray.activated.connect(self.iconActivated)
        self.tray.setVisible(True)
        self.tray.hide()

    def close_all(self):
        log.info("User Exit")
        self.ctrl_GUI = None
    
    def iconActivated(self):
        log.info("tray_menu_click")
        self.tray.hide()
        self.ctrl_GUI.show()
        self.istray = False
        app.setQuitOnLastWindowClosed(True)

    def window_minimum(self):
        log.info("window_minimum")
        self.tray.show()
        self.ctrl_GUI.hide()
        self.istray = True
        app.setQuitOnLastWindowClosed(False)
    
    def set_new_script_state(self):
        log.info("set_new_script_state")
        self.script_stat_activate = False

        time_stamp = int(self.time_setting.dateTime().toPyDateTime().timestamp())
        time_mode = self.time_mode.currentText()
        start_time = int(QtCore.QDateTime.currentDateTime().toPyDateTime().timestamp())
        button_1_isChecked = self.button_activate_checkBox_1.isChecked()
        button_2_isChecked = self.button_activate_checkBox_2.isChecked()
        if self.open_time_counting_checkBox.isChecked():
            if time_mode == "從零開始":
                start_time_stamp = start_time
                end_time_stamp = None
            elif time_mode == "經過時間":
                if time_stamp > start_time:
                    msg_box.warning("錯誤", "經過時間為負數")
                    self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:狀態設定失敗"))
                    self.statusMessage.setText("腳本模式(已停止狀態顯示)")
                    self.activate_status_button.setEnabled(True)
                    self.app.clear()
                    return
                start_time_stamp = time_stamp
                end_time_stamp = None
            elif time_mode == "剩餘時間":
                if time_stamp < start_time:
                    msg_box.warning("錯誤", "剩餘時間為負數")
                    self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:狀態設定失敗"))
                    self.statusMessage.setText("腳本模式(已停止狀態顯示)")
                    self.activate_status_button.setEnabled(True)
                    self.app.clear()
                    return
                start_time_stamp = None
                end_time_stamp = time_stamp
        else:
            start_time_stamp = None
            end_time_stamp = None

        if button_1_isChecked:
            if len(self.scripted_button_1_title) == 0:
                msg_box.warning("腳本錯誤","按鈕一標題的腳本沒有資料\n若不須開啟按鈕一\n請不要勾選「開啟按鈕一」")
                self.statusMessage.setText("腳本模式(已停止狀態顯示)")
                self.activate_status_button.setEnabled(True)
                self.app.clear()
                return
            else:
                scripted_button_1_title = self.scripted_button_1_title
            if len(self.scripted_button_1_url) == 0:
                msg_box.warning("腳本錯誤","按鈕一連結的腳本沒有資料\n若不須開啟按鈕一\n請不要勾選「開啟按鈕一」")
                self.statusMessage.setText("腳本模式(已停止狀態顯示)")
                self.activate_status_button.setEnabled(True)
                self.app.clear()
                return
            else:
                scripted_button_1_url = self.scripted_button_1_url
            button_1 = self.button_1_cycle(scripted_button_1_title,scripted_button_1_url)
        else:
            button_1 = None
            scripted_button_1_title = None
            scripted_button_1_url = None
            #button_1_list_pos = None

        QtTest.QTest.qWait(10)
        if button_2_isChecked:
            if len(self.scripted_button_2_title) == 0:
                msg_box.warning("腳本錯誤","按鈕二標題的腳本沒有資料\n若不須開啟按鈕二\n請不要勾選「開啟按鈕二」")
                self.statusBar.showMessage("腳本模式(已停止狀態顯示)")
                self.activate_status_button.setEnabled(True)
                self.app.clear()
                return
            else:
                scripted_button_2_title = self.scripted_button_2_title
            if len(self.scripted_button_2_url) == 0:
                msg_box.warning("腳本錯誤","按鈕二連結的腳本沒有資料\n若不須開啟按鈕二\n請不要勾選「開啟按鈕二」")
                self.statusBar.showMessage("腳本模式(已停止狀態顯示)")
                self.activate_status_button.setEnabled(True)
                self.app.clear()
                return
            else:
                scripted_button_2_url = self.scripted_button_2_url
            button_2 = self.button_2_cycle(scripted_button_2_title,scripted_button_2_url)
        else:
            button_2 = None
            scripted_button_2_title = None
            scripted_button_2_url = None
            #button_2_list_pos = None
        
        try:
            while self.set_script_state_thread.is_alive():
                self.cur_status_grid_title.setText("目前狀態:正在等待目前狀態結束...")
                self.set_script_state_thread.join()
        except:pass
        self.set_script_state_thread = Thread(target = self.set_new_script_state_thread,
            args=[button_1,button_2,
                scripted_button_1_title,scripted_button_1_url,
                scripted_button_2_title,scripted_button_2_url,
                start_time_stamp,end_time_stamp,start_time] ,
            daemon = True)
        self.script_stat_activate = True
        self.cur_status_grid_title.setText("目前狀態:腳本狀態設定成功")
        self.set_script_state_thread.start()
        QtTest.QTest.qWait(10)
        self.activate_status_button.setEnabled(True)
        return

    def set_new_script_state_thread(self,button_1,button_2,
            scripted_button_1_title,scripted_button_1_url,
            scripted_button_2_title,scripted_button_2_url,
            start_time_stamp,end_time_stamp,start_time):
        change_time = self.scripted_time
        button_1_isChecked = self.button_activate_checkBox_1.isChecked()
        button_2_isChecked = self.button_activate_checkBox_2.isChecked()
        if len(self.scripted_stat) != 0:
            cycle_stat = self.cycle(self.scripted_stat)
        else:
            cycle_stat = None

        if len(self.scripted_detail) != 0:
            cycle_detail = self.cycle(self.scripted_detail)
        else:
            cycle_detail = None

        if len(self.scripted_pic) != 0:
            cycle_pic = self.cycle(self.scripted_pic)
        else:
            cycle_pic = None

        if len(self.scripted_pic_text) != 0:
            cycle_pic_text = self.cycle(self.scripted_pic_text)
        else:
            cycle_pic_text = None

        if len(self.scripted_small_pic) != 0:
            cycle_small_pic = self.cycle(self.scripted_small_pic)
        else:
            cycle_small_pic = None

        if len(self.scripted_small_pic) != 0:
            cycle_small_pic = self.cycle(self.scripted_small_pic)
        else:
            cycle_small_pic = None

        if len(self.scripted_stat) != 0:
            cycle_small_pic_text = self.cycle(self.scripted_small_pic_text)
        else:
            cycle_small_pic_text = None
        set_act_times = 0
        try:
            while self.script_stat_activate:
                change_time = self.scripted_time
                stat = next(cycle_stat) if cycle_stat != None else None
                detail = next(cycle_detail) if cycle_detail != None else None
                pic = next(cycle_pic) if cycle_pic != None else None
                pic_text = next(cycle_pic_text) if cycle_pic_text != None else None
                small_pic = next(cycle_small_pic) if cycle_small_pic != None else None
                small_pic_text = next(cycle_small_pic_text) if cycle_small_pic_text != None else None
                buttons = []
                if button_1_isChecked:
                    button_1_list_pos = next(button_1)
                    buttons.append({"label": f"{scripted_button_1_title[button_1_list_pos[0]]}", "url": f"{scripted_button_1_url[button_1_list_pos[1]]}"})
                else:
                    button_1_list_pos = None
                if  button_2_isChecked:
                    button_2_list_pos = next(button_2)
                    buttons.append({"label": f"{scripted_button_2_title[button_2_list_pos[0]]}", "url": f"{scripted_button_2_url[button_2_list_pos[1]]}"})
                else:
                    button_2_list_pos = None
                if len(buttons) == 0:
                    buttons = None
                self.app.update(state=stat,details=detail,large_image=pic,
                    large_text=pic_text,small_image=small_pic,small_text=small_pic_text,
                    instance=True,start=start_time_stamp,end=end_time_stamp,buttons=buttons)
                try:
                    if set_ui_lable_thread.is_alive():
                        set_ui_lable_thread.join()
                except:pass
                set_ui_lable_thread  = Thread(target = self.set_script_status_UI_lable,daemon=True,args=[stat,detail,pic,pic_text,small_pic,small_pic_text,scripted_button_1_title,scripted_button_1_url,button_1_list_pos,scripted_button_2_title,scripted_button_2_url,button_2_list_pos])
                set_ui_lable_thread.run()
                while self.script_stat_activate:
                    cur_time = int(QtCore.QDateTime.currentDateTime().toPyDateTime().timestamp())
                    elapsed_time = cur_time - start_time
                    if elapsed_time >= change_time + 1:
                        set_act_times += 1
                        start_time += change_time
                        break
                    else:
                        QtTest.QTest.qWait(50)
                        self.statusMessage.setText(f"腳本模式(下次狀態更新:{change_time - elapsed_time}，已更換腳本次數:{set_act_times}，每{change_time}秒更新一次)")
                        QtTest.QTest.qWait(50)
                else:
                    return
        except:return

    def cycle(self,my_list:list):
        start_at = 0
        while True:
            yield my_list[start_at]
            start_at = (start_at + 1) % len(my_list)

    def button_1_cycle(self,button_title_list,button_url_list):
        button_title_start_at = 0
        button_url_start_at = 0
        while True:
            yield [button_title_start_at,button_url_start_at]
            button_title_start_at = (button_title_start_at + 1) % len(button_title_list)
            button_url_start_at = (button_url_start_at + 1) % len(button_url_list)

    def button_2_cycle(self,button_title_list,button_url_list):
        button_title_start_at = 0
        button_url_start_at = 0
        while True:
            yield [button_title_start_at,button_url_start_at]
            button_title_start_at = (button_title_start_at + 1) % len(button_title_list)
            button_url_start_at = (button_url_start_at + 1) % len(button_url_list)
            
    def set_script_status_UI_lable(self,stat,detail,pic,pic_text,small_pic,small_pic_text,button_1_title,button_1_url,button_1_pos,button_2_title,button_2_url,button_2_pos):
        if self.script_stat_activate:
            self.cur_detail.setText(stat)
            QtTest.QTest.qWait(10)
            self.cur_status.setText(detail)
            QtTest.QTest.qWait(10)
            self.cur_BigPicture.setText(f"{pic}({pic_text})")
            QtTest.QTest.qWait(10)
            self.cur_SmallPicture.setText(f"{small_pic}({small_pic_text})")
            QtTest.QTest.qWait(10)
            if button_1_title != None:
                self.cur_button_1.setText(f"{button_1_title[button_1_pos[0]]}({button_1_url[button_1_pos[1]]})")
            else:
                self.cur_button_1.setText(f"按鈕一未啟動")
            QtTest.QTest.qWait(10)
            if button_2_title != None:
                self.cur_button_2.setText(f"{button_2_title[button_2_pos[0]]}({button_2_url[button_2_pos[1]]})")
            else:
                self.cur_button_2.setText(f"按鈕二未啟動")

    def set_new_normal_state(self):
        log.info("set_new_normal_state")
        self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:狀態套用中..."))
        stat = self.status_entry.text() if len(self.status_entry.text()) else None
        detail = self.detail_entry.text() if len(self.detail_entry.text()) else None
        pic = self.bigPicture_name_comboBox.currentText() if len(self.bigPicture_name_comboBox.currentText()) else None
        pic_text = self.bigPicture_Entry.text() if len(self.bigPicture_Entry.text()) else None
        small_pic_text = self.smallPicture_Entry.text() if len(self.smallPicture_Entry.text()) else None
        small_pic = self.smallPicture_name_comboBox.currentText() if len(self.smallPicture_name_comboBox.currentText()) else None
        buttons = []
        if self.button_activate_checkBox_1.isChecked():
            bt1_title = self.button_title_Entry_1.text()
            bt1_url = self.button_url_Entry_1.text()
            if bt1_title == ""  or bt1_url == "":
                msg_box.warning("錯誤", "按鈕一的標題或連結網址不可為空白")
                self.cur_status_grid_title.setText(app.translate("ctrl_GUI", "目前狀態:狀態設定失敗"))
                return
            buttons.append({"label": f"{bt1_title}", "url": f"{bt1_url}"})
            self.cur_button_1.setText(f"{bt1_title}({bt1_url})")
        if self.button_activate_checkBox_2.isChecked():
            bt2_title = self.button_title_Entry_2.text()
            bt2_url = self.button_url_Entry_2.text()
            if bt2_title == ""  or bt2_url == "":
                msg_box.warning("錯誤", "按鈕二的標題或連結網址不可為空白")
                self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:狀態設定失敗"))
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
        log.info(str(time_stamp))
        try:
            self.set_act(stat,detail,pic,pic_text,small_pic,small_pic_text,time_set,time_mode,time_stamp,buttons)
            if not self.ctrl_GUI.isHidden():
                self.statusBar.showMessage("普通模式")
        except Exception as e:
            log.info("錯誤")
            msg_box.warning("錯誤", e)
        self.cur_status.setText(stat)
        self.cur_detail.setText(detail)
        self.cur_BigPicture.setText(f"{pic}({pic_text})")
        self.cur_SmallPicture.setText(f"{small_pic}({small_pic_text})")
        return

    def overwrite_user_state(self):
        log.info("overwrite user state changes...")
        self.cur_status_grid_title.setText(app.translate("ctrl_GUI", "目前狀態:正在覆蓋新的狀態設定檔..."))
        if self.script_enable_checkBox.isChecked():
            detail = self.detail
            stat = self.stat
            pic_text = self.pic_text
            small_pic_text = self.small_pic_text
            button_1_title = self.button_1_title
            button_1_url = self.button_1_url
            button_2_title = self.button_2_title
            button_2_url = self.button_2_url
        else:
            detail = self.detail_entry.text()
            stat = self.status_entry.text()
            pic_text = self.bigPicture_Entry.text()
            small_pic_text = self.smallPicture_Entry.text()
            button_1_title = self.button_title_Entry_1.text()
            button_1_url = self.button_url_Entry_1.text()
            button_2_title = self.button_title_Entry_2.text()
            button_2_url = self.button_url_Entry_2.text()
        dictionary = {"User_stored_stat":{
            "app_id": self.app_id,
            "is_script": self.script_enable_checkBox.isChecked(),
            "detail": detail,
            "stat": stat,
            "pic": self.bigPicture_name_comboBox.currentText(),
            "pic_text": pic_text,
            "small_pic": self.smallPicture_name_comboBox.currentText(),
            "small_pic_text": small_pic_text,
            "time_counting": self.open_time_counting_checkBox.isChecked(),
            "button_1_title": button_1_title,
            "button_1_url": button_1_url,
            "button_1_activate": self.button_activate_checkBox_1.isChecked(),
            "button_2_title": button_2_title,
            "button_2_url": button_2_url,
            "button_2_activate": self.button_activate_checkBox_2.isChecked()
                },
        "Scripted_stored_data":{
            "time_counting": self.scripted_time,
            "detail": self.scripted_detail,
            "stat": self.scripted_stat,
            "pic": self.scripted_pic,
            "pic_text": self.scripted_pic_text,
            "small_pic": self.scripted_small_pic,
            "small_pic_text": self.scripted_small_pic_text,
            "button_1_title": self.scripted_button_1_title,
            "button_1_url": self.scripted_button_1_url,
            "button_2_title": self.scripted_button_2_title,
            "button_2_url": self.scripted_button_2_url
            }}
        json_object = dumps(dictionary, indent = 3)
        with open(f'./data/{file_title}.json', "w", encoding="UTF-8") as json_file:
            json_file.write(json_object)
        json_file.close()
        QtTest.QTest.qWait(100)
        self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:已儲存新的狀態設定檔"))
        
    def add_picture(self):
        log.info("add_picture")
        raw_picture_list = loads(requests.get(f"https://discordapp.com/api/oauth2/applications/{self.app_id}/assets").text)
        picture_list = []
        for i in raw_picture_list:
            picture_list.append(i["name"])
        picture_list.append("不顯示圖片")
        self.bigPicture_name_comboBox.addItems(picture_list)
        self.smallPicture_name_comboBox.addItems(picture_list)
        self.bigPicture_name_comboBox.setCurrentText(self.pic)
        self.smallPicture_name_comboBox.setCurrentText(self.small_pic)
        return

    def setupUi(self, ctrl_GUI):
        ctrl_GUI.setObjectName("ctrl_GUI")
        ctrl_GUI.setWindowModality(QtCore.Qt.NonModal)
        ctrl_GUI.resize(1000, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ctrl_GUI.sizePolicy().hasHeightForWidth())
        ctrl_GUI.setSizePolicy(sizePolicy)
        ctrl_GUI.setMinimumSize(QtCore.QSize(1000, 400))
        ctrl_GUI.setMaximumSize(QtCore.QSize(1000, 400))
        ctrl_GUI.setSizeIncrement(QtCore.QSize(1, 1))
        font = QtGui.QFont()
        font.setFamily("SF Pro Display")
        font.setPointSize(9)
        ctrl_GUI.setFont(font)
        ctrl_GUI.setMouseTracking(True)
        ctrl_GUI.setFocusPolicy(QtCore.Qt.StrongFocus)
        ctrl_GUI.setWindowIcon(icon)
        ctrl_GUI.setAutoFillBackground(True)
        ctrl_GUI.setStyleSheet("")
        ctrl_GUI.setAnimated(True)
        ctrl_GUI.setDocumentMode(False)
        ctrl_GUI.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(ctrl_GUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(1000, 370))
        self.centralwidget.setMaximumSize(QtCore.QSize(1000, 370))
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_status_grid = QtWidgets.QGridLayout()
        self.main_status_grid.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.main_status_grid.setContentsMargins(15, 15, 20, 10)
        self.main_status_grid.setHorizontalSpacing(15)
        self.main_status_grid.setVerticalSpacing(20)
        self.main_status_grid.setObjectName("main_status_grid")
        self.cur_status_title_2 = QtWidgets.QLabel(self.centralwidget)
        self.cur_status_title_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.cur_status_title_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_status_title_2.setObjectName("cur_status_title_2")
        self.main_status_grid.addWidget(self.cur_status_title_2, 1, 0, 1, 1)
        self.status_setting_grid = QtWidgets.QGridLayout()
        self.status_setting_grid.setContentsMargins(4, -1, -1, -1)
        self.status_setting_grid.setHorizontalSpacing(10)
        self.status_setting_grid.setVerticalSpacing(8)
        self.status_setting_grid.setObjectName("status_setting_grid")
        self.status_lable = QtWidgets.QLabel(self.centralwidget)
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
        self.detail_lable = QtWidgets.QLabel(self.centralwidget)
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
        self.detail_entry = QtWidgets.QLineEdit(self.centralwidget)
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
        self.status_entry = QtWidgets.QLineEdit(self.centralwidget)
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
        self.main_picture_setting_title = QtWidgets.QLabel(self.centralwidget)
        self.main_picture_setting_title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.main_picture_setting_title.setObjectName("main_picture_setting_title")
        self.main_status_grid.addWidget(self.main_picture_setting_title, 2, 0, 1, 1)
        self.small_picture_setting_title = QtWidgets.QLabel(self.centralwidget)
        self.small_picture_setting_title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.small_picture_setting_title.setObjectName("small_picture_setting_title")
        self.main_status_grid.addWidget(self.small_picture_setting_title, 3, 0, 1, 1)
        self.cur_user_title_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cur_user_title_2.sizePolicy().hasHeightForWidth())
        self.cur_user_title_2.setSizePolicy(sizePolicy)
        self.cur_user_title_2.setMinimumSize(QtCore.QSize(0, 0))
        self.cur_user_title_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cur_user_title_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cur_user_title_2.setObjectName("cur_user_title_2")
        self.main_status_grid.addWidget(self.cur_user_title_2, 0, 0, 1, 1)
        self.main_picture_setting_grid = QtWidgets.QGridLayout()
        self.main_picture_setting_grid.setContentsMargins(4, 0, -1, -1)
        self.main_picture_setting_grid.setHorizontalSpacing(10)
        self.main_picture_setting_grid.setObjectName("main_picture_setting_grid")
        self.bigPicture_name_lable = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bigPicture_name_lable.sizePolicy().hasHeightForWidth())
        self.bigPicture_name_lable.setSizePolicy(sizePolicy)
        self.bigPicture_name_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.bigPicture_name_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.bigPicture_name_lable.setObjectName("bigPicture_name_lable")
        self.main_picture_setting_grid.addWidget(self.bigPicture_name_lable, 0, 2, 1, 1)
        self.bigPicture_Entry = QtWidgets.QLineEdit(self.centralwidget)
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
        self.bigPicture_lable = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bigPicture_lable.sizePolicy().hasHeightForWidth())
        self.bigPicture_lable.setSizePolicy(sizePolicy)
        self.bigPicture_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.bigPicture_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.bigPicture_lable.setObjectName("bigPicture_lable")
        self.main_picture_setting_grid.addWidget(self.bigPicture_lable, 0, 0, 1, 1)
        self.bigPicture_name_comboBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bigPicture_name_comboBox.sizePolicy().hasHeightForWidth())
        self.bigPicture_name_comboBox.setSizePolicy(sizePolicy)
        self.bigPicture_name_comboBox.setMinimumSize(QtCore.QSize(183, 24))
        self.bigPicture_name_comboBox.setMaximumSize(QtCore.QSize(183, 24))
        self.bigPicture_name_comboBox.setObjectName("bigPicture_name_comboBox")
        self.main_picture_setting_grid.addWidget(self.bigPicture_name_comboBox, 0, 3, 1, 1)
        self.main_status_grid.addLayout(self.main_picture_setting_grid, 2, 1, 1, 1)
        self.smallPicture_setting_grid = QtWidgets.QGridLayout()
        self.smallPicture_setting_grid.setContentsMargins(4, -1, -1, -1)
        self.smallPicture_setting_grid.setHorizontalSpacing(10)
        self.smallPicture_setting_grid.setObjectName("smallPicture_setting_grid")
        self.smallPicture_name_comboBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallPicture_name_comboBox.sizePolicy().hasHeightForWidth())
        self.smallPicture_name_comboBox.setSizePolicy(sizePolicy)
        self.smallPicture_name_comboBox.setMinimumSize(QtCore.QSize(183, 24))
        self.smallPicture_name_comboBox.setMaximumSize(QtCore.QSize(183, 24))
        self.smallPicture_name_comboBox.setObjectName("smallPicture_name_comboBox")
        self.smallPicture_setting_grid.addWidget(self.smallPicture_name_comboBox, 0, 3, 1, 1)
        self.smallPicture_Entry = QtWidgets.QLineEdit(self.centralwidget)
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
        self.smallPicture_lable = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallPicture_lable.sizePolicy().hasHeightForWidth())
        self.smallPicture_lable.setSizePolicy(sizePolicy)
        self.smallPicture_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.smallPicture_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.smallPicture_lable.setObjectName("smallPicture_lable")
        self.smallPicture_setting_grid.addWidget(self.smallPicture_lable, 0, 0, 1, 1)
        self.smallPicture_name_lable = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallPicture_name_lable.sizePolicy().hasHeightForWidth())
        self.smallPicture_name_lable.setSizePolicy(sizePolicy)
        self.smallPicture_name_lable.setMinimumSize(QtCore.QSize(65, 24))
        self.smallPicture_name_lable.setMaximumSize(QtCore.QSize(65, 24))
        self.smallPicture_name_lable.setObjectName("smallPicture_name_lable")
        self.smallPicture_setting_grid.addWidget(self.smallPicture_name_lable, 0, 2, 1, 1)
        self.main_status_grid.addLayout(self.smallPicture_setting_grid, 3, 1, 1, 1)
        self.button_setting_title_1 = QtWidgets.QLabel(self.centralwidget)
        self.button_setting_title_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.button_setting_title_1.setObjectName("button_setting_title_1")
        self.main_status_grid.addWidget(self.button_setting_title_1, 4, 0, 1, 1)
        self.button_setting_title_2 = QtWidgets.QLabel(self.centralwidget)
        self.button_setting_title_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.button_setting_title_2.setObjectName("button_setting_title_2")
        self.main_status_grid.addWidget(self.button_setting_title_2, 5, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cur_user = QtWidgets.QLabel(self.centralwidget)
        self.cur_user.setEnabled(True)
        self.cur_user.setMaximumSize(QtCore.QSize(376, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.cur_user.setFont(font)
        self.cur_user.setObjectName("cur_user")
        self.horizontalLayout_5.addWidget(self.cur_user)
        self.reload_file_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reload_file_button.sizePolicy().hasHeightForWidth())
        self.reload_file_button.setSizePolicy(sizePolicy)
        self.reload_file_button.setMinimumSize(QtCore.QSize(80, 26))
        self.reload_file_button.setMaximumSize(QtCore.QSize(80, 26))
        self.reload_file_button.setObjectName("reload_file_button")
        self.horizontalLayout_5.addWidget(self.reload_file_button)
        self.open_script_setting_Button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_script_setting_Button.sizePolicy().hasHeightForWidth())
        self.open_script_setting_Button.setSizePolicy(sizePolicy)
        self.open_script_setting_Button.setMinimumSize(QtCore.QSize(80, 26))
        self.open_script_setting_Button.setMaximumSize(QtCore.QSize(80, 26))
        self.open_script_setting_Button.setObjectName("open_script_setting_Button")
        self.horizontalLayout_5.addWidget(self.open_script_setting_Button)
        self.go_to_dev_web_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go_to_dev_web_button.sizePolicy().hasHeightForWidth())
        self.go_to_dev_web_button.setSizePolicy(sizePolicy)
        self.go_to_dev_web_button.setMaximumSize(QtCore.QSize(150, 26))
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
        self.button_title_Entry_1 = QtWidgets.QLineEdit(self.centralwidget)
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
        self.button_url_lable_1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_url_lable_1.sizePolicy().hasHeightForWidth())
        self.button_url_lable_1.setSizePolicy(sizePolicy)
        self.button_url_lable_1.setMinimumSize(QtCore.QSize(65, 24))
        self.button_url_lable_1.setMaximumSize(QtCore.QSize(65, 24))
        self.button_url_lable_1.setObjectName("button_url_lable_1")
        self.button_1_setting_grid_2.addWidget(self.button_url_lable_1, 0, 2, 1, 1)
        self.button_title_lable_1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_title_lable_1.sizePolicy().hasHeightForWidth())
        self.button_title_lable_1.setSizePolicy(sizePolicy)
        self.button_title_lable_1.setMinimumSize(QtCore.QSize(65, 24))
        self.button_title_lable_1.setMaximumSize(QtCore.QSize(65, 24))
        self.button_title_lable_1.setObjectName("button_title_lable_1")
        self.button_1_setting_grid_2.addWidget(self.button_title_lable_1, 0, 0, 1, 1)
        self.button_activate_checkBox_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.button_activate_checkBox_1.setObjectName("button_activate_checkBox_1")
        self.button_1_setting_grid_2.addWidget(self.button_activate_checkBox_1, 0, 4, 1, 1)
        self.button_url_Entry_1 = QtWidgets.QLineEdit(self.centralwidget)
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
        self.button_title_lable_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_title_lable_2.sizePolicy().hasHeightForWidth())
        self.button_title_lable_2.setSizePolicy(sizePolicy)
        self.button_title_lable_2.setMinimumSize(QtCore.QSize(65, 24))
        self.button_title_lable_2.setMaximumSize(QtCore.QSize(65, 24))
        self.button_title_lable_2.setObjectName("button_title_lable_2")
        self.button_2_setting_grid_3.addWidget(self.button_title_lable_2, 0, 0, 1, 1)
        self.button_title_Entry_2 = QtWidgets.QLineEdit(self.centralwidget)
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
        self.button_url_lable_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_url_lable_2.sizePolicy().hasHeightForWidth())
        self.button_url_lable_2.setSizePolicy(sizePolicy)
        self.button_url_lable_2.setMinimumSize(QtCore.QSize(65, 24))
        self.button_url_lable_2.setMaximumSize(QtCore.QSize(65, 24))
        self.button_url_lable_2.setObjectName("button_url_lable_2")
        self.button_2_setting_grid_3.addWidget(self.button_url_lable_2, 0, 2, 1, 1)
        self.button_activate_checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.button_activate_checkBox_2.setObjectName("button_activate_checkBox_2")
        self.button_2_setting_grid_3.addWidget(self.button_activate_checkBox_2, 0, 4, 1, 1)
        self.button_url_Entry_2 = QtWidgets.QLineEdit(self.centralwidget)
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
        self.time_setting_title_3 = QtWidgets.QLabel(self.centralwidget)
        self.time_setting_title_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time_setting_title_3.setObjectName("time_setting_title_3")
        self.main_status_grid.addWidget(self.time_setting_title_3, 6, 0, 1, 1)
        self.time_setting_grid_2 = QtWidgets.QGridLayout()
        self.time_setting_grid_2.setContentsMargins(0, -1, -1, -1)
        self.time_setting_grid_2.setHorizontalSpacing(10)
        self.time_setting_grid_2.setVerticalSpacing(8)
        self.time_setting_grid_2.setObjectName("time_setting_grid_2")
        self.open_time_counting_checkBox = QtWidgets.QCheckBox(self.centralwidget)
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
        self.time_setting = QtWidgets.QDateTimeEdit(self.centralwidget)
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
        self.time_mode = QtWidgets.QComboBox(self.centralwidget)
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
        self.time_reset_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_reset_button.sizePolicy().hasHeightForWidth())
        self.time_reset_button.setSizePolicy(sizePolicy)
        self.time_reset_button.setMinimumSize(QtCore.QSize(75, 26))
        self.time_reset_button.setMaximumSize(QtCore.QSize(75, 26))
        self.time_reset_button.setObjectName("time_reset_button")
        self.time_setting_grid_2.addWidget(self.time_reset_button, 0, 4, 1, 1)
        self.main_status_grid.addLayout(self.time_setting_grid_2, 6, 1, 1, 1)
        self.RPC_state_1 = QtWidgets.QHBoxLayout()
        self.RPC_state_1.setObjectName("RPC_state_1")
        self.cur_detail_label = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_detail = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_status_grid_title = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_status_label = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_status = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_BigPicture_lable = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_BigPicture = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_SmallPicture_lable = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_SmallPicture = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_button_lable_1 = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_button_1 = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_button_lable_2 = QtWidgets.QLabel(self.centralwidget)
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
        self.cur_button_2 = QtWidgets.QLabel(self.centralwidget)
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
        self.verticalLayout.addLayout(self.main_status_grid)
        self.activate_button_grid = QtWidgets.QGridLayout()
        self.activate_button_grid.setContentsMargins(5, 0, 5, 0)
        self.activate_button_grid.setObjectName("activate_button_grid")
        self.save_data_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_data_button.sizePolicy().hasHeightForWidth())
        self.save_data_button.setSizePolicy(sizePolicy)
        self.save_data_button.setMinimumSize(QtCore.QSize(0, 30))
        self.save_data_button.setMaximumSize(QtCore.QSize(155, 30))
        self.save_data_button.setSizeIncrement(QtCore.QSize(0, 28))
        self.save_data_button.setDefault(False)
        self.save_data_button.setObjectName("save_data_button")
        self.activate_button_grid.addWidget(self.save_data_button, 0, 2, 1, 1)
        self.activate_status_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.activate_status_button.sizePolicy().hasHeightForWidth())
        self.activate_status_button.setSizePolicy(sizePolicy)
        self.activate_status_button.setMinimumSize(QtCore.QSize(310, 30))
        self.activate_status_button.setMaximumSize(QtCore.QSize(310, 30))
        self.activate_status_button.setObjectName("activate_status_button")
        self.activate_button_grid.addWidget(self.activate_status_button, 0, 3, 1, 1)
        self.close_window_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_window_button.sizePolicy().hasHeightForWidth())
        self.close_window_button.setSizePolicy(sizePolicy)
        self.close_window_button.setMinimumSize(QtCore.QSize(325, 30))
        self.close_window_button.setMaximumSize(QtCore.QSize(325, 30))
        self.close_window_button.setObjectName("close_window_button")
        self.activate_button_grid.addWidget(self.close_window_button, 0, 5, 1, 1)
        self.save_data_button_2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_data_button_2.sizePolicy().hasHeightForWidth())
        self.save_data_button_2.setSizePolicy(sizePolicy)
        self.save_data_button_2.setMinimumSize(QtCore.QSize(0, 30))
        self.save_data_button_2.setMaximumSize(QtCore.QSize(160, 30))
        self.save_data_button_2.setSizeIncrement(QtCore.QSize(0, 0))
        self.save_data_button_2.setDefault(False)
        self.save_data_button_2.setObjectName("save_data_button_2")
        self.activate_button_grid.addWidget(self.save_data_button_2, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.activate_button_grid)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        ctrl_GUI.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(ctrl_GUI)
        self.statusBar.setObjectName("statusBar")
        ctrl_GUI.setStatusBar(self.statusBar)
        self.white_mode = QtWidgets.QAction(ctrl_GUI)
        self.white_mode.setCheckable(True)
        self.white_mode.setObjectName("white_mode")
        self.dark_mode = QtWidgets.QAction(ctrl_GUI)
        self.dark_mode.setCheckable(True)
        self.dark_mode.setObjectName("dark_mode")
        self.hide_RPC_status = QtWidgets.QAction(ctrl_GUI)
        self.hide_RPC_status.setCheckable(True)
        self.hide_RPC_status.setObjectName("hide_RPC_status")
        self.statusMessage = QtWidgets.QLabel()
        self.statusMessage.setText("狀態尚未啟用")
        self.statusBar.addWidget(self.statusMessage)

        self.retranslateUi(ctrl_GUI)
        QtCore.QMetaObject.connectSlotsByName(ctrl_GUI)
    
    def retranslateUi(self, ctrl_GUI):
        _translate = QtCore.QCoreApplication.translate
        ctrl_GUI.setWindowTitle(_translate("ctrl_GUI", version))
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
        self.bigPicture_name_comboBox.setPlaceholderText(_translate("ctrl_GUI", "請輸入圖片名稱"))
        self.smallPicture_name_lable.setText(_translate("ctrl_GUI", "小圖名稱"))
        self.smallPicture_lable.setText(_translate("ctrl_GUI", "小圖標題"))
        self.smallPicture_Entry.setPlaceholderText(_translate("ctrl_GUI", "請輸入小圖標題"))
        self.smallPicture_name_comboBox.setPlaceholderText(_translate("ctrl_GUI", "請輸入小圖名稱"))
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
        self.open_script_setting_Button.setText(_translate("ctrl_GUI", "腳本設定"))
        
        status = self.stat
        detail = self.detail
        bigPicture = self.pic_text
        bigPicture_name = self.pic
        smallPicture = self.small_pic_text
        smallPicture_name = self.small_pic
        button_1_title = self.button_1_title
        button_1_url = self.button_1_url
        button_2_title = self.button_2_title
        button_2_url = self.button_2_url

        self.status_entry.setText(_translate("ctrl_GUI",status))
        self.detail_entry.setText(_translate("ctrl_GUI",detail))
        self.bigPicture_Entry.setText(_translate("ctrl_GUI",bigPicture))
        self.bigPicture_name_comboBox.setCurrentText(_translate("ctrl_GUI",bigPicture_name))
        self.smallPicture_Entry.setText(_translate("ctrl_GUI",smallPicture))
        self.smallPicture_name_comboBox.setCurrentText(_translate("ctrl_GUI",smallPicture_name))
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
        self.open_time_counting_checkBox.setChecked(self.time_count)

        if self.button_1_activate:
            self.button_activate_checkBox_1.setChecked(True)
            self.button_title_Entry_1.setEnabled(True)
            self.button_url_Entry_1.setEnabled(True)
        else:
            self.button_activate_checkBox_1.setChecked(False)
            self.button_title_Entry_1.setEnabled(False)
            self.button_url_Entry_1.setEnabled(False)
        
        if self.button_2_activate:
            self.button_activate_checkBox_2.setChecked(True)
            self.button_title_Entry_2.setEnabled(True)
            self.button_url_Entry_2.setEnabled(True)
        else:
            self.button_activate_checkBox_2.setChecked(False)
            self.button_title_Entry_2.setEnabled(False)
            self.button_url_Entry_2.setEnabled(False)
        self.save_data_button.setEnabled(self.new_file)

        if self.time_count:
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
        self.close_window_button.clicked.connect(self.window_minimum)
        self.go_to_dev_web_button.clicked.connect(self.open_discord_dev)
        self.time_mode.currentTextChanged.connect(self.on_Timemode_changed)
        self.time_reset_button.clicked.connect(self.reset_QDateTime)
        self.button_activate_checkBox_1.stateChanged.connect(self.button_activate_checkBox_1_changed)
        self.button_activate_checkBox_2.stateChanged.connect(self.button_activate_checkBox_2_changed)
        self.open_time_counting_checkBox.stateChanged.connect(self.time_activate_checkBox_changed)
        self.reload_file_button.clicked.connect(self.main_window_reload)
        self.open_script_setting_Button.clicked.connect(self.show_script_setting_window)
        QShortcut(QtGui.QKeySequence("Ctrl+S"), ctrl_GUI, activated=self.overwrite_user_state).setAutoRepeat(False)
        QShortcut(QtGui.QKeySequence("Ctrl+L"), ctrl_GUI, activated=log.logging_ui.show).setAutoRepeat(False)
        QShortcut(QtGui.QKeySequence("Ctrl+R"), ctrl_GUI, activated=self.set_new_state).setAutoRepeat(False)

    def set_new_state(self):
        if not self.activate_status_button.isEnabled():return
        self.activate_status_button.setEnabled(False)
        self.cur_status_grid_title.setText(app.translate("ctrl_GUI", f"目前狀態:狀態套用中..."))
        if self.script_enable_checkBox.isChecked():
            self.set_new_script_state()
            self.script_stat_activate = True
        else:
            try:
                while self.set_script_state_thread.is_alive():
                    self.script_stat_activate = False
                    self.set_script_state_thread.join()
            except:pass
            self.set_new_normal_state()

    def show_script_setting_window(self):
        log.info("show_script_setting_window")
        title = self.script_list_combobox.currentText()
        if title == "主標":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_detail))

        elif title == "副標":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_stat))

        elif title == "大圖標題":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_pic_text))

        elif title == "大圖名稱":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_pic))

        elif title == "小圖標題":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_small_pic_text))

        elif title == "小圖名稱":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_small_pic))

        elif title == "按鈕一標題":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_button_1_title))

        elif title == "按鈕一網址":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_button_1_url))

        elif title == "按鈕二標題":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_button_2_title))

        elif title == "按鈕二網址":
            self.script_textEdit.setText(self.list_to_textEdit(self.temp_scripted_button_2_url))

        cursor = self.script_textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.script_textEdit.setTextCursor(cursor)
        self.time_change_spinBox.setValue(self.scripted_time)
        self.isEdit = False
        self.script_setting_ui.show()
        self.script_textEdit.setFocus()

    def main_window_reload(self):
        log.info("main_window_reload")
        self.reload = Ui_restart_ui()

    def open_save_window(self):
        log.info("open_save_window")
        if self.script_enable_checkBox.isChecked():
            detail = self.detail
            stat = self.stat
            pic_text = self.pic_text
            small_pic_text = self.small_pic_text
            button_1_title = self.button_1_title
            button_1_url = self.button_1_url
            button_2_title = self.button_2_title
            button_2_url = self.button_2_url
        else:
            detail = self.detail_entry.text()
            stat = self.status_entry.text()
            pic_text = self.bigPicture_Entry.text()
            small_pic_text = self.smallPicture_Entry.text()
            button_1_title = self.button_title_Entry_1.text()
            button_1_url = self.button_url_Entry_1.text()
            button_2_title = self.button_title_Entry_2.text()
            button_2_url = self.button_url_Entry_2.text()
        dictionary = {"User_stored_stat":{
            "app_id": self.app_id,
            "is_script": self.script_enable_checkBox.isChecked(),
            "detail": detail,
            "stat": stat,
            "pic": self.bigPicture_name_comboBox.currentText(),
            "pic_text": pic_text,
            "small_pic": self.smallPicture_name_comboBox.currentText(),
            "small_pic_text": small_pic_text,
            "time_counting": self.open_time_counting_checkBox.isChecked(),
            "button_1_title": button_1_title,
            "button_1_url": button_1_url,
            "button_1_activate": self.button_activate_checkBox_1.isChecked(),
            "button_2_title": button_2_title,
            "button_2_url": button_2_url,
            "button_2_activate": self.button_activate_checkBox_2.isChecked()
                },
        "Scripted_stored_data":{
            "time_counting": self.scripted_time,
            "detail": self.scripted_detail,
            "stat": self.scripted_stat,
            "pic": self.scripted_pic,
            "pic_text": self.scripted_pic_text,
            "small_pic": self.scripted_small_pic,
            "small_pic_text": self.scripted_small_pic_text,
            "button_1_title": self.scripted_button_1_title,
            "button_1_url": self.scripted_button_1_url,
            "button_2_title": self.scripted_button_2_title,
            "button_2_url": self.scripted_button_2_url
            }}
        
        if self.save_window is None:
            self.save_window = Ui_Save_As()
            self.save_window.show_window(dictionary)
        else:
            self.save_window.show_window(dictionary)
        self.save_data_button.setEnabled(True)
        self.cur_user.setText(file_title)

    def open_discord_dev(self):
        log.info("open_discord_dev")
        url=QUrl(f"https://discord.com/developers/applications/{self.app_id}/rich-presence/assets")
        QDesktopServices.openUrl(url)

    def button_activate_checkBox_1_changed(self):
        log.info("button_activate_checkBox_1_changed")
        if self.button_activate_checkBox_1.isChecked():
            if not self.script_enable_checkBox.isChecked():
                self.button_title_Entry_1.setEnabled(True)
                self.button_url_Entry_1.setEnabled(True)
        else:
            self.button_title_Entry_1.setEnabled(False)
            self.button_url_Entry_1.setEnabled(False)

    def button_activate_checkBox_2_changed(self):
        log.info("button_activate_checkBox_2_changed")
        if self.button_activate_checkBox_2.isChecked():
            if not self.script_enable_checkBox.isChecked():
                self.button_title_Entry_2.setEnabled(True)
                self.button_url_Entry_2.setEnabled(True)
        else:
            self.button_title_Entry_2.setEnabled(False)
            self.button_url_Entry_2.setEnabled(False)
    
    def on_Timemode_changed(self, value):
        log.info("on_Timemode_changed")
        if self.open_time_counting_checkBox.isChecked():
            if value == "從零開始":
                self.time_setting.setEnabled(False)
                self.time_reset_button.setEnabled(False)
            else:
                self.time_setting.setEnabled(True)
                self.time_reset_button.setEnabled(True)

    def time_activate_checkBox_changed(self):
        log.info("time_activate_checkBox_changed")
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
        log.info("reset_QDateTime")
        self.time_setting.setDateTime(QtCore.QDateTime.currentDateTime())

    def init_script_setting_window(self):
        self.script_setting_ui = QtWidgets.QWidget()
        self.script_setting_window_ui = self.script_setting_ui_setupUi(self.script_setting_ui)
        self.script_setting_ui.setWindowIcon(icon)
        self.temp_scripted_detail = self.scripted_detail
        self.temp_scripted_stat = self.scripted_stat
        self.temp_scripted_pic = self.scripted_pic
        self.temp_scripted_pic_text = self.scripted_pic_text
        self.temp_scripted_small_pic = self.scripted_small_pic
        self.temp_scripted_small_pic_text = self.scripted_small_pic_text
        self.temp_scripted_button_1_title = self.scripted_button_1_title
        self.temp_scripted_button_1_url = self.scripted_button_1_url
        self.temp_scripted_button_2_title = self.scripted_button_2_title
        self.temp_scripted_button_2_url = self.scripted_button_2_url
        self.temp_scripted_change_time = self.scripted_time

    def script_setting_ui_setupUi(self, script_setting_ui):
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
        self.time_change_spinBox.setMinimum(10)
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

        self.script_setting_ui_retranslateUi(script_setting_ui)
        QtCore.QMetaObject.connectSlotsByName(script_setting_ui)
        self.close_script_editor_button.clicked.connect(self.close_script_editor)
        self.script_list_combobox.currentTextChanged.connect(self.script_list_combobox_changed)
        self.save_script_button.clicked.connect(self.save_scripts_button_clicked)
        self.script_textEdit.textChanged.connect(self.script_textEdit_changed)
        self.script_enable_checkBox.stateChanged.connect(self.script_enable_checkBox_changed)
        self.script_enable_checkBox.setChecked(self.is_script)
        QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), script_setting_ui, activated=self.script_setting_ui.destroy).setAutoRepeat(False)
        QShortcut(QtGui.QKeySequence("Ctrl+L"), script_setting_ui, activated=log.logging_ui.show).setAutoRepeat(False)

    def script_setting_ui_retranslateUi(self, script_setting_ui):
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
        self.Previous_title = "主標"

    def script_enable_checkBox_changed(self):
        if self.script_enable_checkBox.isChecked():
            log.info("script mode")
            use_script = False
            self.detail_entry.setText("腳本套用中")
            self.status_entry.setText("腳本套用中")
            self.bigPicture_Entry.setText("腳本套用中")
            self.smallPicture_Entry.setText("腳本套用中")
            self.button_title_Entry_1.setText("腳本套用中")
            self.button_url_Entry_1.setText("腳本套用中")
            self.button_title_Entry_2.setText("腳本套用中")
            self.button_url_Entry_2.setText("腳本套用中")
        else:
            log.info("normal mode")
            use_script = True
            self.detail_entry.setText(self.detail)
            self.status_entry.setText(self.stat)
            self.bigPicture_Entry.setText(self.pic_text)
            self.smallPicture_Entry.setText(self.small_pic_text)
            self.button_title_Entry_1.setText(self.button_1_title)
            self.button_url_Entry_1.setText(self.button_1_url)
            self.button_title_Entry_2.setText(self.button_2_title)
            self.button_url_Entry_2.setText(self.button_2_url)

        self.detail_entry.setEnabled(use_script)
        self.status_entry.setEnabled(use_script)
        self.bigPicture_Entry.setEnabled(use_script)
        self.bigPicture_name_comboBox.setEnabled(use_script)
        self.smallPicture_Entry.setEnabled(use_script)
        self.smallPicture_name_comboBox.setEnabled(use_script)
        self.button_title_Entry_1.setEnabled(use_script)
        self.button_url_Entry_1.setEnabled(use_script)
        self.button_title_Entry_2.setEnabled(use_script)
        self.button_url_Entry_2.setEnabled(use_script)
        return

    def script_textEdit_changed(self):
        log.info("Script text changed")
        script_quantity = str(len(self.script_textEdit.toPlainText().split('\n')))
        self.show_script_quantity.setText(script_quantity)
        self.isEdit = True
        return

    def save_scripts_button_clicked(self):
        log.info("save_scripts_button_clicked")
        temp_data = self.script_textEdit.toPlainText().split('\n')
        data = list(temp_data)
        for i in range(len(temp_data)):
            if temp_data[i] == '':
                data.remove('')
        title = self.script_list_combobox.currentText()
        if title == "主標":
            self.temp_scripted_detail = data

        elif title == "副標":
            self.temp_scripted_stat = data

        elif title == "大圖標題":
            self.temp_scripted_pic_text = data

        elif title == "大圖名稱":
            self.temp_scripted_pic = data

        elif title == "小圖標題":
            self.temp_scripted_small_pic_text = data

        elif title == "小圖名稱":
            self.temp_scripted_small_pic = data

        elif title == "按鈕一標題":
            self.temp_scripted_button_1_title = data

        elif title == "按鈕一網址":
            self.temp_scripted_button_1_url = data

        elif title == "按鈕二標題":
            self.temp_scripted_button_2_title = data

        elif title == "按鈕二網址":
            self.temp_scripted_button_2_url = data

        self.scripted_detail = self.temp_scripted_detail
        self.scripted_stat = self.temp_scripted_stat
        self.scripted_pic = self.temp_scripted_pic
        self.scripted_pic_text = self.temp_scripted_pic_text
        self.scripted_small_pic = self.temp_scripted_small_pic
        self.scripted_small_pic_text = self.temp_scripted_small_pic_text
        self.scripted_button_1_title = self.temp_scripted_button_1_title
        self.scripted_button_1_url = self.temp_scripted_button_1_url
        self.scripted_button_2_title = self.temp_scripted_button_2_title
        self.scripted_button_2_url = self.temp_scripted_button_2_url
        self.scripted_time = int(self.time_change_spinBox.text())
        for tl in QtWidgets.QApplication.topLevelWidgets():
            if tl.windowTitle() == "狀態腳本設定":
                tl.destroy()
        self.overwrite_user_state()
        return
        
    def script_list_combobox_changed(self,title):
        log.info("script_list_combobox_changed")
        temp_data = self.script_textEdit.toPlainText().split('\n')
        self.show_script_quantity.setText(str(len(temp_data)))
        data = list(temp_data)
        for i in range(len(temp_data)):
            if temp_data[i] == '':
                data.remove('')
        log.info(f"上一個項目:{self.Previous_title}\n本項目:{title}\n內容:{data}")

        if self.Previous_title == "主標":
            self.temp_scripted_detail = data

        elif self.Previous_title == "副標":
            self.temp_scripted_stat = data

        elif self.Previous_title == "大圖標題":
            self.temp_scripted_pic_text = data

        elif self.Previous_title == "大圖名稱":
            self.temp_scripted_pic = data

        elif self.Previous_title == "小圖標題":
            self.temp_scripted_small_pic_text = data

        elif self.Previous_title == "小圖名稱":
            self.temp_scripted_small_pic = data

        elif self.Previous_title == "按鈕一標題":
            self.temp_scripted_button_1_title = data

        elif self.Previous_title == "按鈕一網址":
            self.temp_scripted_button_1_url = data

        elif self.Previous_title == "按鈕二標題":
            self.temp_scripted_button_2_title = data

        elif self.Previous_title == "按鈕二網址":
            self.temp_scripted_button_2_url = data


        if title == "主標":
            temp = self.list_to_textEdit(self.temp_scripted_detail)

        elif title == "副標":
            temp = self.list_to_textEdit(self.temp_scripted_stat)

        elif title == "大圖標題":
            temp = self.list_to_textEdit(self.temp_scripted_pic_text)

        elif title == "大圖名稱":
            temp = self.list_to_textEdit(self.temp_scripted_pic)

        elif title == "小圖標題":
            temp = self.list_to_textEdit(self.temp_scripted_small_pic_text)

        elif title == "小圖名稱":
            temp = self.list_to_textEdit(self.temp_scripted_small_pic)

        elif title == "按鈕一標題":
            temp = self.list_to_textEdit(self.temp_scripted_button_1_title)

        elif title == "按鈕一網址":
            temp = self.list_to_textEdit(self.temp_scripted_button_1_url)

        elif title == "按鈕二標題":
            temp = self.list_to_textEdit(self.temp_scripted_button_2_title)

        elif title == "按鈕二網址":
            temp = self.list_to_textEdit(self.temp_scripted_button_2_url)

        QtTest.QTest.qWait(1)
        self.script_textEdit.setPlainText(temp)
        self.Previous_title = title
        self.script_textEdit.setFocus()
        cursor = self.script_textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.script_textEdit.setTextCursor(cursor)
        return
    
    def list_to_textEdit(self,value):
        if len(value) > 0:
            output = ""
            for i in value:
                output = output + i + "\n"
            return output
        else:return

    def close_script_editor(self):
        log.info("close_script_editor")
        if self.isEdit:
            messageBox = QMessageBox()
            messageBox.setWindowIcon(icon)
            messageBox.setWindowTitle(' Discord狀態修改器')
            messageBox.setText('不儲存腳本並直接關閉編輯器?')
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('是的')
            buttonN = messageBox.button(QMessageBox.No)
            buttonN.setText('繼續編輯')
            messageBox.exec_()

            if messageBox.clickedButton() == buttonY:
                log.info('yes')
                for tl in QtWidgets.QApplication.topLevelWidgets():
                    if tl.windowTitle() == "狀態腳本設定":
                        tl.destroy()
                        return
            else :
                return
        else:
            for tl in QtWidgets.QApplication.topLevelWidgets():
                if tl.windowTitle() == "狀態腳本設定":
                    tl.destroy()
                    return

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
        log.info("start_ui closed")
        exit()

    def get_file_name(self):
        log.info("start get_file_name")
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

        QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self.comboBox, activated=self._init_main_ui).setAutoRepeat(False)
        QShortcut(QtGui.QKeySequence("Ctrl+L"), start_ui, activated=log.logging_ui.show).setAutoRepeat(False)

    def open_discord_dev(self):
        url=QUrl("https://discord.com/developers/applications/")
        QDesktopServices.openUrl(url)

    def _init_main_ui(self):
        global file_title
        try:
            file_title = self.comboBox.currentText()
            self.main_GUI = ctrl_GUI(self.dir_list)
            self.start_ui.hide()
        except Exception as e:
            msg_box.warning("錯誤",e)
            return

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
        QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self.lineEdit, activated=self.save_user_state).setAutoRepeat(False)
        QShortcut(QtGui.QKeySequence("Ctrl+L"), Save_As, activated=log.logging_ui.show).setAutoRepeat(False)

    def show_window(self,dictionary):
        self.dictionary = dictionary
        self.Save_As.show()

    def save_user_state(self):
        log.info("saving state changes...")
        if len(self.lineEdit.text()) == 0:
            msg_box.warning("錯誤", "檔名不能為空")
            return
        else:
            json_object = dumps(self.dictionary, indent = 3)
            save_title = self.lineEdit.text()
            log.info(save_title)
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
        QShortcut(QtGui.QKeySequence("Ctrl+L"), restart_ui, activated=log.logging_ui.show).setAutoRepeat(False)

    def reload(self):
        execlp(sys.executable, sys.executable, *sys.argv)
        
    def close_window(self):
        self.restart_ui.destroy()

class msg_window(QWidget):
    def information(self,title:str,message):
        message = str(message)
        QMessageBox.information(self,title,message)

    def warning(self,title:str,message):
        log.info("錯誤")
        message = str(message)
        QMessageBox.warning(self,title,message)
    

class Ui_logging_ui(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logging_ui = QtWidgets.QWidget()
        self.logging_ui.setObjectName("logging_ui")
        self.logging_ui.resize(500, 600)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.logging_ui)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.logging_ui)
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        QtCore.QMetaObject.connectSlotsByName(self.logging_ui)
        self.logging_ui.move(100, 180)

    def info(self,msg):
        self.plainTextEdit.appendPlainText(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    log = Ui_logging_ui()
    try:
        temp_file = sys._MEIPASS
        icon = QtGui.QIcon(f"{temp_file}/lib/icon.ico")
        QFontDatabase.addApplicationFont(f"{temp_file}/SF-Pro-Display-Regular.otf")
        log.logging_ui.setWindowTitle("discord狀態修改器執行紀錄:用戶模式")
    except:
        icon = QtGui.QIcon("./lib/icon.ico")
        QFontDatabase.addApplicationFont("./lib/SF-Pro-Display-Regular.otf")
        log.logging_ui.show()
        log.logging_ui.setWindowTitle("discord狀態修改器執行紀錄:除錯模式")
    log.info("start discord RPC editor")
    msg_box = msg_window()
    log.info(sys.executable)
    log.info(path.abspath(__file__))
    msg_box.setWindowIcon(icon)
    log.logging_ui.setWindowIcon(icon)
    sleep = QtTest.QTest.qWait
    app.setQuitOnLastWindowClosed(True)
    UI_start_ui()