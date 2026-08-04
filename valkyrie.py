#!/usr/bin/env python3
"""
Valkyrie Elite Capellix Linux 控制程序
Linux Control Program for Valkyrie Elite Capellix AIO Cooler

用法 Usage:
  ./valkyrie.py status              # 显示当前状态 Show current status
  ./valkyrie.py set <0-100>         # 设置速度 Set speed (0-100%)
  ./valkyrie.py monitor             # 持续监控 Continuous monitoring
  ./valkyrie.py gui                 # 启动图形界面 Launch GUI
"""

import time
import sys

try:
    import hid
except ImportError:
    print("❌ 需要安装 hidapi / hidapi required: pip install hidapi")
    sys.exit(1)

VID = 0x0416
PID = 0x5201

def parse_sensor_data(data):
    """解析传感器数据 Parse sensor data

    校验魔数 + 协议标记位 + 温度合理范围，丢弃陈旧/错误数据包
    Validate magic + protocol markers + sane temp range, reject stale packets
    """
    if (len(data) < 26 or data[0] != 0xDC or data[1] != 0xDC
            or data[14] != 0x04 or data[17] != 0x04
            or data[20] != 0x04 or data[23] != 0x04):
        return None
    temp = (data[24] | (data[25] << 8)) / 10.0
    if not 0.0 < temp <= 200.0:
        return None
    return {
        'fan1_rpm': data[15] | (data[16] << 8),
        'fan2_rpm': data[18] | (data[19] << 8),
        'pump_rpm': data[21] | (data[22] << 8),
        'temp_c': temp
    }

def build_status_query():
    """构建状态查询帧 Build status query packet"""
    pkt = bytearray(64)
    pkt[0:11] = [0xDC, 0xDC, 0x01, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    pkt[11] = 0x02
    return bytes([0x00]) + pkt

def set_all_speeds(device, speed_percent):
    """
    设置所有通道速度 Set all channel speeds

    关键 Critical: 必须发送 4 个子命令 Must send 4 subcommands (0x01-0x04)
    每个子命令控制不同的物理输出组 Each controls different physical outputs
    """
    speed_hex = max(0, min(100, speed_percent))

    for subcmd in [0x01, 0x02, 0x03, 0x04]:
        pkt = bytearray(64)
        pkt[0:11] = [0xDC, 0xDC, 0x01, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        pkt[11] = 0x06       # CMD: 速度控制 Speed control
        pkt[12] = subcmd     # 子命令 Subcommand
        pkt[13] = 0x04       # 4个通道 4 channels
        pkt[14] = speed_hex
        pkt[15] = speed_hex
        pkt[16] = speed_hex
        pkt[17] = speed_hex

        device.write(bytes([0x00]) + pkt)
        time.sleep(0.05)

def read_current_speeds(device):
    """读取当前转速 Read current speeds"""
    device.write(build_status_query())
    time.sleep(0.1)
    data = device.read(64, timeout_ms=200)
    if data:
        return parse_sensor_data(data)
    return None

def cmd_status(device):
    """显示当前状态 Show current status"""
    sensor = read_current_speeds(device)
    if not sensor:
        print("❌ 无法读取传感器数据 Cannot read sensor data")
        return

    print("\n当前状态 Current Status:")
    print("=" * 50)
    print(f"  🌡️  水温 Coolant:  {sensor['temp_c']:.1f}°C")
    print(f"  💧 水泵 Pump:     {sensor['pump_rpm']:4d} RPM")
    print(f"  🌀 风扇1 Fan 1:   {sensor['fan1_rpm']:4d} RPM")
    print(f"  💨 风扇2 Fan 2:   {sensor['fan2_rpm']:4d} RPM")
    print("=" * 50)

def cmd_set_speed(device, speed):
    """设置速度 Set speed"""
    try:
        speed_val = int(speed)
        if not 0 <= speed_val <= 100:
            print("❌ 速度必须在 0-100 之间 Speed must be 0-100")
            return
    except ValueError:
        print("❌ 无效的速度值 Invalid speed value")
        return

    print(f"\n设置速度 Setting speed: {speed_val}%")
    print("发送 4 个子命令 Sending 4 subcommands...")

    set_all_speeds(device, speed_val)

    print("\n等待 8 秒 Waiting 8 seconds...")
    time.sleep(8)

    sensor = read_current_speeds(device)
    if sensor:
        print("\n新的转速 New speeds:")
        print("=" * 50)
        print(f"  💧 水泵 Pump:   {sensor['pump_rpm']:4d} RPM")
        print(f"  🌀 风扇1 Fan 1: {sensor['fan1_rpm']:4d} RPM")
        print(f"  💨 风扇2 Fan 2: {sensor['fan2_rpm']:4d} RPM")
        print("=" * 50)

def cmd_monitor(device):
    """持续监控模式 Continuous monitoring mode"""
    print("\n持续监控模式 Monitoring mode (按 Ctrl+C 停止 Press Ctrl+C to stop)")
    print("=" * 60)

    try:
        while True:
            sensor = read_current_speeds(device)
            if sensor:
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] 🌡️ {sensor['temp_c']:5.1f}°C | "
                      f"💧{sensor['pump_rpm']:4d} | "
                      f"🌀{sensor['fan1_rpm']:4d} | "
                      f"💨{sensor['fan2_rpm']:4d} RPM")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n停止监控 Monitoring stopped")

def cmd_gui():
    """启动图形界面 Launch GUI"""
    try:
        import subprocess
        subprocess.run(["python3", "valkyrie_app.py"])
    except Exception as e:
        print(f"❌ 无法启动 GUI Cannot launch GUI: {e}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1].lower()

    if command == "gui":
        cmd_gui()
        return

    # 打开设备 Open device
    try:
        dev = hid.device()
        dev.open(VID, PID)
        dev.set_nonblocking(True)
    except Exception as e:
        print(f"❌ 无法打开设备 Cannot open device: {e}")
        print("\n提示 Tips:")
        print("  1. 确保设备已连接 Ensure device is connected")
        print("  2. 检查 udev 规则 Check udev rules:")
        print("     sudo cp 99-valkyrie.rules /etc/udev/rules.d/")
        print("  3. 重新加载规则 Reload rules:")
        print("     sudo udevadm control --reload-rules && sudo udevadm trigger")
        return

    try:
        if command == "status":
            cmd_status(dev)
        elif command == "set":
            if len(sys.argv) < 3:
                print("❌ 用法 Usage: valkyrie.py set <0-100>")
                return
            cmd_set_speed(dev, sys.argv[2])
        elif command == "monitor":
            cmd_monitor(dev)
        else:
            print(f"❌ 未知命令 Unknown command: {command}")
            print(__doc__)
    finally:
        dev.close()

if __name__ == "__main__":
    main()
