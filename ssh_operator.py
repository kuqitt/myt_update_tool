import paramiko
import time
from logger_util import add_log

class SSHMytOperator:
    def __init__(self, ip, username='user', password='myt', su_password='myt', timeout=10):
        self.ip = ip
        self.username = username
        self.password = password
        self.su_password = su_password
        self.timeout = timeout
        self.client = None
        self.shell = None
        add_log(f"[{ip}] 初始化 SSH 连接对象")

    def login(self):
        try:
            add_log(f"[{self.ip}] 尝试登录 SSH")
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip, username=self.username, password=self.password, timeout=self.timeout)

            self.shell = self.client.invoke_shell()
            time.sleep(1)
            self._clear_buffer()

            add_log(f"[{self.ip}] 登录成功，尝试切换 su 用户")
            self._send_command('su -')
            time.sleep(1)
            self._send_command(self.su_password)
            time.sleep(1)
            self._clear_buffer()
            add_log(f"[{self.ip}] 已切换到 root 用户")
            return True
        except Exception as e:
            add_log(f"[{self.ip}] SSH 登录失败: {e}")
            return False

    def _send_command(self, cmd):
        if self.shell:
            add_log(f"[{self.ip}] 执行命令: {cmd}")
            self.shell.send(cmd + '\n')

    def _clear_buffer(self):
        if self.shell and self.shell.recv_ready():
            output = self.shell.recv(65535).decode('utf-8')
            add_log(f"[{self.ip}] 命令输出: {output.strip()}")
            return output
        return ''

    def update_myt_token(self, token):
        if not self.shell:
            raise RuntimeError("Shell未建立连接，请先调用login()")
        add_log(f"[{self.ip}] 开始更新 token: {token}")
        self._send_command(f"getinfo -token {token}")
        time.sleep(1)
        self._clear_buffer()

        self._send_command("reboot&")
        time.sleep(1)
        self._clear_buffer()
        add_log(f"[{self.ip}] 更新完成，已执行重启命令")
        return True

    def close(self):
        if self.client:
            add_log(f"[{self.ip}] 关闭 SSH 连接")
            self.client.close()
            self.client = None
            self.shell = None
