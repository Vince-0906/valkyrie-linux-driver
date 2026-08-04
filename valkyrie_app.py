#!/usr/bin/env python3
"""
Valkyrie C360 控制终端 (原生窗口, Web 渲染)
Control Terminal for Valkyrie C360 AIO Cooler
Native window powered by pywebview + WebKitGTK
"""

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    import hid
except ImportError:
    print("❌ 需要安装 hidapi / hidapi required: pip install hidapi")
    import sys
    sys.exit(1)

try:
    import webview
except ImportError:
    print("❌ 需要安装 pywebview / required: pip install pywebview")
    import sys
    sys.exit(1)

VID = 0x0416
PID = 0x5201
UI_DIR = Path(__file__).resolve().parent / "ui"


class Cooler:
    """设备通信封装（线程安全） Thread-safe device communication wrapper"""

    def __init__(self):
        self.lock = threading.Lock()
        self.device = None
        self.data = {
            "connected": False,
            "temp_c": None,
            "pump_rpm": None,
            "fan1_rpm": None,
            "fan2_rpm": None,
        }

    def _open_locked(self):
        try:
            dev = hid.device()
            dev.open(VID, PID)
            dev.set_nonblocking(True)
            self.device = dev
        except Exception:
            self.device = None

    def _close_locked(self):
        try:
            if self.device:
                self.device.close()
        except Exception:
            pass
        self.device = None
        self.data.update(connected=False, temp_c=None,
                         pump_rpm=None, fan1_rpm=None, fan2_rpm=None)

    @staticmethod
    def _parse(data):
        # 校验魔数 + 协议标记位 + 温度合理范围，丢弃陈旧/错误数据包
        # Validate magic + protocol markers + sane temp range, reject stale packets
        if (len(data) < 26 or data[0] != 0xDC or data[1] != 0xDC
                or data[14] != 0x04 or data[17] != 0x04
                or data[20] != 0x04 or data[23] != 0x04):
            return None
        temp = (data[24] | (data[25] << 8)) / 10.0
        if not 0.0 < temp <= 200.0:
            return None
        return {
            "fan1_rpm": data[15] | (data[16] << 8),
            "fan2_rpm": data[18] | (data[19] << 8),
            "pump_rpm": data[21] | (data[22] << 8),
            "temp_c": temp,
        }

    def poll_sensors(self):
        """读取一次传感器（由监控线程周期调用） Read sensors once"""
        with self.lock:
            if self.device is None:
                self._open_locked()
            if self.device is None:
                return
            try:
                pkt = bytearray(64)
                pkt[0:11] = [0xDC, 0xDC, 0x01, 0x00, 0x03, 0x00,
                             0x00, 0x00, 0x00, 0x00, 0x00]
                pkt[11] = 0x02
                self.device.write(bytes([0x00]) + pkt)
                time.sleep(0.1)
                # 取最后一个有效数据包，排空可能积压的陈旧响应
                # Drain the queue, keep the last valid packet
                parsed = None
                for _ in range(4):
                    raw = self.device.read(64, timeout_ms=200)
                    if not raw:
                        break
                    parsed = self._parse(raw) or parsed
                if parsed:
                    self.data.update(connected=True, **parsed)
            except Exception:
                self._close_locked()

    def set_speed(self, speed):
        """下发转速 0-100% Apply speed 0-100%"""
        speed = max(0, min(100, int(speed)))
        with self.lock:
            if self.device is None:
                self._open_locked()
            if self.device is None:
                raise RuntimeError("device not connected")
            try:
                # 发送4个子命令 Send 4 subcommands
                for subcmd in [0x01, 0x02, 0x03, 0x04]:
                    pkt = bytearray(64)
                    pkt[0:11] = [0xDC, 0xDC, 0x01, 0x00, 0x03, 0x00,
                                 0x00, 0x00, 0x00, 0x00, 0x00]
                    pkt[11] = 0x06
                    pkt[12] = subcmd
                    pkt[13] = 0x04
                    pkt[14:18] = [speed] * 4
                    self.device.write(bytes([0x00]) + pkt)
                    time.sleep(0.05)
            except Exception:
                self._close_locked()
                raise

    def monitor_loop(self):
        while True:
            self.poll_sensors()
            time.sleep(2)

    def start_monitor(self):
        t = threading.Thread(target=self.monitor_loop, daemon=True)
        t.start()

    def close(self):
        with self.lock:
            self._close_locked()


class Handler(BaseHTTPRequestHandler):
    """内置 HTTP 服务: 向 WebView 提供页面与 API
    Embedded HTTP server: serves the UI page and API to the WebView"""

    cooler: Cooler = None  # 由 main() 注入 Injected by main()
    server_version = "ValkyrieApp/1.0"

    def log_message(self, fmt, *args):
        pass  # 静默日志 Silence request logs

    def _send_json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path):
        try:
            body = path.read_bytes()
        except OSError:
            self._send_json({"ok": False, "error": "not found"}, 404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send_file(UI_DIR / "index.html")
        elif self.path == "/api/status":
            self._send_json(self.cooler.data)
        else:
            self._send_json({"ok": False, "error": "not found"}, 404)

    def do_POST(self):
        if self.path != "/api/speed":
            self._send_json({"ok": False, "error": "not found"}, 404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            speed = int(payload["speed"])
        except Exception:
            self._send_json({"ok": False, "error": "bad request"}, 400)
            return
        try:
            self.cooler.set_speed(speed)
            self._send_json({"ok": True, "speed": max(0, min(100, speed))})
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)


def main():
    Handler.cooler = Cooler()
    Handler.cooler.start_monitor()

    # 端口 0 = 自动分配空闲端口 Auto-assign a free port
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    url = f"http://127.0.0.1:{server.server_address[1]}"

    print("┌──────────────────────────────────────────────┐")
    print("│  VALKYRIE C360 // COOLING CONTROL TERMINAL   │")
    print("└──────────────────────────────────────────────┘")
    print("  ▸ 控制终端已启动 Terminal online")
    print("  ▸ 关闭窗口退出 Close window to quit")

    # 服务器跑在后台线程, 主线程跑原生 WebView 窗口
    # Server in background thread, native WebView window on main thread
    threading.Thread(target=server.serve_forever, daemon=True).start()
    window = webview.create_window(
        "VALKYRIE C360 // 水冷控制终端",
        url, width=1180, height=860, min_size=(960, 720),
        background_color="#0a0a0b")
    try:
        webview.start()
    except KeyboardInterrupt:
        pass
    finally:
        window.destroy()
        server.shutdown()
        Handler.cooler.close()
        server.server_close()


if __name__ == "__main__":
    main()
