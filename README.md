# Valkyrie C360 AIO Linux Driver | 瓦尔基里 C360 水冷 Linux 驱动

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## 🌊 Valkyrie C360 AIO Cooler - Linux Driver

Unofficial Linux driver for the Valkyrie C360 all-in-one liquid cooler.

### Features

- ✅ **Full control of all channels** - Pump + 2 fans
- ✅ **Real-time monitoring** - Temperature and RPM sensors
- ✅ **Speed control** - 0-100% PWM control
- ✅ **Native GUI** - Cyberpunk-style control terminal (native window, web-rendered)
- ✅ **CLI tool** - Command-line interface for automation

### Hardware Support

- **Valkyrie C360** (VID: 0x0416, PID: 0x5201)
- Likely compatible with other Myth.cool products using the same controller

### Finding Your Device

To check if this driver supports your device:

```bash
# List USB devices
lsusb

# Look for lines like:
# Bus 001 Device 005: ID 0416:5201 Winbond Electronics Corp.

# Check detailed info
sudo lsusb -v -d 0416:5201
```

If your device has a different VID:PID, you may need to:
1. Modify the device IDs in the Python scripts
2. Test basic communication with your device
3. Adjust the protocol if necessary

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance on adapting this driver to similar devices.

### Quick Start

#### Installation

```bash
# Clone repository
git clone https://github.com/Vince-0906/valkyrie-linux-driver.git
cd valkyrie-linux-driver

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# GUI: install system WebView runtime (Linux, preinstalled on GNOME)
sudo apt install libwebkit2gtk-4.1-0 python3-gi

# If the venv cannot import gi (no system site packages), link it in:
ln -s /usr/lib/python3/dist-packages/gi venv/lib/python3.12/site-packages/gi

# Install udev rules (for non-root access)
sudo cp 99-valkyrie.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

#### Usage

**GUI** (Recommended)
```bash
# Activate virtual environment first
source venv/bin/activate

# Launch the control terminal (native window)
./valkyrie_app.py
```

**Command Line**
```bash
# Activate virtual environment first
source venv/bin/activate

# Check status
./valkyrie.py status

# Set speed to 100%
./valkyrie.py set 100

# Set speed to 50%
./valkyrie.py set 50

# Continuous monitoring
./valkyrie.py monitor
```

### Project Structure

```
valkyrie-linux-driver/
├── valkyrie.py            Main CLI tool
├── valkyrie_app.py        GUI control terminal (pywebview native window)
├── ui/index.html          UI page rendered in the native window
├── 99-valkyrie.rules      udev rules
├── requirements.txt       Python dependencies
├── PROTOCOL.md            Protocol documentation
├── INSTALL.md             Installation guide
├── CHANGELOG.md           Version history
├── CONTRIBUTING.md        Contribution guidelines
└── LICENSE                MIT License
```

### Requirements

- Python 3.7+
- hidapi
- pywebview (for GUI)
- Linux: WebKit2GTK + PyGObject (for GUI, usually preinstalled on GNOME desktops)

### Hardware Testing Results

Testing on Linux systems:

| Channel | Idle Speed | Max Speed | Ramp Time |
|---------|-----------|-----------|-----------|
| Pump | ~530 RPM | ~1840 RPM | 10s |
| Fan 1 | ~550 RPM | ~1810 RPM | 10s |
| Fan 2 | ~550 RPM | ~1840 RPM | 10s |

*Note: Exact values may vary depending on your specific hardware configuration.*

### Known Issues

- Requires sudo/root access or udev rules for USB access
- Device-specific variations may require protocol adjustments

### Roadmap

- [x] Full control of all channels (pump + fans)
- [x] Real-time monitoring
- [ ] Temperature-based automatic speed curves
- [ ] RGB LED control (if supported by hardware)
- [ ] systemd service for background monitoring
- [ ] Integration with lm-sensors

### Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

### Disclaimer

This is an unofficial, community-developed driver. Use at your own risk. The authors are not affiliated with Valkyrie or Myth.cool.

### Acknowledgments

- Inspired by other open-source liquid cooling drivers
- Community testing and feedback

---

<a name="chinese"></a>

## 🌊 Valkyrie C360 一体式水冷 - Linux 驱动

Valkyrie C360 一体式水冷的非官方 Linux 驱动程序。

### 功能特性

- ✅ **完整控制所有通道** - 水泵 + 2 个风扇
- ✅ **实时监控** - 温度和转速传感器
- ✅ **速度控制** - 0-100% PWM 控制
- ✅ **原生 GUI** - 赛博朋克风格控制终端（原生窗口，Web 渲染）
- ✅ **命令行工具** - 用于自动化的命令行接口

### 硬件支持

- **Valkyrie C360** (VID: 0x0416, PID: 0x5201)
- 可能兼容其他使用相同控制器的 Myth.cool 产品

### 查找您的设备

检查此驱动是否支持您的设备：

```bash
# 列出 USB 设备
lsusb

# 查找类似以下的行：
# Bus 001 Device 005: ID 0416:5201 Winbond Electronics Corp.

# 查看详细信息
sudo lsusb -v -d 0416:5201
```

如果您的设备具有不同的 VID:PID，您可能需要：
1. 修改 Python 脚本中的设备 ID
2. 测试与您的设备的基本通信
3. 必要时调整协议

有关将此驱动适配到类似设备的指导，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/Vince-0906/valkyrie-linux-driver.git
cd valkyrie-linux-driver

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# GUI：安装系统 WebView 运行时（Linux，GNOME 桌面通常已预装）
sudo apt install libwebkit2gtk-4.1-0 python3-gi

# 如果 venv 中无法 import gi（venv 不含系统站点包），创建符号链接：
ln -s /usr/lib/python3/dist-packages/gi venv/lib/python3.12/site-packages/gi

# 安装 udev 规则（用于非 root 访问）
sudo cp 99-valkyrie.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

#### 使用方法

**图形界面**（推荐）
```bash
# 首先激活虚拟环境
source venv/bin/activate

# 启动控制终端（原生窗口）
./valkyrie_app.py
```

**命令行**
```bash
# 首先激活虚拟环境
source venv/bin/activate

# 查看状态
./valkyrie.py status

# 设置速度为 100%
./valkyrie.py set 100

# 设置速度为 50%
./valkyrie.py set 50

# 持续监控
./valkyrie.py monitor
```

### 项目结构

```
valkyrie-linux-driver/
├── valkyrie.py            主命令行工具
├── valkyrie_app.py        GUI 控制终端（pywebview 原生窗口）
├── ui/index.html          原生窗口中渲染的 UI 页面
├── 99-valkyrie.rules      udev 规则
├── requirements.txt       Python 依赖
├── PROTOCOL.md            协议文档
├── INSTALL.md             安装指南
├── CHANGELOG.md           版本历史
├── CONTRIBUTING.md        贡献指南
└── LICENSE                MIT 许可证
```

### 系统要求

- Python 3.7+
- hidapi
- pywebview（用于 GUI）
- Linux：WebKit2GTK + PyGObject（用于 GUI，GNOME 桌面通常已预装）

### 硬件测试结果

在 Linux 系统上的测试结果：

| 通道 | 待机速度 | 最大速度 | 加速时间 |
|------|---------|---------|---------|
| 水泵 | ~530 RPM | ~1840 RPM | 10秒 |
| 风扇1 | ~550 RPM | ~1810 RPM | 10秒 |
| 风扇2 | ~550 RPM | ~1840 RPM | 10秒 |

*注意：确切数值可能因您的具体硬件配置而异。*

### 已知问题

- 需要 sudo/root 权限或 udev 规则才能访问 USB 设备
- 特定设备的变体可能需要协议调整

### 路线图

- [x] 完全控制所有通道（水泵 + 风扇）
- [x] 实时监控
- [ ] 基于温度的自动速度曲线
- [ ] RGB LED 控制（如果硬件支持）
- [ ] systemd 服务用于后台监控
- [ ] 与 lm-sensors 集成

### 贡献

欢迎贡献！详情请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE)。

### 免责声明

这是一个非官方的、社区开发的驱动程序。使用风险自负。作者与 Valkyrie 或 Myth.cool 无关。

### 致谢

- 受其他开源液冷驱动程序启发
- 社区测试和反馈

---

**Status**: ✅ Fully functional and tested on Linux systems

**状态**: ✅ 在 Linux 系统上完全功能且已测试
