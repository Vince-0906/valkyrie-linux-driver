# Changelog | 更新日志

All notable changes to this project will be documented in this file.

本文件记录此项目的所有重要更改。

---

## [3.0.0] - 2026-08-05

### 🎉 Major Release | 重大版本

**New cyberpunk-style control terminal: native window with web-rendered UI.**

**全新赛博朋克风格控制终端：原生窗口 + Web 渲染界面。**

### Added | 新增

- New `valkyrie_app.py` GUI: native desktop window (pywebview + WebKitGTK) rendering a cyberpunk industrial-style UI
  - 全新 `valkyrie_app.py` GUI：原生桌面窗口（pywebview + WebKitGTK），赛博朋克工业风界面
- Embedded HTTP backend with REST API (`/api/status`, `/api/speed`), thread-safe HID access, auto-reconnect
  - 内置 HTTP 后端与 REST API（`/api/status`、`/api/speed`），线程安全 HID 访问，断线自动重连
- Temperature gauge range updated to 40-160°C (normal operating range 60-150°C)
  - 温度量程更新为 40-160°C（正常工作范围 60-150°C）

### Fixed | 修复

- Sensor parser now validates protocol marker bytes (0x04) and rejects stale/invalid packets that caused bogus temperature readings
  - 传感器解析器现在校验协议标记位（0x04），丢弃导致错误温度读数的陈旧/无效数据包

### Removed | 移除

- Removed `valkyrie_gui.py` (tkinter GUI) and the standalone browser WebUI, superseded by `valkyrie_app.py`
  - 移除 `valkyrie_gui.py`（tkinter 图形界面）和独立浏览器 WebUI，由 `valkyrie_app.py` 取代

---

## [2.0.0] - 2024-08-05

### 🎉 Major Release | 重大版本

**Complete implementation with full device control.**

**完整实现，完全设备控制。**

### Added | 新增

- Multi-subcommand protocol support for comprehensive device control
  - 多子命令协议支持，实现全面的设备控制
- New unified `valkyrie.py` CLI tool with bilingual support
  - 新的统一 `valkyrie.py` 命令行工具，支持双语
- Redesigned `valkyrie_gui.py` with improved bilingual interface
  - 重新设计的 `valkyrie_gui.py`，改进的双语界面
- Comprehensive bilingual documentation (English/Chinese)
  - 全面的双语文档（英文/中文）
- Virtual environment setup instructions
  - 虚拟环境设置说明

### Fixed | 修复

- ✅ **All channels now respond to speed commands**
  - **所有通道现在都响应速度命令**
- ✅ Water pump: Full speed control (534 → 1840+ RPM)
  - 水泵：完全速度控制（534 → 1840+ RPM）
- ✅ Fan channels: Complete PWM control (550 → 1800+ RPM)
  - 风扇通道：完整 PWM 控制（550 → 1800+ RPM）
- ✅ Smooth 10-second acceleration response
  - 平滑的 10 秒加速响应

### Changed | 更改

- Simplified project structure with clean entry points
  - 简化的项目结构，清晰的入口点
- Updated all documentation with improved clarity
  - 更新所有文档，提高清晰度
- README now features bilingual clickable navigation
  - README 现在具有双语可点击导航
- Enhanced device finding and adaptation guidance
  - 增强的设备查找和适配指南

### Technical Details | 技术细节

- Implemented 4-subcommand protocol (0x01-0x04)
  - 实现 4 子命令协议（0x01-0x04）
- Each subcommand controls different physical output groups
  - 每个子命令控制不同的物理输出组
- Verified linear acceleration: ~130 RPM/sec
  - 验证线性加速：约 130 RPM/秒
- All changes tested and verified on real hardware
  - 所有更改均在真实硬件上测试和验证

---

## [1.0.0] - 2024-08-04

### Added | 新增

- Initial release with basic functionality
  - 初始版本，基本功能
- USB/HID protocol implementation
  - USB/HID 协议实现
- Status query (temperature, RPM)
  - 状态查询（温度、转速）
- Basic speed control
  - 基本速度控制
- GUI interface with tkinter
  - tkinter 图形界面
- CLI tool for operations
  - 操作命令行工具
- udev rules for non-root access
  - 用于非 root 访问的 udev 规则

---

## Future Roadmap | 未来路线图

- [ ] Temperature-based automatic speed curves
  - [ ] 基于温度的自动速度曲线
- [ ] RGB LED control (if hardware supports)
  - [ ] RGB LED 控制（如果硬件支持）
- [ ] systemd service for daemon mode
  - [ ] systemd 服务用于守护进程模式
- [ ] Integration with lm-sensors
  - [ ] 与 lm-sensors 集成
- [ ] Configuration file support
  - [ ] 配置文件支持
- [ ] Support for additional device models
  - [ ] 支持更多设备型号

---

**Note | 注意**: Version 2.0.0 provides complete device control with verified hardware support.

版本 2.0.0 提供完整的设备控制，并经过硬件验证支持。
