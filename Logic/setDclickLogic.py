from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
from GUI import setDclick

class setDclickLogic(QDialog,setDclick.Ui_Dialog):
    send_dclick_signal=pyqtSignal(int,int)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind_events()
    def bind_events(self):
        pass
    def closeEvent(self, a0):
        self.hide()
    def accept(self):
        if not self.dClickXTextEdit.toPlainText() or not self.dClickYTextEdit.toPlainText():
            QMessageBox.warning(self, "输入错误", "请输入数字")
            return
        self.send_dclick_signal.emit(int(self.dClickXTextEdit.toPlainText()),int(self.dClickYTextEdit.toPlainText()))
        super().accept()