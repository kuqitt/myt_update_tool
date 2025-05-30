# 初始化 检测sdk是否存在,不存在则下载
import os
import time

import requests
import zipfile
import shutil
import subprocess
import platform
import psutil
from logger_util import add_log

# 创建一个public文件夹，用于存放公共文件
if not os.path.exists('public'):
    os.makedirs('public')

def check_sdk():
    """
    检查SDK是否存在，不存在则下载
    """
    sdk_path = 'public/myt_sdk'
    if not os.path.exists(sdk_path):
        add_log('sdk不存在，正在下载...')
        url = 'http://d.moyunteng.com/sdk/myt_sdk_1.0.14.30.20.zip'
        response = requests.get(url)

        # 确保public目录存在
        os.makedirs('public', exist_ok=True)

        zip_path = 'public/myt_sdk_1.0.14.30.20.zip'
        with open(zip_path, 'wb') as f:
            f.write(response.content)

        # 解压到临时目录
        temp_extract_path = 'public/temp_sdk'
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_path)

        # 删除zip文件
        os.remove(zip_path)

        # 找到解压目录中实际的文件夹（通常只有一个）
        extracted_items = os.listdir(temp_extract_path)
        if len(extracted_items) == 1:
            extracted_folder = os.path.join(temp_extract_path, extracted_items[0])
            shutil.move(extracted_folder, sdk_path)
        else:
            # 如果有多个项目，也统一放入myt_sdk目录
            os.makedirs(sdk_path, exist_ok=True)
            for item in extracted_items:
                shutil.move(os.path.join(temp_extract_path, item), sdk_path)

        # 清理临时目录
        shutil.rmtree(temp_extract_path)

        add_log('sdk下载完成')
    else:
        add_log('sdk已存在')


def start_sdk():
    """
    启动 SDK 进程
    """
    # 仅允许 Windows 启动
    if platform.system() != 'Windows':
        print("只支持在 Windows 系统上启动 SDK")
        return

    sdk_path = 'public/myt_sdk'
    sdk_exe = os.path.join(sdk_path, 'myt_sdk.exe')

    if not os.path.exists(sdk_exe):
        print("myt_sdk.exe 未找到")
        return

    # 检查是否已在运行
    for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
        try:
            if 'myt_sdk.exe' in proc.info['name'].lower():
                print("SDK已在运行，跳过启动")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # 启动进程，不显示控制台窗口
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(
        sdk_exe,
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    time.sleep(2)
    add_log('SDK已启动')

def stop_sdk():
    """
    停止 SDK 进程
    """
    # 仅允许 Windows 停止
    if platform.system() != 'Windows':
        print("只支持在 Windows 系统上停止 SDK")
        return

    # 查找并终止进程
    for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
        try:
            if'myt_sdk.exe' in proc.info['name'].lower():
                proc.terminate()
                proc.wait()


        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    add_log('SDK已停止')
