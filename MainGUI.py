import sys
from PyQt5.QtWidgets import QApplication
from Logic.ConnectorLogic import ConnectorLogic  # 导入逻辑处理类

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 直接实例化逻辑处理类（该类已集成UI）
    mainWindow = ConnectorLogic()
    mainWindow.show()  # 显示窗口

    sys.exit(app.exec_())