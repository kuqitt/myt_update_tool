import json
import logging
import os
import socket
import time
import webbrowser

from flask import Flask, render_template, jsonify, request
import threading
from collections import deque
from mytapi import MytAPI
from ssh_operator import SSHMytOperator
from logger_util import add_log, get_logs as fetch_logs
import init
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,
            static_folder=os.path.join(base_dir, 'static'),
            template_folder=os.path.join(base_dir, 'templates'))


CONFIG_PATH = 'config.json'

def save_credentials(user, password):
    with open(CONFIG_PATH, 'w') as f:
        json.dump({'user': user, 'password': password}, f)

def load_credentials():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return None


@app.route('/')
def index():
    add_log("[INFO] 用户访问主页")
    return render_template('index.html')

@app.route('/api/credentials')
def get_saved_credentials():
    creds = load_credentials()
    if creds:
        return jsonify(creds)
    else:
        return jsonify({})
@app.route('/get_logs')
def get_logs():
    return jsonify(fetch_logs())
@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/api/login', methods=['POST'])
def api_login():
    user = request.form.get('user')
    password = request.form.get('password')
    result = MytAPI.login(user, password)
    if result and result.get('code') == 200:
        save_credentials(user, password)
        return jsonify({"code": 200, "token": result.get('data')})
    else:
        return jsonify({"code": 500, "message": "登录失败"})

@app.route('/start_task', methods=['POST'])
def start_task():
    devices = request.form.getlist('devices[]')
    token = request.form.get('token')
    if not token:
        add_log("[WARN] 未登录或token缺失")
        return jsonify({"code": 401, "message": "未登录或token缺失"})

    if not devices:
        add_log("[WARN] 启动任务失败，未选择设备")
        return jsonify({"code": 400, "message": "请选择设备"})
    add_log(f"[TASK] 任务启动，设备列表: {devices}")
    # 这里可以启动后台线程处理任务（示例）
    def task_simulator(dev_list):
        for i, dev in enumerate(dev_list, 1):
            add_log(f"[TASK] 正在处理设备 {dev} ({i}/{len(dev_list)})")
            sshClass = SSHMytOperator(dev)
            sshClass.login()
            sshClass.update_myt_token(token)
        add_log("[TASK] 任务完成")
    threading.Thread(target=task_simulator, args=(devices,), daemon=True).start()
    return jsonify({"code": 200, "message": "任务已开始", "devices": devices})

@app.route('/api/device/list')
def device_list():
    add_log("[INFO] 设备列表请求")
    result = MytAPI.query_myt()
    add_log(f"[INFO] 返回设备列表: {list(result.get('data', {}).keys())}")
    return jsonify(result)
def find_free_port(start_port=5000, max_port=5100):
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                add_log(f"[INFO] 找到可用端口: {port}")
                return port
    add_log("[ERROR] 找不到可用端口")
    raise RuntimeError("找不到可用端口")

import webview
flask_port = None

def start_flask():
    global flask_port
    # 初始化myt_sdk
    init.check_sdk()
    init.start_sdk()
    flask_port = find_free_port(5001)
    add_log(f"[INFO] Flask 服务启动于端口: {flask_port}")
    app.run(port=flask_port)

def wait_flask_ready_and_load_main():
    global flask_port
    while flask_port is None:
        time.sleep(0.1)
    logging.info("Flask 启动完成，准备加载主页面")
    # 使用主窗口加载主页面URL，避免销毁重建
    main_url = f"http://127.0.0.1:{flask_port}"
    # 通过主线程调用load_url安全更新
    window = webview.windows[0]
    window.load_url(main_url)
    window.set_title("设备监控")
    window.resize(800, 600)  # 调整到需要的尺寸

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 创建初始化窗口
    init_html = '<h2 style="text-align:center;margin-top:30px;">初始化启动中，请稍候...</h2>'
    window = webview.create_window('初始化', html=init_html, width=300, height=120)

    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    wait_thread = threading.Thread(target=wait_flask_ready_and_load_main, daemon=True)
    wait_thread.start()

    webview.start()
    logging.info("窗口关闭，停止SDK")
    init.stop_sdk()