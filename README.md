# MazeMouse电脑鼠迷宫上位机

<div align="center">

![Version](https://img.shields.io/badge/version-3.4.2-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-orange.svg)
![License](https://img.shields.io/badge/license-Educational-yellow.svg)

**一个电脑鼠迷宫可视化与控制系统**

开发者：石殷睿（苏州大学电子信息学院）  
用途：电子系统课程设计  
联系方式：yinrui_shi@163.com  
求路过的学弟学妹一个小小的STAR⭐~  
<img width="296" height="120" alt="求星星" src="https://github.com/user-attachments/assets/78789cc4-6a8f-45d9-ace4-12b5267fba30" />

</div>

---

## 📋 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [系统要求](#系统要求)
- [安装说明](#安装说明)
- [使用说明](#使用说明)
  - [快速开始](#快速开始)
  - [界面介绍](#界面介绍)
  - [串口配置](#串口配置)
  - [通信协议](#通信协议)
  - [功能详解](#功能详解)
- [开发说明](#开发说明)
  - [项目结构](#项目结构)
  - [技术栈](#技术栈)
  - [核心模块](#核心模块)
  - [代码架构](#代码架构)
  - [扩展开发](#扩展开发)
  - [构建打包](#构建打包)
- [常见问题](#常见问题)
- [更新日志](#更新日志)
- [许可证](#许可证)

---

## 📖 项目简介

电脑鼠迷宫上位机是一款专为电子系统课程中涉及的电脑鼠（Micromouse）迷宫竞赛而设计的可视化与控制系统。该软件通过串口通信实时接收电脑鼠的位置、传感器数据等信息，并以直观的图形界面展示电脑鼠在迷宫中的运动轨迹、墙体信息、传感器状态等，同时支持轨迹回放、路径优化、数据导出等功能。

### 主要应用场景

- 🏁 电脑鼠迷宫竞赛训练与调试
- 📊 迷宫探索算法可视化分析
- 🔍 传感器数据实时监控
- 📈 轨迹数据记录与分析
- 🎓 电子系统设计课程教学

---

## ✨ 功能特性

### 🎯 核心功能

- **实时轨迹可视化**
  - 2D/3D 双模式显示
  - 动态轨迹绘制，支持轨迹渐隐效果
  - 实时显示电脑鼠位置、朝向和角度
  - 自动墙体绘制与更新

- **串口通信管理**
  - 自动检测可用串口
  - 支持自定义波特率、数据位、停止位、校验位
  - 实时数据收发监控
  - 通信速率统计

- **传感器监控**
  - 前后左右传感器状态实时显示
  - 传感器数据可视化
  - 墙体自动判断与绘制

- **轨迹回放系统**
  - 自动保存运行轨迹
  - 支持多轨迹回放对比
  - 轨迹快照功能
  - 轨迹数据导出

- **路径优化**
  - 自动计算最短路径
  - 支持手动发送优化路径
  - 路径可视化显示

- **数据管理**
  - 实时日志记录
  - 数据导出功能
  - 历史数据查看

### 🎨 界面特性

- 现代化 Fluent UI 设计（可选）
- 支持明暗主题切换
- 响应式布局设计
- 多页面导航系统
- 启动画面自定义

---

## 💻 系统要求

### 最低要求

- **操作系统**: Windows 7/8/10/11 (64位)
- **Python**: 3.8 或更高版本
- **内存**: 2GB RAM
- **存储空间**: 100MB 可用空间
- **串口**: USB转串口适配器（如需要）

### 推荐配置

- **操作系统**: Windows 10/11 (64位)
- **Python**: 3.9+
- **内存**: 4GB RAM 或更高
- **显示器**: 1920x1080 或更高分辨率

---

## 📦 安装说明

### 方式一：使用预编译可执行文件（推荐）

1. 下载最新版本的安装程序（`电脑鼠上位机_v3.4.2_安装程序.exe`）
2. 双击运行安装程序
3. 按照安装向导完成安装
4. 从开始菜单或桌面快捷方式启动程序

### 方式二：从源码运行

#### 1. 克隆或下载项目

```bash
# 如果使用 Git
git clone <repository-url>
cd 上位机设计

# 或直接下载 ZIP 文件并解压
```

#### 2. 安装 Python 依赖

```bash
# 基础依赖（必需）
pip install PyQt5>=5.15.0
pip install matplotlib>=3.5.0
pip install numpy>=1.21.0

# 可选依赖（增强功能）
pip install qfluentwidgets  # Fluent UI 支持
pip install qframelesswindow  # 无边框窗口支持
```

#### 3. 运行程序

```bash
# 使用 Fluent UI 界面（推荐）
python restored_main.py

# 或使用标准 PyQt5 界面
python main.py
```

### 方式三：使用 PyInstaller 打包

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包程序
pyinstaller --name="电脑鼠上位机" --icon=icon.ico --windowed restored_main.py

# 打包后的可执行文件在 dist 目录中
```

---

## 📚 使用说明

### 快速开始

1. **启动程序**
   - 双击桌面快捷方式或运行可执行文件
   - 首次启动会显示启动画面（可在设置中关闭）

2. **连接串口**
   - 在"串口配置"区域选择串口（如 COM3）
   - 设置波特率（默认 115200）
   - 点击"连接"按钮

3. **开始监控**
   - 连接成功后，程序会自动接收串口数据
   - 迷宫界面会实时显示电脑鼠的位置和轨迹
   - 传感器状态会在界面上实时更新

### 界面介绍

#### 主控制页面

- **左侧控制面板**
  - 串口配置区域
  - 控制按钮（启动/停止/复位等）
  - 传感器状态显示
  - 数据统计信息

- **右侧迷宫显示**
  - 8x8 迷宫网格
  - 实时轨迹绘制
  - 墙体显示
  - 电脑鼠位置与朝向

- **底部状态栏**
  - 连接状态
  - 运行模式
  - 数据接收状态
  - 通信速率

<div align="center">
  <img width="1100" alt="主控制页面 - 迷宫与控制面板" src="https://github.com/user-attachments/assets/aed41e9f-4476-4d92-873f-08398fce4ac5" />
</div>

#### 其他页面

- **实时日志页面**: 查看详细的收发数据日志  
  <div align="center">
    <img width="1100" alt="实时日志页面" src="https://github.com/user-attachments/assets/de2804cc-9a49-419e-89f5-b261ee187c01" />
  </div>

- **轨迹回放页面**: 回放历史运行轨迹  
  <div align="center">
    <img width="1100" alt="轨迹回放页面" src="https://github.com/user-attachments/assets/31c5a065-377f-4eb5-8872-af64bd99b9d9" />
  </div>

- **设置页面**: 配置主题、串口默认值等  
  <div align="center">
    <img width="1100" alt="设置页面与主题配置" src="https://github.com/user-attachments/assets/cf24f77d-4d9f-4369-834d-4df9bfb9ba29" />
  </div>

- **使用说明页面**: 查看详细的使用文档
- **关于页面**: 查看版本信息和开发者信息

#### 状态栏与串口信息示意

<div align="center">
  <img width="420" alt="状态栏与串口信息" src="https://github.com/user-attachments/assets/4ee69c49-2976-4d0d-aa67-bfae3285c448" />
</div>

### 串口配置

#### 基本配置

1. **选择串口**
   - 点击"串口"下拉框
   - 选择对应的 COM 端口
   - 如果列表为空，点击"刷新串口"按钮

2. **设置参数**
   - **波特率**: 通常为 115200、9600 等
   - **数据位**: 通常为 8
   - **停止位**: 通常为 1
   - **校验位**: 通常为"无"

3. **连接/断开**
   - 点击"连接"按钮建立连接
   - 连接成功后按钮变为"断开"
   - 点击"断开"按钮关闭连接

#### 高级设置

在"设置"页面可以配置：
- 默认串口参数（下次启动自动应用）
- 串口超时设置
- 数据缓冲区大小

### 通信协议

#### 数据帧格式

```
s,X,Y,O,Angle,Front,Left,Right,Mode\r\n
```

#### 参数说明

| 参数 | 说明 | 取值范围 | 示例 |
|------|------|----------|------|
| `s` | 帧起始标识 | 固定为 's' | s |
| `X` | 列坐标 | 0-7 | 3 |
| `Y` | 行坐标 | 0-7 | 4 |
| `O` | 朝向 | 0=北, 1=东, 2=南, 3=西 | 1 |
| `Angle` | 陀螺仪角度（度） | 0-360 | 45.5 |
| `Front` | 前传感器 | 0=有墙, 1=无墙 | 0 |
| `Left` | 左传感器 | 0=有墙, 1=无墙 | 1 |
| `Right` | 右传感器 | 0=有墙, 1=无墙 | 1 |
| `Mode` | 运行模式 | 0=停止, 1=迷宫模式 | 1 |

#### 示例数据帧

```
s,3,4,1,45.5,0,1,1,1\r\n
```

**解析**:
- 位置: (3, 4)
- 朝向: 东（1）
- 角度: 45.5°
- 前方: 有墙（0）
- 左侧: 无墙（1）
- 右侧: 无墙（1）
- 模式: 迷宫模式（1）

#### 墙体自动判断

系统根据以下规则自动判断并绘制墙体：

1. **前方墙体**: 当 `Front=0` 时，在电脑鼠前方绘制墙体
2. **左侧墙体**: 当 `Left=0` 时，在电脑鼠左侧绘制墙体
3. **右侧墙体**: 当 `Right=0` 时，在电脑鼠右侧绘制墙体

墙体方向根据电脑鼠的朝向自动计算：
- 朝向为北（O=0）时：前=北，左=西，右=东
- 朝向为东（O=1）时：前=东，左=北，右=南
- 朝向为南（O=2）时：前=南，左=东，右=西
- 朝向为西（O=3）时：前=西，左=南，右=北

### 功能详解

#### 1. 轨迹可视化

- **2D 模式**: 俯视图显示，清晰展示迷宫布局
- **3D 模式**: 立体视图，更直观的视觉效果
- **轨迹样式**: 支持自定义轨迹长度和渐隐效果
- **实时更新**: 电脑鼠移动时轨迹实时绘制

#### 2. 传感器监控

- **实时显示**: 前后左右传感器状态实时更新
- **可视化**: 传感器状态以图标形式显示
- **数据记录**: 传感器数据记录在日志中

#### 3. 轨迹回放

- **自动保存**: 每次运行自动保存轨迹
- **回放控制**: 支持播放、暂停、重置
- **多轨迹对比**: 可以同时查看多个轨迹
- **快照功能**: 保存当前轨迹为快照

#### 4. 路径优化

- **自动计算**: 到达终点后自动计算最短路径
- **手动发送**: 可以手动发送优化路径到电脑鼠
- **路径显示**: 优化路径在迷宫界面中高亮显示

#### 5. 数据导出

- **日志导出**: 导出实时日志为文本文件
- **轨迹导出**: 导出轨迹数据为 JSON 格式
- **数据统计**: 查看数据统计信息

---

## 🔧 开发说明

### 项目结构

```
上位机设计/
├── restored_main.py          # 主程序文件（推荐使用）
├── main.py                   # 原始主程序文件
├── main_fluent.py           # Fluent UI 版本
├── main_refactored.py        # 重构版本
├── icon.ico                  # 应用程序图标
├── README.md                 # 本文件
├── version.json.example      # 版本信息示例
├── version.txt.example       # 版本文本示例
├── main.spec                 # PyInstaller 配置文件
├── inno_setup_script.iss     # Inno Setup 安装脚本
├── build/                    # 构建输出目录
├── dist/                     # 打包输出目录
└── __pycache__/             # Python 缓存目录
```

### 技术栈

#### 核心框架

- **PyQt5** (5.15+): GUI 框架
  - `QtWidgets`: 界面组件
  - `QtSerialPort`: 串口通信
  - `QtCore`: 核心功能（定时器、信号槽等）
  - `QtGui`: 图形绘制

- **Matplotlib** (3.5+): 数据可视化
  - `FigureCanvasQTAgg`: Qt5 后端
  - `mpl_toolkits.mplot3d`: 3D 绘图支持

- **NumPy** (1.21+): 数值计算

#### 可选依赖

- **qfluentwidgets**: Fluent UI 组件库（可选）
- **qframelesswindow**: 无边框窗口支持（可选）

### 核心模块

#### 1. `MicroMouseApp` 类

主应用程序类，负责：
- 界面初始化与布局管理
- 串口通信管理
- 数据解析与处理
- 状态管理

**关键方法**:
- `connect_serial()`: 连接串口
- `read_serial_data()`: 读取串口数据
- `_handle_frame()`: 处理数据帧
- `update_plot()`: 更新迷宫显示

#### 2. `MazePlotter` 类

迷宫绘图类，负责：
- 2D/3D 迷宫绘制
- 轨迹绘制
- 墙体绘制
- 视图切换

**关键方法**:
- `setup_maze_plot()`: 初始化 2D 绘图
- `setup_3d_plot()`: 初始化 3D 绘图
- `draw_maze_wall()`: 绘制墙体
- `update_plot()`: 更新 2D 显示
- `update_plot_3d()`: 更新 3D 显示

#### 3. `CompassWidget` 类

指南针组件，显示电脑鼠角度：
- 角度数值显示
- 动态指南针绘制
- 角度归一化处理

#### 4. `SettingsPage` 类

设置页面，管理应用配置：
- 主题设置
- 串口默认值
- 启动画面设置
- 其他偏好设置

#### 5. `ReplayPage` 类

轨迹回放页面：
- 轨迹列表管理
- 回放控制
- 轨迹快照

#### 6. `RealtimeLogPage` 类

实时日志页面：
- 日志显示
- 数据过滤
- 日志导出

### 代码架构

#### 设计模式

1. **MVC 模式**
   - Model: 数据模型（位置、传感器数据等）
   - View: 界面组件（MazePlotter、CompassWidget 等）
   - Controller: 主应用类（MicroMouseApp）

2. **观察者模式**
   - 使用 PyQt5 信号槽机制
   - 数据更新自动通知界面

3. **单例模式**
   - QSettings 单例管理配置
   - 应用主窗口单例

#### 数据流

```
串口数据 → read_serial_data() → 数据解析 → _handle_frame() 
    ↓
更新数据模型（位置、传感器等）
    ↓
触发界面更新信号
    ↓
MazePlotter.update_plot() → 绘制界面
```

#### 关键数据结构

```python
# 位置数据
mouse_current_x, mouse_current_y: float  # 当前坐标
mouse_orientation: int  # 朝向 (0-3)
gyro_angle: float  # 陀螺仪角度

# 轨迹数据
mouse_path_x, mouse_path_y: list  # 轨迹点列表

# 墙体数据
wall_map: dict  # {(x, y): wall_mask} 墙体映射

# 传感器数据
front_val, left_val, right_val: int  # 传感器值 (0/1)
```

### 扩展开发

#### 添加新功能

1. **添加新的数据字段**
   ```python
   # 在 MicroMouseApp.__init__() 中添加
   self.new_field = default_value
   
   # 在 _handle_frame() 中解析
   self.new_field = parsed_value
   
   # 在界面中显示
   self.new_label.setText(str(self.new_field))
   ```

2. **添加新的页面**
   ```python
   # 创建页面类
   class NewPage(QWidget):
       def __init__(self, parent=None):
           super().__init__(parent)
           # 初始化界面
   
   # 在主窗口中添加
   new_page = NewPage(parent=win)
   win.addSubInterface(new_page, icon, "页面名称", position)
   ```

3. **扩展通信协议**
   ```python
   # 修改 _handle_frame() 方法
   def _handle_frame(self, line):
       parts = line.split(',')
       # 解析新字段
       new_field = parts[8]  # 假设是第9个字段
       # 处理新数据
   ```

#### 自定义主题

1. **修改样式表**
   ```python
   # 在 apply_theme() 方法中添加
   if theme == "dark":
       self.setStyleSheet("""
           QWidget {
               background-color: #1e1e1e;
               color: #ffffff;
           }
       """)
   ```

2. **添加新主题**
   ```python
   # 在设置页面添加主题选项
   self.theme_combo.addItem("custom_theme")
   
   # 在 apply_theme() 中处理
   elif theme == "custom_theme":
       # 应用自定义主题
   ```

#### 性能优化

1. **减少重绘频率**
   ```python
   # 使用定时器批量更新
   self.update_timer = QTimer()
   self.update_timer.timeout.connect(self.batch_update)
   self.update_timer.start(100)  # 100ms 更新一次
   ```

2. **优化数据结构**
   ```python
   # 使用 deque 提高队列操作效率
   from collections import deque
   self.data_queue = deque(maxlen=1000)
   ```

3. **异步处理**
   ```python
   # 使用线程处理耗时操作
   import threading
   thread = threading.Thread(target=heavy_task)
   thread.start()
   ```

### 构建打包

#### 使用 PyInstaller

1. **创建 spec 文件**
   ```bash
   pyi-makespec --name="电脑鼠上位机" --icon=icon.ico --windowed restored_main.py
   ```

2. **修改 spec 文件**
   ```python
   # 添加数据文件、隐藏导入等
   datas = [('icon.ico', '.')]
   hiddenimports = ['matplotlib.backends.backend_qt5agg']
   ```

3. **执行打包**
   ```bash
   pyinstaller 电脑鼠上位机.spec
   ```

#### 使用 Inno Setup 创建安装程序

1. 安装 Inno Setup
2. 打开 `inno_setup_script.iss`
3. 修改版本号、路径等信息
4. 编译脚本生成安装程序

#### 版本管理

1. **更新版本号**
   ```python
   # 在 restored_main.py 中修改
   APP_VERSION = "3.4.3"  # 新版本号
   ```

2. **创建版本信息文件**
   ```json
   {
       "version": "3.4.3",
       "download_url": "https://example.com/download",
       "release_notes": "更新内容..."
   }
   ```

---

## ❓ 常见问题

### 串口相关问题

**Q: 无法检测到串口？**
- 检查 USB 转串口驱动是否安装
- 确认串口设备已连接
- 尝试点击"刷新串口"按钮
- 检查设备管理器中串口是否正常

**Q: 连接串口失败？**
- 确认串口未被其他程序占用
- 检查串口参数是否正确（波特率、数据位等）
- 尝试重新插拔 USB 设备
- 检查串口权限（Linux/Mac）

**Q: 接收不到数据？**
- 确认串口已成功连接
- 检查下位机是否正常发送数据
- 查看"实时日志"页面确认数据接收情况
- 检查数据格式是否符合协议要求

### 界面相关问题

**Q: 界面显示异常？**
- 尝试切换主题（明暗主题）
- 检查屏幕分辨率设置
- 重启程序
- 清除设置文件重新配置

**Q: 迷宫不显示或显示错误？**
- 确认已接收到有效数据帧
- 检查数据格式是否正确
- 尝试重置迷宫（复位按钮）
- 查看控制台错误信息

**Q: 3D 视图无法显示？**
- 确认已安装 matplotlib 3D 支持
- 检查显卡驱动是否正常
- 尝试切换到 2D 视图

### 性能相关问题

**Q: 程序运行卡顿？**
- 关闭不必要的其他程序
- 减少轨迹点数量（在设置中调整）
- 降低更新频率
- 检查系统资源使用情况

**Q: 内存占用过高？**
- 定期清理历史轨迹数据
- 减少日志缓冲区大小
- 重启程序释放内存

### 其他问题

**Q: 如何导出数据？**
- 在"实时日志"页面点击"导出"按钮
- 在"轨迹回放"页面导出轨迹数据
- 数据以文本或 JSON 格式保存

**Q: 如何重置所有设置？**
- 删除配置文件（Windows: `%APPDATA%\MicromouseLab\MicromouseApp`）
- 或在设置页面手动恢复默认值

**Q: 程序无法启动？**
- 检查 Python 版本是否符合要求
- 确认所有依赖已正确安装
- 查看错误日志
- 尝试以管理员权限运行

---

## 📝 更新日志

### v3.4.2 (当前版本)

- ✅ 修复 `_purge_old_bytes` 方法中的无限循环问题
- ✅ 优化界面响应性能
- ✅ 改进错误处理机制
- ✅ 增强数据解析稳定性

### v3.4.1

- 添加 3D 视图支持
- 优化轨迹绘制性能
- 改进传感器数据显示

### v3.4.0

- 重构界面布局
- 添加 Fluent UI 支持
- 新增轨迹回放功能
- 改进设置管理

### 更早版本

- 初始版本发布
- 基础功能实现

---

## 📄 许可证

本项目为电子系统设计课程项目，仅供学习交流使用。

**版权信息**:
- Copyright © 2025 石殷睿
- 苏州大学电子信息学院
- 电子系统课程设计项目

**使用限制**:
- 本软件仅供学习和研究使用
- 禁止用于商业用途
- 保留所有权利

---

## 📞 联系方式

- **开发者**: 石殷睿
- **学校**: 苏州大学电子信息学院
- **邮箱**: yinrui_shi@163.com
- **项目网址**: https://www.quartz.xin

---

## 🙏 致谢

感谢以下开源项目的支持：
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)
- [qfluentwidgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

---

<div align="center">

**如果这个项目对你有帮助，欢迎 Star ⭐**

by 石殷睿

</div>

