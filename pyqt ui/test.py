
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QMessageBox, QPushButton,
                             QLabel, QCheckBox, QComboBox, QLineEdit, QSpinBox,
                             QMenu, QAction, QGridLayout, QHBoxLayout, QVBoxLayout,
                             QTextEdit,QGroupBox, QStyle, QSystemTrayIcon)
 
class SystemTrayDemo(QDialog):
    def __init__(self):
        super(SystemTrayDemo, self).__init__()
        
        # 设置窗口标题
        self.setWindowTitle('实战PyQt5: 演示应用最小化到托盘')
        
        #设置窗口尺寸
        self.resize(400, 300)
        
        self.sysIcon = QIcon(':/panda.png')
        self.setWindowIcon(self.sysIcon)
        
        self.initUi()
        
    def initUi(self):
        
        self.createMessageGroupBox()
        self.createTrayIcon()
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.grpMessageBox)
        self.setLayout(mainLayout)
        
        #让托盘图标显示在系统托盘上
        self.trayIcon.show()
        
    #创建托盘图标
    def createTrayIcon(self):
        aRestore = QAction('恢复(&R)', self, triggered = self.showNormal)
        aQuit = QAction('退出(&Q)', self, triggered = QApplication.instance().quit)
        
        menu = QMenu(self)
        menu.addAction(aRestore)
        menu.addAction(aQuit)
        
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.sysIcon)
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.activated.connect(self.iconActivated)
    
    #气球信息控制部分
    def createMessageGroupBox(self):
        self.grpMessageBox = QGroupBox('气球消息')
        
        #==== 消息类型控制部分 ====#
        typeLabel = QLabel('消息类型:')
        
        self.cmbType = QComboBox()
        self.cmbType.addItem('无类型', QSystemTrayIcon.NoIcon)
        self.cmbType.addItem(self.style().standardIcon(QStyle.SP_MessageBoxInformation), 
                             '信息', QSystemTrayIcon.Information)
        self.cmbType.addItem(self.style().standardIcon(QStyle.SP_MessageBoxWarning),
                             '警告', QSystemTrayIcon.Warning)
        self.cmbType.addItem(self.style().standardIcon(QStyle.SP_MessageBoxCritical),
                             '错误', QSystemTrayIcon.Critical)
        self.cmbType.setCurrentIndex(1)
        
        #==== 消息显示持续时间部分 ====#
        durationLabel = QLabel('持续时间:')
        
        self.durationSpinBox = QSpinBox()
        self.durationSpinBox.setRange(5, 60)    #时间范围
        self.durationSpinBox.setSuffix(' s')    #后缀，秒
        self.durationSpinBox.setValue(15)       # 缺省时间 15秒
        
        #spinbox 右边的警告提示信息
        durationWarningLabel = QLabel('(一些系统可能会忽略消息显示的持续时间控制)')
        durationWarningLabel.setIndent(10)
        
        #==== 消息标题栏控制 ====#
        titleLabel = QLabel('标题:')
        
        self.titleEdit = QLineEdit('不能连接到网络')
        
        #==== 消息编辑栏 ====#
        bodyLabel = QLabel('消息:')
        self.bodyEdit = QTextEdit()
        self.bodyEdit.setPlainText('不要问我, 老实说吧，我也不知道原因。'
                                   '\n请点击气球图标获得更多信息')
        
        #==== 显示消息按钮 ====#
        showMessageButton = QPushButton('显示消息')
        showMessageButton.setDefault(True)
        showMessageButton.clicked.connect(self.showMessage)
        
        #==== 将上述部件加入到一个网格布局中
        msgLayout = QGridLayout()
        msgLayout.addWidget(typeLabel, 0, 0)     #0行0列
        msgLayout.addWidget(self.cmbType, 0, 1, 1, 2)    #0行1列, 占1行2列
        msgLayout.addWidget(durationLabel, 1, 0)    #1行0列
        msgLayout.addWidget(self.durationSpinBox, 1, 1)     #1行1列
        msgLayout.addWidget(durationWarningLabel, 1, 2, 1, 3)  #1行2列, 占1行3列
        msgLayout.addWidget(titleLabel, 2, 0)     #2行0列
        msgLayout.addWidget(self.titleEdit, 2, 1, 1, 4)  #2行1列, 占1行4列
        msgLayout.addWidget(bodyLabel, 3, 0)     #3行0列
        msgLayout.addWidget(self.bodyEdit, 3, 1, 2, 4)  #3行1列, 占2行4列
        msgLayout.addWidget(showMessageButton, 5, 4) #5行4列
        msgLayout.setColumnStretch(3, 1)
        msgLayout.setRowStretch(4, 1)
        
        self.grpMessageBox.setLayout(msgLayout)
     
    #显示气球信息   
    def showMessage(self):
        #根据消息类型获取图标
        icon = QSystemTrayIcon.MessageIcon(self.cmbType.itemData(self.cmbType.currentIndex()))
        self.trayIcon.showMessage(self.titleEdit.text(),         #标题
                                  self.bodyEdit.toPlainText(),   #信息
                                  icon,                          #图标
                                  self.durationSpinBox.value() * 1000) #信息显示持续时间
    
    #关闭事件处理, 不关闭，只是隐藏，真正的关闭操作在托盘图标菜单里
    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QMessageBox.information(self, '系统托盘', 
                                    '程序将继续在系统托盘中运行，要终止本程序，\n'
                                    '请在系统托盘入口的上下文菜单中选择"退出"')
            self.hide()
            event.ignore()
    
    def messageClicked(self):
        QMessageBox.information(None, '系统托盘',
                                '对不起，我已经尽力了。'
                                '也许你应该试着问一个人?')
     
       
    def iconActivated(self, reason):
        if reason in (QSystemTrayIcon.DoubleClick, QSystemTrayIcon.MiddleClick):
            self.showMessage()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    #如果系统不支持最小化到托盘
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, '系统托盘', '本系统不支持托盘功能')
        sys.exit(1)
        
    QApplication.setQuitOnLastWindowClosed(False)
    
    window = SystemTrayDemo()
    window.show()
    sys.exit(app.exec())