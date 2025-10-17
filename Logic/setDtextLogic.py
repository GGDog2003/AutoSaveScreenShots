from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from GUI import setDtext

class setDtextLogic(QDialog,setDtext.Ui_Dialog):
    send_dtext_signal=pyqtSignal(str,int)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind_events()
        #设置默认radio_button选中
        self.dTextClickRadioBtn.setChecked(True)

    def bind_events(self):
        pass
    def closeEvent(self, a0, QCloseEvent=None):
        """窗口关闭事件处理"""
        # 显示连接界面
        self.hide()
    def accept(self):
        """执行自定义逻辑后关闭窗口"""
        radio_checked=-1
        self.dTextClickRadioBtn = self.dTextClickRadioBtn.isChecked()
        self.dTextExistRadioBtn = self.dTextExistRadioBtn.isChecked()
        self.dTextNotExistRadioBtn = self.dTextNotExistRadioBtn.isChecked()
        if self.dTextClickRadioBtn:
            radio_checked=0
        elif self.dTextExistRadioBtn:
            radio_checked=1
        elif self.dTextNotExistRadioBtn:
            radio_checked=2
        self.send_dtext_signal.emit(self.DtextEdit.toPlainText(),radio_checked)
        super().accept()