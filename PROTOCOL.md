# Protocol Documentation | 协议文档

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## USB/HID Protocol for Valkyrie C360

### Connection Information

- **Vendor ID (VID)**: 0x0416 (Winbond Electronics Corp.)
- **Product ID (PID)**: 0x5201
- **Interface**: USB HID
- **Report Size**: 64 bytes

### Packet Structure

All packets follow this basic structure:

```
Offset  Length  Description
------  ------  -----------
0-1     2       Magic header (0xDC 0xDC)
2-10    9       Fixed header
11      1       Command byte
12+     varies  Command-specific data
```

### Commands

#### 0x02 - Status Query

Query current sensor readings (temperature, RPM).

**Request:**
```
Byte    Value   Description
----    -----   -----------
0-1     DC DC   Magic header
2-10    (fixed) Standard header
11      02      CMD: Query
12-63   00      Padding
```

**Response:**
```
Byte    Value       Description
----    -----       -----------
0-1     DC DC       Magic header
...
14      04          Marker
15-16   XX XX       Fan 1 RPM (little-endian uint16)
17      04          Marker
18-19   XX XX       Fan 2 RPM (little-endian uint16)
20      04          Marker
21-22   XX XX       Pump RPM (little-endian uint16)
23      04          Marker
24-25   XX XX       Temperature * 10 (little-endian uint16)
```

**Example:**
```python
import hid

device = hid.device()
device.open(0x0416, 0x5201)

# Build query packet
pkt = bytearray(64)
pkt[0:11] = [0xDC, 0xDC, 0x01, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
pkt[11] = 0x02

# Send query
device.write(bytes([0x00]) + pkt)

# Read response
data = device.read(64)

# Parse response
fan1_rpm = data[15] | (data[16] << 8)
fan2_rpm = data[18] | (data[19] << 8)
pump_rpm = data[21] | (data[22] << 8)
temp_c = ((data[24] | (data[25] << 8)) / 10.0)
```

#### 0x06 - Speed Control

Set fan and pump speeds (0-100%).

**IMPORTANT**: This device requires sending **4 separate commands** with subcommands 0x01, 0x02, 0x03, 0x04. Each subcommand controls different physical output groups.

**Request (repeat for each subcommand):**
```
Byte    Value       Description
----    -----       -----------
0-1     DC DC       Magic header
2-10    (fixed)     Standard header
11      06          CMD: Speed control
12      01-04       Subcommand (0x01, 0x02, 0x03, or 0x04)
13      04          Channel count
14-17   XX XX XX XX Speed values (0-100 for each channel)
18-63   00          Padding
```

**Example:**
```python
import hid
import time

device = hid.device()
device.open(0x0416, 0x5201)

# Set all channels to 50%
speed = 50

# Send all 4 subcommands
for subcmd in [0x01, 0x02, 0x03, 0x04]:
    pkt = bytearray(64)
    pkt[0:11] = [0xDC, 0xDC, 0x01, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    pkt[11] = 0x06       # CMD: Speed control
    pkt[12] = subcmd     # Subcommand
    pkt[13] = 0x04       # 4 channels
    pkt[14] = speed      # Channel 1
    pkt[15] = speed      # Channel 2
    pkt[16] = speed      # Channel 3
    pkt[17] = speed      # Channel 4
    
    device.write(bytes([0x00]) + pkt)
    time.sleep(0.05)  # Small delay between subcommands

device.close()
```

### Multi-Subcommand Protocol

**Why 4 subcommands are needed:**

This device uses a multi-subcommand protocol where each subcommand controls different physical output groups:

```
CMD 0x06, SubCmd 0x01, Channels: [speed, speed, speed, speed]
CMD 0x06, SubCmd 0x02, Channels: [speed, speed, speed, speed]
CMD 0x06, SubCmd 0x03, Channels: [speed, speed, speed, speed]
CMD 0x06, SubCmd 0x04, Channels: [speed, speed, speed, speed]
```

Each subcommand appears to control:
- Fan channels
- Pump
- Potentially other outputs (RGB, auxiliary fans, etc.)

**If you only send one subcommand**, only some outputs will respond!

### Timing

- **Command response time**: ~100ms
- **Speed change ramp time**: ~10 seconds
- **Acceleration rate**: ~130 RPM/second (linear)

### Data Encoding

- **Multi-byte integers**: Little-endian (LSB first)
- **Temperature**: Value * 10 (e.g., 335 = 33.5°C)
- **RPM**: Direct value (e.g., 1840 = 1840 RPM)

### Common Issues

❌ **Wrong: Only sending one subcommand**
```python
pkt[12] = 0x01
device.write(bytes([0x00]) + pkt)
# Result: Only one fan responds!
```

✅ **Correct: Sending all 4 subcommands**
```python
for subcmd in [0x01, 0x02, 0x03, 0x04]:
    pkt[12] = subcmd
    device.write(bytes([0x00]) + pkt)
    time.sleep(0.05)
# Result: All outputs respond!
```

### Adapting to Other Devices

If you have a different device:

1. **Check VID:PID** using `lsusb`
2. **Test basic communication** with the query command (0x02)
3. **Experiment with subcommands** - your device may need 1, 2, 3, or 4 subcommands
4. **Monitor sensor response** to verify correct protocol

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details on adapting this driver.

---

<a name="chinese"></a>

## Valkyrie C360 USB/HID 协议

### 连接信息

- **供应商 ID (VID)**: 0x0416 (Winbond Electronics Corp.)
- **产品 ID (PID)**: 0x5201
- **接口**: USB HID
- **报告大小**: 64 字节

### 数据包结构

所有数据包遵循此基本结构：

```
偏移    长度    描述
------  ------  -----------
0-1     2       魔数头部 (0xDC 0xDC)
2-10    9       固定头部
11      1       命令字节
12+     变化    命令特定数据
```

### 命令

#### 0x02 - 状态查询

查询当前传感器读数（温度、转速）。

**请求:**
```
字节    值      描述
----    -----   -----------
0-1     DC DC   魔数头部
2-10    (固定)  标准头部
11      02      CMD: 查询
12-63   00      填充
```

**响应:**
```
字节    值          描述
----    -----       -----------
0-1     DC DC       魔数头部
...
14      04          标记
15-16   XX XX       风扇 1 转速 (小端序 uint16)
17      04          标记
18-19   XX XX       风扇 2 转速 (小端序 uint16)
20      04          标记
21-22   XX XX       水泵转速 (小端序 uint16)
23      04          标记
24-25   XX XX       温度 * 10 (小端序 uint16)
```

**示例:**
```python
import hid

device = hid.device()
device.open(0x0416, 0x5201)

# 构建查询数据包
pkt = bytearray(64)
pkt[0:11] = [0xDC, 0xDC, 0x01, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
pkt[11] = 0x02

# 发送查询
device.write(bytes([0x00]) + pkt)

# 读取响应
data = device.read(64)

# 解析响应
fan1_rpm = data[15] | (data[16] << 8)
fan2_rpm = data[18] | (data[19] << 8)
pump_rpm = data[21] | (data[22] << 8)
temp_c = ((data[24] | (data[25] << 8)) / 10.0)
```

#### 0x06 - 速度控制

设置风扇和水泵速度 (0-100%)。

**重要**: 此设备需要发送带有子命令 0x01, 0x02, 0x03, 0x04 的 **4 个独立命令**。每个子命令控制不同的物理输出组。

**请求（对每个子命令重复）:**
```
字节    值          描述
----    -----       -----------
0-1     DC DC       魔数头部
2-10    (固定)      标准头部
11      06          CMD: 速度控制
12      01-04       子命令 (0x01, 0x02, 0x03, 或 0x04)
13      04          通道数量
14-17   XX XX XX XX 速度值 (每个通道 0-100)
18-63   00          填充
```

**示例:**
```python
import hid
import time

device = hid.device()
device.open(0x0416, 0x5201)

# 将所有通道设置为 50%
speed = 50

# 发送所有 4 个子命令
for subcmd in [0x01, 0x02, 0x03, 0x04]:
    pkt = bytearray(64)
    pkt[0:11] = [0xDC, 0xDC, 0x01, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    pkt[11] = 0x06       # CMD: 速度控制
    pkt[12] = subcmd     # 子命令
    pkt[13] = 0x04       # 4 个通道
    pkt[14] = speed      # 通道 1
    pkt[15] = speed      # 通道 2
    pkt[16] = speed      # 通道 3
    pkt[17] = speed      # 通道 4
    
    device.write(bytes([0x00]) + pkt)
    time.sleep(0.05)  # 子命令之间的小延迟

device.close()
```

### 多子命令协议

**为什么需要 4 个子命令：**

此设备使用多子命令协议，其中每个子命令控制不同的物理输出组：

```
CMD 0x06, SubCmd 0x01, 通道: [速度, 速度, 速度, 速度]
CMD 0x06, SubCmd 0x02, 通道: [速度, 速度, 速度, 速度]
CMD 0x06, SubCmd 0x03, 通道: [速度, 速度, 速度, 速度]
CMD 0x06, SubCmd 0x04, 通道: [速度, 速度, 速度, 速度]
```

每个子命令似乎控制：
- 风扇通道
- 水泵
- 可能的其他输出（RGB、辅助风扇等）

**如果您只发送一个子命令**，只有部分输出会响应！

### 时序

- **命令响应时间**: ~100ms
- **速度变化斜坡时间**: ~10 秒
- **加速度率**: ~130 RPM/秒（线性）

### 数据编码

- **多字节整数**: 小端序（LSB 优先）
- **温度**: 值 * 10（例如，335 = 33.5°C）
- **转速**: 直接值（例如，1840 = 1840 RPM）

### 常见问题

❌ **错误：只发送一个子命令**
```python
pkt[12] = 0x01
device.write(bytes([0x00]) + pkt)
# 结果：只有一个风扇响应！
```

✅ **正确：发送所有 4 个子命令**
```python
for subcmd in [0x01, 0x02, 0x03, 0x04]:
    pkt[12] = subcmd
    device.write(bytes([0x00]) + pkt)
    time.sleep(0.05)
# 结果：所有输出都响应！
```

### 适配到其他设备

如果您有不同的设备：

1. **使用 `lsusb` 检查 VID:PID**
2. **使用查询命令 (0x02) 测试基本通信**
3. **尝试不同的子命令** - 您的设备可能需要 1、2、3 或 4 个子命令
4. **监控传感器响应** 以验证正确的协议

有关适配此驱动程序的更多详细信息，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

**Version | 版本**: 2.0 - Multi-subcommand protocol implementation | 多子命令协议实现
