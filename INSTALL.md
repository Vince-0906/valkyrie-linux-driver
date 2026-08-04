# Installation Guide | 安装指南

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## English Installation Guide

### Prerequisites

- Linux system (tested on Ubuntu 22.04, should work on most distributions)
- Python 3.6 or higher
- USB access (either root privileges or udev rules)
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Vince-0906/valkyrie-linux-driver.git
cd valkyrie-linux-driver
```

### Step 2: Setup Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Python Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install hidapi
```

For GUI support, install the system WebView runtime (usually preinstalled on GNOME desktops):
```bash
# Ubuntu/Debian
sudo apt install libwebkit2gtk-4.1-0 python3-gi

# Fedora
sudo dnf install webkit2gtk4.1 python3-gobject

# Arch Linux
sudo pacman -S webkit2gtk-4.1 python-gobject
```

If your venv cannot `import gi` (venvs created without system site packages),
link the system module into the venv:
```bash
ln -s /usr/lib/python3/dist-packages/gi venv/lib/python3.12/site-packages/gi
```

### Step 4: Setup USB Permissions (Recommended)

To use the driver without root privileges, install the udev rules:

```bash
# Copy udev rules
sudo cp 99-valkyrie.rules /etc/udev/rules.d/

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Add your user to plugdev group (if needed)
sudo usermod -a -G plugdev $USER

# Log out and log back in for group changes to take effect
```

### Step 5: Verify Installation

Check if the device is detected:

```bash
lsusb | grep 0416:5201
```

You should see output like:
```
Bus 001 Device 005: ID 0416:5201 Nuvoton Technology Corp.
```

### Step 6: Test the Driver

```bash
# Activate virtual environment (if you created one)
source venv/bin/activate

# Test CLI
./valkyrie.py status

# Test GUI
./valkyrie_app.py
```

### Troubleshooting

**Error: "Cannot open device"**
- Ensure the device is plugged in: `lsusb | grep 0416:5201`
- Check udev rules are installed: `ls /etc/udev/rules.d/99-valkyrie.rules`
- Try running with sudo: `sudo ./valkyrie.py status`
- Verify you're in the plugdev group: `groups | grep plugdev`

**Error: "No module named 'hid'"**
- Install hidapi: `pip install hidapi`

**GUI doesn't start**
- Ensure WebKit2GTK and PyGObject are installed: `python3 -c "import gi; gi.require_version('WebKit2','4.1')"`
- If the venv cannot import gi, link it: `ln -s /usr/lib/python3/dist-packages/gi venv/lib/python3.12/site-packages/gi`
- Check for errors: `python3 valkyrie_app.py`

### Uninstallation

```bash
# Remove udev rules
sudo rm /etc/udev/rules.d/99-valkyrie.rules
sudo udevadm control --reload-rules

# Remove Python packages
pip uninstall hidapi

# Delete repository
cd ..
rm -rf valkyrie-linux-driver
```

---

<a name="chinese"></a>

## 中文安装指南

### 前置要求

- Linux 系统（在 Ubuntu 22.04 上测试，应该在大多数发行版上工作）
- Python 3.6 或更高版本
- USB 访问权限（root 权限或 udev 规则）
- Git（用于克隆仓库）

### 步骤 1：克隆仓库

```bash
git clone https://github.com/Vince-0906/valkyrie-linux-driver.git
cd valkyrie-linux-driver
```

### 步骤 2：设置虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

### 步骤 3：安装 Python 依赖

使用 pip：
```bash
pip install -r requirements.txt
```

或单独安装：
```bash
pip install hidapi
```

对于 GUI 支持，安装系统 WebView 运行时（GNOME 桌面通常已预装）：
```bash
# Ubuntu/Debian
sudo apt install libwebkit2gtk-4.1-0 python3-gi

# Fedora
sudo dnf install webkit2gtk4.1 python3-gobject

# Arch Linux
sudo pacman -S webkit2gtk-4.1 python-gobject
```

如果您的 venv 无法 `import gi`（venv 创建时未包含系统站点包），
请将系统模块链接到 venv 中：
```bash
ln -s /usr/lib/python3/dist-packages/gi venv/lib/python3.12/site-packages/gi
```

### 步骤 4：设置 USB 权限（推荐）

要在没有 root 权限的情况下使用驱动程序，请安装 udev 规则：

```bash
# 复制 udev 规则
sudo cp 99-valkyrie.rules /etc/udev/rules.d/

# 重新加载 udev 规则
sudo udevadm control --reload-rules
sudo udevadm trigger

# 将您的用户添加到 plugdev 组（如果需要）
sudo usermod -a -G plugdev $USER

# 注销并重新登录以使组更改生效
```

### 步骤 5：验证安装

检查设备是否被检测到：

```bash
lsusb | grep 0416:5201
```

您应该看到类似的输出：
```
Bus 001 Device 005: ID 0416:5201 Nuvoton Technology Corp.
```

### 步骤 6：测试驱动程序

```bash
# 激活虚拟环境（如果您创建了）
source venv/bin/activate

# 测试命令行工具
./valkyrie.py status

# 测试图形界面
./valkyrie_app.py
```

### 故障排除

**错误："无法打开设备"**
- 确保设备已插入：`lsusb | grep 0416:5201`
- 检查 udev 规则是否已安装：`ls /etc/udev/rules.d/99-valkyrie.rules`
- 尝试使用 sudo 运行：`sudo ./valkyrie.py status`
- 验证您是否在 plugdev 组中：`groups | grep plugdev`

**错误："没有名为 'hid' 的模块"**
- 安装 hidapi：`pip install hidapi`

**GUI 无法启动**
- 确保已安装 WebKit2GTK 和 PyGObject：`python3 -c "import gi; gi.require_version('WebKit2','4.1')"`
- 如果 venv 无法 import gi，创建符号链接：`ln -s /usr/lib/python3/dist-packages/gi venv/lib/python3.12/site-packages/gi`
- 检查错误：`python3 valkyrie_app.py`

### 卸载

```bash
# 删除 udev 规则
sudo rm /etc/udev/rules.d/99-valkyrie.rules
sudo udevadm control --reload-rules

# 删除 Python 包
pip uninstall hidapi

# 删除仓库
cd ..
rm -rf valkyrie-linux-driver
```

---

**Support | 支持**: If you encounter issues, please open an issue on GitHub. | 如果遇到问题，请在 GitHub 上提交 issue。
