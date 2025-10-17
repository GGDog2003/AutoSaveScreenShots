from PyQt5.QtCore import QStringListModel, pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from GUI import MainScreenShotsWindow
from Logic import CodeExcutor
from Logic.ConnectorLogic import ConnectorLogic
from Logic.SleepLogic import SleepLogic


class MainScreenShotsWindowLogic(QMainWindow, MainScreenShotsWindow.Ui_MainScreenShotsWindow):
    raw_code = """#这是控制手机的原始代码
import uiautomator2 as u2
import time
import tqdm
print("正在执行代码.........")
"""
    """截图工具主窗口逻辑处理类"""
    raw_code_indentation = ""

    def __init__(self):
        super().__init__()
        self.sleep_window = None
        self.LogicList = []
        self.PrintList = []  # 新增：存储输出结果的列表
        self.selected_device = None
        self.setupUi(self)
        self._bind_events()

    def _bind_events(self):
        """绑定所有界面事件"""
        # 绑定获取设备信息的槽函数
        self.sleepBtn.clicked.connect(self.handle_sleep)
        self.start_screenshots.clicked.connect(self.handle_execute_code)
        self.dTextBtn.clicked.connect(self.handle_dText)
        self.dClickBtn.clicked.connect(self.handle_dclick)
    def closeEvent(self, a0, QCloseEvent=None):
        """窗口关闭事件处理"""
        # 隐藏当前窗口，显示连接界面
        self.hide()
        self.connectorLogic = ConnectorLogic()
        self.connectorLogic.show()

    def get_selected_device(self, device):
        """获取已选择的设备"""
        self.selected_device = device
        QMessageBox.information(self, "提示", f"您已选择设备：{self.selected_device}")
        self.addRawCode(f"d = u2.connect(\"{self.selected_device}\")")

    def addRawCode(self, newCode,newline=True):
        """添加原始代码"""

        if newline:
            newCode = self.raw_code_indentation + f"\n{newCode}"
        else:
            newCode = self.raw_code_indentation + newCode

        self.raw_code += newCode

    def addScrLogicListView(self, newString):
        self.LogicList.append(newString)
        scrLogicListModel = QStringListModel()
        scrLogicListModel.setStringList(self.LogicList)
        self.scrLogicListView.setModel(scrLogicListModel)

    def handle_sleep(self):
        """打开睡眠窗口，并绑定信号接收"""
        self.sleep_window = SleepLogic()
        # 绑定睡眠窗口的信号到主窗口的处理函数
        self.sleep_window.send_sleep_time_signal.connect(self.on_receive_sleep_time)
        self.sleep_window.show()

    @pyqtSlot(str)  # 标记为槽函数，接收睡眠时间
    def on_receive_sleep_time(self, sleep_time):
        """处理从睡眠窗口接收的时间数据"""
        # 示例1：添加到逻辑列表显示
        self.addScrLogicListView(f"睡眠 {sleep_time} 秒")
        # 示例2：生成对应的控制代码（如uiautomator2的sleep命令）
        self.addRawCode(f"time.sleep({sleep_time})")

        # 可根据需求扩展其他处理逻辑

    def handle_execute_code(self):
        """执行代码并接收输出结果"""
        # 调用CodeExcutor，传入输出回调函数
        CodeExcutor.execute_code(self.raw_code, self.handle_output)

    def handle_output(self, output):
        """处理代码执行的输出结果，更新printListView"""
        # 将输出按行分割，避免列表项过长
        output_lines = output.splitlines()
        self.PrintList.extend(output_lines)  # 添加到输出列表

        # 更新ListView显示
        print_model = QStringListModel()
        print_model.setStringList(self.PrintList)
        self.printListView.setModel(print_model)

        # 滚动到最后一行
        if self.PrintList:
            index = print_model.index(len(self.PrintList) - 1)
            # self.printListView.scrollTo(index, Qt)
    def handle_dText(self):
        from  Logic.setDtextLogic import setDtextLogic
        self.setDtext_window=setDtextLogic()
        self.setDtext_window.send_dtext_signal.connect(self.on_receive_dtext)
        self.setDtext_window.show()
    def on_receive_dtext(self,dtext,radio_checked):
        """处理从setDtext_window接收的dtext数据"""
        if radio_checked==0:
            self.addScrLogicListView(f"点击文本：{dtext}")
            self.addRawCode(f"d(text=\"{dtext}\").click()")
        elif radio_checked==1:
            self.addScrLogicListView(f"判断文本存在：{dtext}")
            self.addRawCode(f" d(text=\"{dtext}\").exist()",newline=False)
        elif radio_checked==2:
            self.addScrLogicListView(f"判断文本不存在：{dtext}")
            self.addRawCode(f" d(text=\"{dtext}\").exist==False",newline=False)
        return
    def handle_dclick(self):
        from  Logic.setDclickLogic import setDclickLogic
        self.setDclick_window=setDclickLogic()
        self.setDclick_window.send_dclick_signal.connect(self.on_receive_dclick)
        self.setDclick_window.show()
    def on_receive_dclick(self,dclickX,dclickY):
        """处理从setDclick_window接收的dclick数据"""
        self.addScrLogicListView(f"点击坐标：({dclickX},{dclickY})")
        self.addRawCode(f"d.click({dclickX},{dclickY})")
        return
if __name__ == "__main__":
    import sys
    # 创建独立的应用实例
    app = QApplication(sys.argv)
    # 直接实例化当前窗口，无需启动主程序
    window = MainScreenShotsWindowLogic()
    # 显示窗口
    window.show()
    # 运行事件循环
    sys.exit(app.exec_())
