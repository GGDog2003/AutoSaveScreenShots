from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
from GUI import setDswipe

class setDclickLogic(QDialog,setDswipe.Ui_Dialog):
    send_dswipe_signal=pyqtSignal(int,int,int,int)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind_events()
    def bind_events(self):
        pass
    def closeEvent(self, a0):
        self.hide()
    def accept(self):
        #判断是否全都是数字
        if not self.setFxTextEdit.toPlainText().isdigit() or not self.setFyTextEdit.toPlainText().isdigit() or not self.setTxTextEdit.toPlainText().isdigit() or not self.setTyTextEdit.toPlainText().isdigit():
            QMessageBox.warning(self, "错误", "请输入数字")
            return
        self.send_dswipe_signal.emit(int(self.setFxTextEdit.toPlainText()),int(self.setFyTextEdit.toPlainText()),int(self.setTxTextEdit.toPlainText()),int(self.setTyTextEdit.toPlainText()))
        super().accept()