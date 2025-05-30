# 魔云腾令牌刷新工具

魔云腾令牌刷新工具是一个基于 Python 的桌面应用程序，提供图形化界面，用于批量监控设备状态并刷新设备令牌（Token）。该工具集成了 Flask + PyWebview，适合企业或运维人员对接入设备进行集中管理与控制。

## ✨ 功能亮点

- 🧠 自动检测可用端口并启动内嵌 Flask 服务
- 🖥️ 使用 PyWebview 嵌入网页为桌面 GUI
- 🔍 支持 IP 搜索筛选设备
- ✅ 一键全选 / 取消选择设备
- 🔐 登录信息自动保存，二次启动自动填充
- 📋 实时日志输出窗口
- 🚪 程序关闭时自动释放 SDK
- 🗂️ 支持打包为单个 EXE 文件，带图标、无命令行窗口
- ⚠️ 打包为 EXE 后默认请求管理员权限运行

## 📁 项目结构

```
mytupdatetoken/
├── app.py                # 主程序入口
├── init.py               # SDK 初始化与释放逻辑
├── templates/
│   └── index.html        # 前端界面模板
├── static/               # 静态资源文件（JS/CSS）
├── app.spec              # PyInstaller 打包配置文件
└── README.md             # 项目说明文件
```

## 🚀 启动方式

```bash
python app.py
```

## 🛠 打包说明

推荐使用 PyInstaller 进行打包：

```bash
pyinstaller app.spec
```

## 📌 注意事项

- 程序需要以管理员权限运行
- 建议安装 WebView2 运行时以确保最佳兼容性
- 打包时建议图标命名为 `icon.ico` 并放在项目根目录

## 📬 联系方式

如有任何问题或建议，请联系作者。
