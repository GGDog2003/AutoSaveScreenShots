# ui_logic.py：处理界面交互逻辑
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QStringListModel, QTimer, pyqtSignal, QSettings
import subprocess
from GUI import Connector
import os
import time
class ConnectorLogic(QMainWindow, Connector.Ui_MainWindow):
    send_selected_device_signal=pyqtSignal(str)
    """连接手机界面的逻辑处理类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化界面布局
        self.setupUi(self)

        # 设置默认IP和端口提示
        self.connectIp.setPlaceholderText("例如: 192.168.1.100:5555")

        # 绑定事件
        self._bind_events()

        # 初始化状态
        self.connection_status = False

        self.init_list_connected_devices_timer()

        self.get_saved_ip_port()

    def get_saved_ip_port(self):
        """获取保存的IP和端口"""
        self.settings = QSettings("connect_ip.ini", QSettings.Format.IniFormat)
        ip_port = self.settings.value("ip_port")
        if ip_port:
            self.connectIp.setText(self.settings.value("ip_port"))



    def init_list_connected_devices_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.list_connected_devices)
        self.timer.setInterval(2000)
        self.timer.start()
    def _bind_events(self):
        """绑定所有界面事件"""
        # 连接按钮点击事件
        self.connectBtn.clicked.connect(self.handle_connect)
        # 列表点击事件
        self.listView.clicked.connect(self.list_connected_devices_click)


    def handle_connect(self):
        """处理连接逻辑"""
        # 获取输入的IP和端口
        ip_port = self.connectIp.toPlainText().strip()
        #用QSetting保存当前ip到ini配置文件
        self.settings = QSettings("connect_ip.ini", QSettings.Format.IniFormat)

        if self.settings.value("ip_port")==ip_port:
            print("已保存的ip")
            # 显示到界面
            self.connectIp.setText(self.settings.value("ip_port"))
        else:
            print("未保存的ip")
        self.settings.setValue("ip_port", ip_port)
        # 验证输入
        if not ip_port:
            QMessageBox.warning(self, "输入错误", "请输入IP和端口号")
            return

        if ":" not in ip_port:
            QMessageBox.warning(self, "格式错误", "请使用正确格式: IP:端口")
            return

        # 尝试连接
        if self._adb_connect(ip_port):
            self.connection_status = True
            QMessageBox.information(self, "连接成功", f"已成功连接到 {ip_port}")

        else:
            self.connection_status = False


    def _adb_connect(self, ip_port):

        """执行ADB连接命令"""
        #拿到当前目录/adb路径
        adb_path=os.path.join(os.getcwd(),"adb","adb.exe")
        print(adb_path)
        try:
            # 执行adb连接命令
            result = subprocess.run(
                [adb_path, "connect", ip_port],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10
            )


            # 检查命令执行结果
            if "connected to" in result.stdout:
                return True
            else:
                QMessageBox.critical(self, "连接失败", f"无法连接到 {ip_port}\n错误信息:\n{result.stdout}")
                print(f"ADB连接失败: {result.stdout}")
                return False

        except FileNotFoundError:
            QMessageBox.critical(self, "错误", "未找到ADB工具，请确保ADB已添加到系统PATH中")
            return False
        except Exception as e:
            QMessageBox.critical(self, "错误", f"连接过程中发生错误: {str(e)}")
            return False

    def closeEvent(self, event):
        """窗口关闭事件处理"""
        if self.connection_status:
            event.accept()  # 允许关闭
        else:
            # 如果未连接成功，提示用户
            reply = QMessageBox.question(
                self, "确认关闭",
                "尚未成功连接手机，确定要关闭吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
    def list_connected_devices(self):
        """列出已连接的设备"""
        adb_path=os.path.join(os.getcwd(),"adb","adb.exe")
        try:

            result=subprocess.run(
                [adb_path,"devices"],
                capture_output=True,
                text=True,
                timeout=10
            )
            devices=[]

            for line in result.stdout.splitlines()[1:]:
                if "device" in line:
                    devices.append(line.split()[0])
            # 关键：将设备列表保存到实例变量，供点击事件使用
            self.devices=devices
            #显示到列表中
            devicesListModel = QStringListModel()
            devicesListModel.setStringList(devices)
            self.listView.setModel(devicesListModel)
            # 双击列表项跳转


        except Exception as e:
            QMessageBox.critical(self, "错误", f"列出已连接设备时发生错误: {str(e)}")
            return []
    def list_connected_devices_click(self,index):
        """处理列表项点击事件"""
        if 0 <= index.row() < len(self.devices):
            self.selected_device = self.devices[index.row()]
            print(f"点击了设备：{self.selected_device}")


            # 关闭当前窗口


            # 创建并显示截图工具界面，同时传递选中的设备信息
            # 假设你的截图工具类名为 ScreenshotTool
            from Logic.MainScreenShotsWindowLogic import MainScreenShotsWindowLogic  # 导入截图工具类
            self.mainWindow=MainScreenShotsWindowLogic()

            self.send_selected_device_signal.connect(self.mainWindow.get_selected_device)
             # 发射信号（此时主窗口已准备好接收）
            self.send_selected_device_signal.emit(self.selected_device)
            self.mainWindow.show()
            self.hide()
            # self.screenshot_window.show()  # 显示新窗口
        else:
            QMessageBox.warning(self, "提示", "无效的设备选择")