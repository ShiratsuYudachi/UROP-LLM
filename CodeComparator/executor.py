import subprocess
import threading
import os
import signal
from Utils import *

# 定义一个执行外部命令的函数
timeout = 1

def run_command(cmd):
    global process
    process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    process.communicate()

# 超时处理函数
def timeout_handler():
    colorPrint("Command timed out. Terminating process.","red")
    #process.kill()
    # not working because < and > entails another shell
    
    # 在Unix系统上，可以使用以下方式发送SIGINT（Ctrl-C）信号
    os.killpg(os.getpgid(process.pid), signal.SIGKILL)

# 主程序
def executeInNewThread(command:str):
    #command = "python3 /Users/tsuyue/Documents/GitHub/UROP-LLM/CodeComparator/src.py </Users/tsuyue/Documents/GitHub/UROP-LLM/CodeComparator/test_inputs/input_916e2.txt > /Users/tsuyue/Documents/GitHub/UROP-LLM/CodeComparator/temp_ExecuteResult/src.py.output"
    # 创建并启动一个线程来运行外部命令
    command_thread = threading.Thread(target=run_command, args=(command,))
    command_thread.start()
    # 等待指定的超时时间
    command_thread.join(timeout)

    if command_thread.is_alive():
        # 如果线程仍然活跃，表示命令执行超时
        timeout_handler()
        command_thread.join()  # 等待线程结束
