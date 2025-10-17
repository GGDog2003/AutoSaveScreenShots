# Logic/CodeExcutor.py
import traceback
import sys
from io import StringIO

def execute_code(code, output_callback):
    """执行代码并通过回调返回输出结果"""
    if not code.strip():
        output_callback("错误: 没有输入任何代码")
        return

    try:
        # 保存原始stdout
        original_stdout = sys.stdout
        # 捕获输出
        sys.stdout = captured_output = StringIO()

        # 执行代码
        exec(code, globals())

        # 恢复stdout
        sys.stdout = original_stdout

        # 获取输出并通过回调返回
        output = captured_output.getvalue()
        if output:
            output_callback(output)
        else:
            output_callback("代码执行成功，但没有输出结果")

    except Exception as e:
        # 恢复stdout
        sys.stdout = sys.__stdout__
        # 捕获错误信息
        error_msg = traceback.format_exc()
        output_callback(f"执行错误:\n{error_msg}")