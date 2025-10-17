from PyQt5.QtCore import QStringListModel, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QApplication
from GUI import sleep



class SleepLogic(QDialog,sleep.Ui_Dialog):
    send_sleep_time_signal=pyqtSignal(str)
    """睡眠界面逻辑处理类"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    #     self.bind_events()
    # def bind_events(self):
    #     pass
    def closeEvent(self, a0, QCloseEvent=None):
        """窗口关闭事件处理"""
        # 显示连接界面
        self.hide()
    # 可选：重写accept方法，自定义"确定"按钮逻辑
    def accept(self):
        # 执行自定义逻辑后关闭窗口
        self.sleepTime=self.setSleepTimeTextEdit.toPlainText()
        if self.sleepTime:
            if not self.sleepTime.isnumeric():
                QMessageBox.warning(self, "输入错误", "请输入数字")
                return

        else:
            QMessageBox.warning(self, "输入错误", "请输入数字")
        #发送数据给主窗口
        self.send_sleep_time_signal.emit(self.sleepTime)


        super().accept()  # 调用父类QDialog的accept方法关闭窗口
    # 可选：重写reject方法，自定义"取消"按钮逻辑
    def reject(self):
        print("点击了取消按钮")
        super().reject()  # 调用父类QDialog的reject方法关闭窗口
# ---------------------- 单页面测试入口 ----------------------
if __name__ == "__main__":
    import sys
    # 创建独立的应用实例
    app = QApplication(sys.argv)
    # 直接实例化当前窗口，无需启动主程序
    window = SleepLogic()
    # 显示窗口
    window.show()
    # 运行事件循环
    sys.exit(app.exec_())