# Contributing | 贡献指南

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## English Contributing Guide

Thank you for your interest in contributing to the Valkyrie Linux Driver project!

### How to Contribute

We welcome contributions in many forms:

- 🐛 **Bug reports** - Found an issue? Let us know!
- 💡 **Feature requests** - Have an idea? Share it!
- 📝 **Documentation** - Help improve our docs
- 🔧 **Code contributions** - Submit pull requests
- 🧪 **Testing** - Test on different systems and report results
- 🔌 **Hardware support** - Help adapt the driver to similar devices

### Reporting Issues

When reporting bugs, please include:

1. **System information**
   - Linux distribution and version
   - Python version
   - Hardware model (exact cooler model)

2. **Steps to reproduce**
   - What commands did you run?
   - What did you expect to happen?
   - What actually happened?

3. **Logs and output**
   - Error messages
   - Relevant log output
   - Output of `lsusb` showing your device

### Adapting to Similar Devices

If you have a different liquid cooler or similar USB device:

#### Step 1: Identify Your Device

```bash
# List all USB devices
lsusb

# Find your device and note the VID:PID
# Example: Bus 001 Device 005: ID 0416:5201 Winbond Electronics Corp.
```

#### Step 2: Check Device Communication

Try modifying the VID/PID in `valkyrie.py`:

```python
# Change these values to your device
VID = 0x0416  # Your vendor ID
PID = 0x5201  # Your product ID
```

#### Step 3: Test Basic Communication

```bash
# Try status query first
./valkyrie.py status
```

If this works, your device uses a similar protocol!

#### Step 4: Experiment with Subcommands

Some devices may need different numbers of subcommands:

```python
# Try with 1 subcommand
for subcmd in [0x01]:
    # ... send command

# Try with 2 subcommands
for subcmd in [0x01, 0x02]:
    # ... send command

# Try with 4 subcommands (like Valkyrie C360)
for subcmd in [0x01, 0x02, 0x03, 0x04]:
    # ... send command
```

Monitor your device's RPM response to determine which configuration works.

#### Step 5: Share Your Findings

If you successfully adapt the driver:

1. Open a pull request with your changes
2. Document the new VID/PID in README.md
3. Note any protocol differences in PROTOCOL.md
4. Share your hardware model for the compatibility list

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/Vince-0906/valkyrie-linux-driver.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation as needed
   - Include bilingual strings where appropriate

4. **Test your changes**
   - Test on real hardware if possible
   - Verify both CLI and GUI work
   - Check that existing functionality still works

5. **Commit your changes**
   ```bash
   git commit -m "Add feature: description"
   ```

6. **Push and create pull request**
   ```bash
   git push origin feature-name
   ```

### Code Style

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings for functions
- Include bilingual comments/strings where user-facing
- Keep functions focused and modular

### Documentation

When updating documentation:

- Update both English and Chinese versions
- Use clear, simple language
- Include code examples where helpful
- Update the table of contents if needed

### Community Guidelines

- Be respectful and constructive
- Help others when you can
- Share your findings and experiments
- Credit others' contributions

### License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

<a name="chinese"></a>

## 中文贡献指南

感谢您对 Valkyrie Linux 驱动项目的贡献兴趣！

### 如何贡献

我们欢迎多种形式的贡献：

- 🐛 **错误报告** - 发现问题？让我们知道！
- 💡 **功能请求** - 有想法？分享它！
- 📝 **文档** - 帮助改进我们的文档
- 🔧 **代码贡献** - 提交拉取请求
- 🧪 **测试** - 在不同系统上测试并报告结果
- 🔌 **硬件支持** - 帮助将驱动适配到类似设备

### 报告问题

报告错误时，请包括：

1. **系统信息**
   - Linux 发行版和版本
   - Python 版本
   - 硬件型号（确切的水冷型号）

2. **重现步骤**
   - 您运行了哪些命令？
   - 您期望发生什么？
   - 实际发生了什么？

3. **日志和输出**
   - 错误消息
   - 相关日志输出
   - `lsusb` 显示您设备的输出

### 适配到类似设备

如果您有不同的水冷或类似的 USB 设备：

#### 步骤 1：识别您的设备

```bash
# 列出所有 USB 设备
lsusb

# 找到您的设备并记下 VID:PID
# 示例：Bus 001 Device 005: ID 0416:5201 Winbond Electronics Corp.
```

#### 步骤 2：检查设备通信

尝试在 `valkyrie.py` 中修改 VID/PID：

```python
# 将这些值更改为您的设备
VID = 0x0416  # 您的供应商 ID
PID = 0x5201  # 您的产品 ID
```

#### 步骤 3：测试基本通信

```bash
# 首先尝试状态查询
./valkyrie.py status
```

如果这有效，您的设备使用类似的协议！

#### 步骤 4：尝试不同的子命令

某些设备可能需要不同数量的子命令：

```python
# 尝试 1 个子命令
for subcmd in [0x01]:
    # ... 发送命令

# 尝试 2 个子命令
for subcmd in [0x01, 0x02]:
    # ... 发送命令

# 尝试 4 个子命令（如 Valkyrie C360）
for subcmd in [0x01, 0x02, 0x03, 0x04]:
    # ... 发送命令
```

监控设备的 RPM 响应以确定哪种配置有效。

#### 步骤 5：分享您的发现

如果您成功适配了驱动：

1. 提交包含您更改的拉取请求
2. 在 README.md 中记录新的 VID/PID
3. 在 PROTOCOL.md 中注明任何协议差异
4. 分享您的硬件型号以添加到兼容性列表

### 拉取请求

1. **Fork 仓库**
   ```bash
   git clone https://github.com/Vince-0906/valkyrie-linux-driver.git
   ```

2. **创建功能分支**
   ```bash
   git checkout -b feature-name
   ```

3. **进行更改**
   - 遵循现有代码风格
   - 为复杂逻辑添加注释
   - 根据需要更新文档
   - 在适当的地方包含双语字符串

4. **测试您的更改**
   - 如果可能，在真实硬件上测试
   - 验证 CLI 和 GUI 都能工作
   - 检查现有功能仍然工作

5. **提交您的更改**
   ```bash
   git commit -m "Add feature: description"
   ```

6. **推送并创建拉取请求**
   ```bash
   git push origin feature-name
   ```

### 代码风格

- Python 代码遵循 PEP 8
- 使用描述性变量名
- 为函数添加文档字符串
- 在面向用户的地方包含双语注释/字符串
- 保持函数专注和模块化

### 文档

更新文档时：

- 同时更新英文和中文版本
- 使用清晰、简单的语言
- 在有帮助的地方包含代码示例
- 如果需要，更新目录

### 社区准则

- 尊重他人，建设性交流
- 尽可能帮助他人
- 分享您的发现和实验
- 认可他人的贡献

### 许可证

通过贡献，您同意您的贡献将根据 MIT 许可证授权。

---

**Contact | 联系方式**: For questions, open an issue on GitHub. | 如有疑问，请在 GitHub 上开启 issue。
