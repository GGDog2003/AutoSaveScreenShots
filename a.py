import sys
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QWidget, QSplitter, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor

class CodeExecutor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle("Python代码执行器")
        self.setGeometry(100, 100, 1000, 700)

        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 创建分割器，用于分隔代码区和输出区
        splitter = QSplitter(Qt.Vertical)

        # 代码编辑区域
        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText("在这里编写Python代码...")
        # 设置等宽字体，适合代码编辑
        font = QFont("Consolas", 10)
        self.code_editor.setFont(font)
        splitter.addWidget(self.code_editor)

        # 输出显示区域
        output_label = QLabel("执行输出:")
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)  # 设为只读
        self.output_display.setFont(font)

        # 输出区域布局
        output_layout = QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_display)

        output_widget = QWidget()
        output_widget.setLayout(output_layout)
        splitter.addWidget(output_widget)

        # 设置分割器初始大小比例
        splitter.setSizes([400, 300])

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.run_btn = QPushButton("执行代码")
        self.run_btn.clicked.connect(self.execute_code)
        self.run_btn.setStyleSheet("padding: 8px 16px; font-size: 14px;")

        self.clear_btn = QPushButton("清空代码")
        self.clear_btn.clicked.connect(self.clear_code)

        self.clear_output_btn = QPushButton("清空输出")
        self.clear_output_btn.clicked.connect(self.clear_output)

        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.clear_output_btn)

        # 添加部件到主布局
        main_layout.addWidget(splitter)
        main_layout.addLayout(btn_layout)

        # 添加示例代码
        self.add_example_code()

    def add_example_code(self):
        """添加示例代码到编辑区"""
        example_code = """# 这是一段示例代码
import math

def calculate_circle_area(radius):
    return math.pi * radius **2

# 测试代码
radius = 5
area = calculate_circle_area(radius)
print(f"半径为{radius}的圆面积是: {area:.2f}")

# 循环示例
for i in range(3):
    print(f"循环输出: {i}")
"""
        self.code_editor.setText(example_code)

    def execute_code(self):
        """执行编辑区中的代码"""
        # 清空之前的输出
        self.clear_output()

        # 获取编辑区的代码
        code = self.code_editor.toPlainText()

        if not code.strip():
            self.append_output("错误: 没有输入任何代码")
            return

        try:
            # 重定向标准输出到输出区
            import sys
            from io import StringIO

            # 保存原始的stdout
            original_stdout = sys.stdout
            # 创建一个StringIO对象来捕获输出
            sys.stdout = captured_output = StringIO()

            # 执行代码
            exec(code, globals())

            # 恢复原始的stdout
            sys.stdout = original_stdout

            # 获取捕获的输出并显示
            output = captured_output.getvalue()
            if output:
                self.append_output(output)
            else:
                self.append_output("代码执行成功，但没有输出结果")

        except Exception as e:
            # 恢复原始的stdout
            sys.stdout = sys.__stdout__
            # 捕获并显示错误信息
            error_msg = traceback.format_exc()
            self.append_output(f"执行错误:\n{error_msg}")

    def append_output(self, text):
        """向输出区添加文本"""
        self.output_display.append(text)
        # 滚动到最后一行
        cursor = self.output_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.output_display.setTextCursor(cursor)

    def clear_code(self):
        """清空代码编辑区"""
        self.code_editor.clear()

    def clear_output(self):
        """清空输出区"""
        self.output_display.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeExecutor()
    window.show()
    sys.exit(app.exec_())
