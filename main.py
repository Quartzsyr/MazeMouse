"""电脑鼠迷宫上位机
开发者：石殷睿（苏州大学电子信息学院）
用途：电子系统课程设计
联系方式：yinrui_shi@163.com
"""

# 应用版本和信息
APP_VERSION = "3.4.2"
APP_NAME = "电脑鼠迷宫上位机"
APP_DEVELOPER = "石殷睿"
APP_SCHOOL = "苏州大学电子信息学院"
APP_EMAIL = "yinrui_shi@163.com"
APP_PROJECT = "电子系统课程设计"
APP_URL = "https://www.quartz.xin"
APP_COPYRIGHT = "Copyright © 2025"

import sys
import threading
import queue
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QGridLayout, QComboBox, QPushButton, QLabel, QLineEdit, QMessageBox, QTextEdit, QMenuBar, QAction, QGroupBox, QSplitter, QStatusBar, QSizePolicy, QStackedWidget, QFormLayout, QCheckBox, QFileDialog, QProgressBar, QSpinBox, QDoubleSpinBox, QListWidget, QListWidgetItem, QScrollArea
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, Qt, QSettings, QT_VERSION_STR, PYQT_VERSION_STR, QTimer, QPoint, pyqtSignal, QObject, QSize
from PyQt5.QtGui import QFont, QGuiApplication, QMovie, QIcon, QPainter, QPen, QBrush, QColor, QPolygon
from PyQt5.QtWidgets import QStyle # Added for standard icons

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.collections import LineCollection
from matplotlib import colors as mcolors
import math
from matplotlib.collections import LineCollection
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
import numpy as np
import time
from collections import deque
from matplotlib.patches import Rectangle # 新增导入
from mpl_toolkits.mplot3d.art3d import Poly3DCollection # 新增导入

# Optional Fluent UI integration - 临时禁用以修复兼容性问题
QFW_AVAILABLE = False
# try:
#     from qfluentwidgets import (
#         setTheme, Theme, setThemeColor,
#         ComboBox as QfwComboBox,
#         LineEdit as QfwLineEdit,
#         PrimaryPushButton as QfwPrimaryPushButton,
#         PushButton as QfwPushButton,
#         InfoBar, InfoBarPosition,
#         NavigationItemPosition,
#         FluentWindow,
#         FluentIcon as FIF
#     )
#     QFW_AVAILABLE = True
# except Exception:
#     QFW_AVAILABLE = False

# Optional Frameless Window
FRAM_AVAILABLE = False
try:
    from qframelesswindow import FramelessWindow, StandardTitleBar
    FRAM_AVAILABLE = True
except Exception:
    FRAM_AVAILABLE = False

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class NavigationBar(QWidget):
    """左侧导航栏组件"""
    itemClicked = pyqtSignal(int)  # 发送选中的索引
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.current_index = 0
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 16, 8, 16)
        layout.setSpacing(4)
        
        # 导航项列表
        self.nav_items = [
            {"text": "主控制", "icon": "🎮"},
            {"text": "实时日志", "icon": "📊"},
            {"text": "轨迹回放", "icon": "🎬"},
            {"text": "设置", "icon": "⚙️"},
            {"text": "文档", "icon": "📖"},
            {"text": "关于", "icon": "ℹ️"},
        ]
        
        self.buttons = []
        for i, item in enumerate(self.nav_items):
            btn = QPushButton(f"{item['icon']} {item['text']}")
            btn.setCheckable(True)
            btn.setObjectName("navButton")
            btn.clicked.connect(lambda checked, idx=i: self.on_item_clicked(idx))
            layout.addWidget(btn)
            self.buttons.append(btn)
        
        layout.addStretch()
        
        # 设置第一个按钮为选中状态
        if self.buttons:
            self.buttons[0].setChecked(True)
        
        # 样式由全局样式表统一管理
    
    def on_item_clicked(self, index):
        """处理导航项点击"""
        # 取消所有按钮的选中状态
        for btn in self.buttons:
            btn.setChecked(False)
        # 设置当前按钮为选中
        self.buttons[index].setChecked(True)
        self.current_index = index
        self.itemClicked.emit(index)
    
    def set_current_index(self, index):
        """设置当前选中的索引"""
        if 0 <= index < len(self.buttons):
            self.on_item_clicked(index)

class CompassArea(QWidget):
    """指南针绘制区域"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0.0
        
    def set_angle(self, angle_degrees: float):
        """设置角度"""
        self.angle = angle_degrees
        self.update()
        
    def paintEvent(self, event):
        """绘制指南针"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 获取绘制区域
        rect = self.rect()
        center_x = rect.width() / 2
        center_y = rect.height() / 2
        radius = min(center_x, center_y) - 5
        
        # 绘制外圈
        painter.setPen(QPen(QColor("#e2e8f0"), 2))
        painter.setBrush(QBrush(QColor("#f8fafc")))
        painter.drawEllipse(int(center_x - radius), int(center_y - radius), 
                           int(radius * 2), int(radius * 2))
        
        # 绘制方向标记（N, E, S, W）
        font = QFont("Arial", 8, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#64748b"), 1))
        
        # N (北)
        painter.drawText(int(center_x - 5), int(center_y - radius + 12), "N")
        # E (东)
        painter.drawText(int(center_x + radius - 12), int(center_y + 4), "E")
        # S (南)
        painter.drawText(int(center_x - 5), int(center_y + radius - 2), "S")
        # W (西)
        painter.drawText(int(center_x - radius + 2), int(center_y + 4), "W")
        
        # 保存当前状态
        painter.save()
        
        # 移动到中心点并旋转
        painter.translate(center_x, center_y)
        # 角度转换：0度=北，顺时针为正，需要转换为Qt的坐标系（0度=东，逆时针为正）
        # Qt坐标系：0度指向右（东），逆时针为正
        # 我们的坐标系：0度指向北，顺时针为正
        # 转换公式：qt_angle = 90 - angle
        qt_angle = 90 - self.angle
        painter.rotate(qt_angle)
        
        # 绘制箭头（指向当前方向）
        arrow_size = radius - 8
        painter.setPen(QPen(QColor("#10b981"), 3))
        painter.setBrush(QBrush(QColor("#10b981")))
        
        # 绘制箭头主体（从中心向上）
        arrow_points = [
            QPoint(0, -int(arrow_size)),  # 箭头尖端
            QPoint(-8, -int(arrow_size) + 12),  # 左下
            QPoint(-3, -int(arrow_size) + 8),  # 左中
            QPoint(-3, 0),  # 左底
            QPoint(3, 0),  # 右底
            QPoint(3, -int(arrow_size) + 8),  # 右中
            QPoint(8, -int(arrow_size) + 12),  # 右下
        ]
        
        polygon = QPolygon(arrow_points)
        painter.drawPolygon(polygon)
        
        # 恢复状态
        painter.restore()
        
        # 绘制中心点
        painter.setPen(QPen(QColor("#0f172a"), 2))
        painter.setBrush(QBrush(QColor("#0f172a")))
        painter.drawEllipse(int(center_x - 3), int(center_y - 3), 6, 6)

class CompassWidget(QWidget):
    """角度显示组件 - 显示小车角度（0-360度）和动态指南针"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(120, 120)  # 固定尺寸，正方形
        
        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 16px;
            }
        """)
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # 角度显示标签（只显示数值）
        self.angle_label = QLabel("0.0°")
        self.angle_label.setStyleSheet("""
            QLabel {
                color: #0f172a;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Microsoft YaHei', 'Arial';
                background-color: transparent;
            }
        """)
        self.angle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.angle_label)
        
        # 指南针显示区域（自定义绘制）
        self.compass_area = CompassArea(self)
        self.compass_area.setFixedSize(80, 80)
        layout.addWidget(self.compass_area, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
        # 初始化角度
        self.current_angle = 0.0
        self.update_angle(0.0)
    
    def update_angle(self, angle_degrees: float):
        """更新角度显示（角度以度为单位，0-360度）"""
        self.current_angle = angle_degrees
        
        # 规范化角度到0-360度范围
        normalized_angle = angle_degrees % 360.0
        if normalized_angle < 0:
            normalized_angle += 360.0
        
        # 更新角度显示，保留1位小数
        self.angle_label.setText(f"{normalized_angle:.1f}°")
        
        # 更新指南针角度
        self.compass_area.set_angle(normalized_angle)

class MazePlotter(FigureCanvas):
    def __init__(self, app_page, parent=None, width=5, height=5, dpi=100):
        self.app_page = app_page
        # Adjust figure background to match app theme
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#fafbfc')
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        # Make canvas expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(400, 300)
        # 路径数据与渐隐配置
        self.path_points = []
        self.path_max_len = 200
        self.path_fade_power = 0.85  # 0~1，越大越慢淡出
        self.path_collection = LineCollection([], linewidths=3.0, colors='#6366f1', alpha=0.9, zorder=5)
        self.axes.add_collection(self.path_collection)

        # 方向箭头呼吸动画
        self.arrow_timer = QTimer(self)
        self.arrow_timer.setInterval(120)
        self.arrow_timer.timeout.connect(self._pulse_arrow)
        self.arrow_phase = 0.0
        self.arrow_timer.start()
        
        # 3D显示模式相关
        self.view_mode = "2D"  # "2D" 或 "3D"
        self.axes_3d = None
        self.path_collection_3d = None
        self.mouse_pos_3d = None
        self.arrow_3d = None
        self.arrow_head_3d = None
        self.drawn_walls_3d = {}
        # 保存所有墙体数据，用于切换视图时重新绘制
        self.wall_data_cache = {}  # {(x, y): wall_mask}
        
        self.setup_maze_plot()

    def setup_maze_plot(self):
        """设置2D迷宫显示"""
        # 清除figure并重新创建2D axes
        self.figure.clear()
        self.axes = self.figure.add_subplot(111)
        
        # 设置现代化的背景色 - 更柔和的白色
        self.figure.patch.set_facecolor('#fafbfc')
        self.axes.set_facecolor('#ffffff')
        
        self.axes.set_aspect('equal', adjustable='box')
        self.axes.set_xlim(-0.5, 8.5) # 扩展边界使视觉更好
        self.axes.set_ylim(-0.5, 8.5)
        self.axes.set_xticks(range(9))
        self.axes.set_yticks(range(9))
        
        # 添加现代化的网格 - 更细腻
        self.axes.grid(True, color='#f1f5f9', linewidth=1.0, alpha=0.8, linestyle='-', zorder=1)
        
        # 现代化标题样式 - 减少padding，让图更靠近顶部
        self.axes.set_title("电脑鼠迷宫轨迹", 
                           color='#0f172a', fontsize=16, fontweight='600', 
                           fontfamily='Microsoft YaHei', pad=8)
        
        # 美化坐标轴 - 更精致的样式
        self.axes.tick_params(axis='x', colors='#64748b', labelsize=11, width=0.5)
        self.axes.tick_params(axis='y', colors='#64748b', labelsize=11, width=0.5)
        
        # 现代化边框 - 更细腻
        for spine in self.axes.spines.values():
            spine.set_color('#e2e8f0')
            spine.set_linewidth(1.2)

        # 现代化小鼠位置样式 - 更精致（移除图例避免遮挡）
        self.mouse_pos, = self.axes.plot([], [], 'o', color='#ef4444', 
                                        markersize=14, markeredgecolor='#ffffff', 
                                        markeredgewidth=2.5,
                                        zorder=10)
        
        # 重新初始化路径集合
        self.path_collection = LineCollection([], linewidths=3.0, colors='#6366f1', alpha=0.9, zorder=5)
        self.axes.add_collection(self.path_collection)
        
        # 减少绘图区域周围的边距，去掉无用背景
        self.figure.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.08)
        
        self.arrow = None # Initialize arrow object
        self.drawn_walls = {}
        self.draw()
        self._draw_goal_area_2d()

    def _draw_goal_area_2d(self):
        """在2D模式下绘制终点区域"""
        if hasattr(self.app_page, 'goal_min_x'):
            min_x = self.app_page.goal_min_x
            max_x = self.app_page.goal_max_x
            min_y = self.app_page.goal_min_y
            max_y = self.app_page.goal_max_y

            # 计算矩形的左下角坐标和宽高
            rect_x = min_x
            rect_y = min_y
            rect_width = (max_x - min_x) + 1
            rect_height = (max_y - min_y) + 1

            # 终点区域的颜色和透明度
            goal_color = '#3b82f6'  # 蓝色，根据需求可更改
            alpha = 0.2

            # 移除旧的终点区域绘制，防止重复绘制
            if hasattr(self, 'goal_patch_2d') and self.goal_patch_2d is not None:
                self.goal_patch_2d.remove()

            # 绘制矩形作为终点区域
            self.goal_patch_2d = Rectangle((rect_x, rect_y), rect_width, rect_height,
                                            facecolor=goal_color, alpha=alpha, zorder=0)
            self.axes.add_patch(self.goal_patch_2d)
            self.draw_idle()

    def draw_maze_wall(self, x, y, wall_direction):
        """绘制迷宫墙体（根据模式选择2D或3D）"""
        # 保存墙体数据（wall_direction是位掩码，直接保存）
        self.wall_data_cache[(x, y)] = wall_direction
        
        if self.view_mode == "3D":
            self.draw_maze_wall_3d(x, y, wall_direction)
            return
        
        # 2D模式绘制
        # wall_direction is a bitmask based on CoordinateStateType
        # 0x01: Right wall (+X)
        # 0x02: Top wall (+Y)
        # 0x04: Left wall (-X)
        # 0x08: Bottom wall (-Y)

        line_width = 3.5
        line_color = '#1e293b'  # 现代化墙体颜色 - 更深更有质感
        highlight_color = '#f97316'
        highlight_width = 4.5

        # Key for drawn_walls dictionary: (x, y, direction_code)

        def _animate_wall(key, xs, ys):
            if key not in self.drawn_walls:
                wall = self.axes.plot(xs, ys, color=highlight_color, linewidth=highlight_width, alpha=0.0)[0]
                self.drawn_walls[key] = wall
                # 淡入动画
                for step, alpha in enumerate([0.3, 0.6, 0.9, 1.0]):
                    QTimer.singleShot(step * 40, lambda w=wall, a=alpha: (w.set_alpha(a), self.draw_idle()))
                # 恢复为正常颜色和线宽
                QTimer.singleShot(200, lambda w=wall: (w.set_color(line_color), w.set_linewidth(line_width), self.draw_idle()))
            else:
                self.drawn_walls[key].set_data(xs, ys)

        def _remove_wall(key):
            if key in self.drawn_walls:
                try:
                    self.drawn_walls[key].remove()
                except Exception:
                    pass
                del self.drawn_walls[key]

        # Right wall
        if (wall_direction & 0x01):
            _animate_wall((x, y, 'right'), [x + 1, x + 1], [y, y + 1])
        else:
            _remove_wall((x, y, 'right'))

        # Top wall
        if (wall_direction & 0x02):
            _animate_wall((x, y, 'top'), [x, x + 1], [y + 1, y + 1])
        else:
            _remove_wall((x, y, 'top'))

        # Left wall
        if (wall_direction & 0x04):
            _animate_wall((x, y, 'left'), [x, x], [y, y + 1])
        else:
            _remove_wall((x, y, 'left'))

        # Bottom wall
        if (wall_direction & 0x08):
            _animate_wall((x, y, 'bottom'), [x, x + 1], [y, y])
        else:
            _remove_wall((x, y, 'bottom'))

        self.draw()

    def update_plot(self, x, y, orientation, path_x, path_y):
        """更新显示（根据模式选择2D或3D）"""
        if self.view_mode == "3D":
            self.update_plot_3d(x, y, orientation, path_x, path_y)
            return
        
        # 2D模式更新
        self.mouse_pos.set_data([x], [y])

        # 使用渐隐尾迹：基于 path_x/path_y 构造带透明度的分段线条
        points = list(zip(path_x, path_y))
        self.path_points = points[-self.path_max_len:]

        if len(self.path_points) >= 2:
            segments = [
                [self.path_points[i], self.path_points[i + 1]]
                for i in range(len(self.path_points) - 1)
            ]
            n = len(segments)
            base_rgba = mcolors.to_rgba('#6366f1')
            # 尾迹渐隐（靠近末尾更亮，可调节渐隐强度）
            fade_power = getattr(self, "path_fade_power", 0.85)
            alphas = [0.08 + (0.92 * ((i + 1) / n) ** fade_power) for i in range(n)]
            colors = [(base_rgba[0], base_rgba[1], base_rgba[2], a) for a in alphas]
            self.path_collection.set_segments(segments)
            self.path_collection.set_color(colors)
        else:
            self.path_collection.set_segments([])

        # Remove old arrow if it exists
        if self.arrow:
            self.arrow.remove()
        
        # Draw new arrow for orientation
        dx, dy = 0, 0
        if orientation == 0: # North
            dx, dy = 0, 0.4
        elif orientation == 1: # East
            dx, dy = 0.4, 0
        elif orientation == 2: # South
            dx, dy = 0, -0.4
        elif orientation == 3: # West
            dx, dy = -0.4, 0
        
        # 现代化方向箭头 - 更精致
        self.arrow = self.axes.arrow(x, y, dx, dy, 
                                    head_width=0.24, head_length=0.24, 
                                    fc='#10b981', ec='#059669', 
                                    linewidth=2.0, zorder=15,
                                    alpha=0.95)

        self.draw()

    def _pulse_arrow(self):
        """方向箭头呼吸动效：轻微变化透明度/线宽"""
        if self.view_mode == "3D":
            if not self.arrow_3d:
                return
            self.arrow_phase = (self.arrow_phase + 0.2) % (2 * math.pi)
            alpha = 0.75 + 0.20 * (0.5 * (1 + math.sin(self.arrow_phase)))
            lw = 2.5 + 0.5 * (0.5 * (1 + math.sin(self.arrow_phase)))
            try:
                self.arrow_3d.set_alpha(alpha)
                self.arrow_3d.set_linewidth(lw)
                if self.arrow_head_3d:
                    self.arrow_head_3d.set_alpha(alpha)
                self.draw_idle()
            except Exception:
                pass
        else:
            if not self.arrow:
                return
            self.arrow_phase = (self.arrow_phase + 0.2) % (2 * math.pi)
            alpha = 0.75 + 0.20 * (0.5 * (1 + math.sin(self.arrow_phase)))
            lw = 1.8 + 0.4 * (0.5 * (1 + math.sin(self.arrow_phase)))
            try:
                self.arrow.set_alpha(alpha)
                self.arrow.set_linewidth(lw)
                self.draw_idle()
            except Exception:
                pass

    def set_tail_style(self, length: int, fade_power: float):
        """外部设置尾迹长度与渐隐强度"""
        self.path_max_len = max(10, int(length))
        self.path_fade_power = max(0.1, min(1.0, float(fade_power)))
    
    def toggle_view_mode(self):
        """切换2D/3D显示模式"""
        if self.view_mode == "2D":
            self.view_mode = "3D"
            self.setup_3d_plot()
        else:
            self.view_mode = "2D"
            self.setup_maze_plot()
        # 重新绘制所有已保存的墙体
        for (x, y), wall_mask in self.wall_data_cache.items():
            if wall_mask > 0:
                self.draw_maze_wall(x, y, wall_mask)
    
    def setup_3d_plot(self):
        """设置3D迷宫显示"""
        self.figure.clear()
        self.axes_3d = self.figure.add_subplot(111, projection='3d')
        
        # 设置3D视图参数 - 俯视角度，符合沙盘视图
        self.axes_3d.view_init(elev=75, azim=45)  # 俯视角度，稍微倾斜
        
        # 设置背景色 - 参考真实迷宫风格
        self.figure.patch.set_facecolor('#fafbfc')
        self.axes_3d.set_facecolor('#f8f9fa')  # 浅灰色底板，与整体风格一致
        
        # 设置坐标轴范围
        self.axes_3d.set_xlim(-0.5, 8.5)
        self.axes_3d.set_ylim(-0.5, 8.5)
        self.axes_3d.set_zlim(0, 0.05)  # 墙体高度范围（薄的长方形墙体）
        
        # 设置坐标轴标签（浅色，在深色背景上可见）
        self.axes_3d.set_xlabel('X', color='#9ca3af', fontsize=10)
        self.axes_3d.set_ylabel('Y', color='#9ca3af', fontsize=10)
        self.axes_3d.set_zlabel('Z', color='#9ca3af', fontsize=10)
        
        # 设置坐标轴颜色
        self.axes_3d.tick_params(axis='x', colors='#9ca3af', labelsize=9)
        self.axes_3d.tick_params(axis='y', colors='#9ca3af', labelsize=9)
        self.axes_3d.tick_params(axis='z', colors='#9ca3af', labelsize=9)
        
        # 设置标题 - 减少padding，让图更靠近顶部
        self.axes_3d.set_title("电脑鼠迷宫轨迹 (3D)", 
                               color='#0f172a', fontsize=16, fontweight='600', 
                               fontfamily='Microsoft YaHei', pad=8)
        
        # 绘制深灰色底板（模拟真实迷宫的底板）
        x_grid = np.arange(-0.5, 9.5, 0.1)
        y_grid = np.arange(-0.5, 9.5, 0.1)
        X_grid, Y_grid = np.meshgrid(x_grid, y_grid)
        Z_grid = np.zeros_like(X_grid)
        self.axes_3d.plot_surface(X_grid, Y_grid, Z_grid, alpha=0.9, color='#e2e8f0', 
                                  linewidth=0, antialiased=True, shade=True)
        
        # 初始化3D路径集合（亮蓝色，在深色背景上更清晰）
        self.path_collection_3d = Line3DCollection([], linewidths=3.5, colors='#3b82f6', alpha=0.9)
        self.axes_3d.add_collection3d(self.path_collection_3d)
        
        # 初始化3D小鼠位置（红色，在深色背景上更醒目）
        self.mouse_pos_3d, = self.axes_3d.plot([], [], [], 'o', color='#ef4444', 
                                               markersize=16, markeredgecolor='#ffffff', 
                                               markeredgewidth=3.0)
        
        # 减少绘图区域周围的边距，去掉无用背景
        self.figure.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.08)
        
        self.arrow_3d = None
        self.arrow_head_3d = None
        self.drawn_walls_3d = {}
        
        # 确保wall_data_cache已初始化
        if not hasattr(self, 'wall_data_cache'):
            self.wall_data_cache = {}
        
        self.draw()
        self._draw_goal_area_3d()
    
    def _draw_goal_area_3d(self):
        """在3D模式下绘制终点区域"""
        if hasattr(self.app_page, 'goal_min_x'):
            min_x = self.app_page.goal_min_x
            max_x = self.app_page.goal_max_x
            min_y = self.app_page.goal_min_y
            max_y = self.app_page.goal_max_y

            # 终点区域的颜色和透明度
            goal_color = '#a855f7'  # 紫色
            alpha = 0.2

            # 移除旧的终点区域绘制
            if hasattr(self, 'goal_patch_3d') and self.goal_patch_3d is not None:
                for patch in self.goal_patch_3d.collections:
                    patch.remove()
                self.goal_patch_3d = None

            # 绘制一个平面作为终点区域
            x_min, x_max = min_x, max_x + 1
            y_min, y_max = min_y, max_y + 1
            z_val = 0.001  # 略高于地面，防止被地面覆盖

            # 定义终点区域的四个角点
            vertices = [
                [x_min, y_min, z_val],
                [x_max, y_min, z_val],
                [x_max, y_max, z_val],
                [x_min, y_max, z_val]
            ]
            
            # 使用 Poly3DCollection 绘制平面
            self.goal_patch_3d = Poly3DCollection([vertices], facecolors=goal_color, alpha=alpha, zorder=0)
            self.axes_3d.add_collection3d(self.goal_patch_3d)
            self.draw_idle()

    def draw_maze_wall_3d(self, x, y, wall_direction):
        """在3D模式下绘制墙体 - 参考真实迷宫风格，水平长方形贴地放置"""
        wall_thickness = 0.02  # 墙体厚度（薄的长方形）
        wall_color = '#f5f5dc'  # 浅米色墙体，类似真实迷宫
        red_stripe_color = '#dc2626'  # 红色顶部条纹
        edge_color = '#d4d4d4'  # 浅灰色边缘
        highlight_color = '#f97316'  # 高亮颜色（动画用）
        stripe_thickness = 0.005  # 红色条纹厚度
        
        def _animate_wall_3d(key, vertices, top_vertices=None):
            if key not in self.drawn_walls_3d:
                # 创建3D墙体主体（浅米色）
                wall = Poly3DCollection([vertices], facecolors=highlight_color, 
                                       edgecolors=edge_color, linewidths=1.5, 
                                       alpha=0.0)
                self.axes_3d.add_collection3d(wall)
                
                # 创建顶部红色条纹
                red_stripe = None
                if top_vertices:
                    red_stripe = Poly3DCollection([top_vertices], facecolors=highlight_color,
                                                  edgecolors=red_stripe_color, linewidths=1.0,
                                                  alpha=0.0)
                    self.axes_3d.add_collection3d(red_stripe)
                
                self.drawn_walls_3d[key] = {'wall': wall, 'stripe': red_stripe}
                
                # 淡入动画
                for step, alpha in enumerate([0.3, 0.6, 0.9, 1.0]):
                    QTimer.singleShot(step * 40, lambda w=wall, s=red_stripe, a=alpha: (
                        w.set_alpha(a), 
                        s.set_alpha(a) if s else None, 
                        self.draw_idle()
                    ))
                # 恢复为正常颜色
                QTimer.singleShot(200, lambda w=wall, s=red_stripe: (
                    w.set_facecolor(wall_color), w.set_alpha(0.95),
                    s.set_facecolor(red_stripe_color) if s else None,
                    s.set_alpha(0.95) if s else None,
                    self.draw_idle()
                ))
            else:
                self.drawn_walls_3d[key]['wall'].set_verts([vertices])
                if top_vertices and self.drawn_walls_3d[key]['stripe']:
                    self.drawn_walls_3d[key]['stripe'].set_verts([top_vertices])
        
        def _remove_wall_3d(key):
            if key in self.drawn_walls_3d:
                try:
                    wall_obj = self.drawn_walls_3d[key]
                    if isinstance(wall_obj, dict):
                        if wall_obj['wall']:
                            wall_obj['wall'].remove()
                        if wall_obj.get('stripe'):
                            wall_obj['stripe'].remove()
                    else:
                        wall_obj.remove()
                except Exception:
                    pass
                del self.drawn_walls_3d[key]
        
        # Right wall (+X方向) - 水平长方形，长边沿Y方向贴地
        if (wall_direction & 0x01):
            # 墙体主体：薄的长方形，从(x+1, y, 0)到(x+1, y+1, wall_thickness)
            vertices = [
                [x + 1, y, 0],
                [x + 1, y + 1, 0],
                [x + 1, y + 1, wall_thickness - stripe_thickness],
                [x + 1, y, wall_thickness - stripe_thickness]
            ]
            # 顶部红色条纹
            top_vertices = [
                [x + 1, y, wall_thickness - stripe_thickness],
                [x + 1, y + 1, wall_thickness - stripe_thickness],
                [x + 1, y + 1, wall_thickness],
                [x + 1, y, wall_thickness]
            ]
            _animate_wall_3d((x, y, 'right'), vertices, top_vertices)
        else:
            _remove_wall_3d((x, y, 'right'))
        
        # Top wall (+Y方向) - 水平长方形，长边沿X方向贴地
        if (wall_direction & 0x02):
            # 墙体主体：薄的长方形，从(x, y+1, 0)到(x+1, y+1, wall_thickness)
            vertices = [
                [x, y + 1, 0],
                [x + 1, y + 1, 0],
                [x + 1, y + 1, wall_thickness - stripe_thickness],
                [x, y + 1, wall_thickness - stripe_thickness]
            ]
            # 顶部红色条纹
            top_vertices = [
                [x, y + 1, wall_thickness - stripe_thickness],
                [x + 1, y + 1, wall_thickness - stripe_thickness],
                [x + 1, y + 1, wall_thickness],
                [x, y + 1, wall_thickness]
            ]
            _animate_wall_3d((x, y, 'top'), vertices, top_vertices)
        else:
            _remove_wall_3d((x, y, 'top'))
        
        # Left wall (-X方向) - 水平长方形，长边沿Y方向贴地
        if (wall_direction & 0x04):
            # 墙体主体：薄的长方形，从(x, y, 0)到(x, y+1, wall_thickness)
            vertices = [
                [x, y, 0],
                [x, y + 1, 0],
                [x, y + 1, wall_thickness - stripe_thickness],
                [x, y, wall_thickness - stripe_thickness]
            ]
            # 顶部红色条纹
            top_vertices = [
                [x, y, wall_thickness - stripe_thickness],
                [x, y + 1, wall_thickness - stripe_thickness],
                [x, y + 1, wall_thickness],
                [x, y, wall_thickness]
            ]
            _animate_wall_3d((x, y, 'left'), vertices, top_vertices)
        else:
            _remove_wall_3d((x, y, 'left'))
        
        # Bottom wall (-Y方向) - 水平长方形，长边沿X方向贴地
        if (wall_direction & 0x08):
            # 墙体主体：薄的长方形，从(x, y, 0)到(x+1, y, wall_thickness)
            vertices = [
                [x, y, 0],
                [x + 1, y, 0],
                [x + 1, y, wall_thickness - stripe_thickness],
                [x, y, wall_thickness - stripe_thickness]
            ]
            # 顶部红色条纹
            top_vertices = [
                [x, y, wall_thickness - stripe_thickness],
                [x + 1, y, wall_thickness - stripe_thickness],
                [x + 1, y, wall_thickness],
                [x, y, wall_thickness]
            ]
            _animate_wall_3d((x, y, 'bottom'), vertices, top_vertices)
        else:
            _remove_wall_3d((x, y, 'bottom'))
        
        self.draw()
    
    def update_plot_3d(self, x, y, orientation, path_x, path_y):
        """更新3D模式下的显示"""
        # 更新小鼠位置（贴在地面上）
        self.mouse_pos_3d.set_data_3d([x], [y], [0.01])
        
        # 更新路径
        points = list(zip(path_x, path_y))
        self.path_points = points[-self.path_max_len:]
        
        if len(self.path_points) >= 2:
            segments = []
            for i in range(len(self.path_points) - 1):
                x1, y1 = self.path_points[i]
                x2, y2 = self.path_points[i + 1]
                segments.append([(x1, y1, 0.01), (x2, y2, 0.01)])  # 路径贴在地面上
            
            n = len(segments)
            base_rgba = mcolors.to_rgba('#3b82f6')  # 亮蓝色，在深色背景上更清晰
            fade_power = getattr(self, "path_fade_power", 0.85)
            alphas = [0.15 + (0.85 * ((i + 1) / n) ** fade_power) for i in range(n)]  # 提高最小透明度
            colors = [(base_rgba[0], base_rgba[1], base_rgba[2], a) for a in alphas]
            self.path_collection_3d.set_segments(segments)
            self.path_collection_3d.set_color(colors)
        else:
            self.path_collection_3d.set_segments([])
        
        # 移除旧箭头
        if self.arrow_3d:
            self.arrow_3d.remove()
            self.arrow_3d = None
        if self.arrow_head_3d:
            self.arrow_head_3d.remove()
            self.arrow_head_3d = None
        
        # 绘制3D方向箭头
        dx, dy = 0, 0
        if orientation == 0:  # North
            dx, dy = 0, 0.4
        elif orientation == 1:  # East
            dx, dy = 0.4, 0
        elif orientation == 2:  # South
            dx, dy = 0, -0.4
        elif orientation == 3:  # West
            dx, dy = -0.4, 0
        
        # 3D箭头（使用线条表示，贴在地面上）
        self.arrow_3d = self.axes_3d.plot([x, x + dx], [y, y + dy], [0.01, 0.01], 
                                         color='#10b981', linewidth=3.0, alpha=0.95)[0]
        # 添加箭头头部
        if orientation == 0:  # North
            head_x, head_y = x, y + dy
        elif orientation == 1:  # East
            head_x, head_y = x + dx, y
        elif orientation == 2:  # South
            head_x, head_y = x, y + dy
        else:  # West
            head_x, head_y = x + dx, y
        self.arrow_head_3d = self.axes_3d.scatter([head_x], [head_y], [0.01], c='#10b981', s=100, alpha=0.95)
        
        self.draw()
    

class MicroMouseApp(QMainWindow):
    def __init__(self, as_page: bool = False):
        super().__init__()
        self.as_page = as_page
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        # 默认更宽、更扁：减少纵向滚动需求
        self.setGeometry(80, 80, 1400, 760)
        self.setMinimumSize(1180, 640)

        self.serial = QSerialPort()
        self.rx_buffer = ""
        self.serial.readyRead.connect(self.read_serial_data)
        
        # 默认起点改为右下角 (7,0) —— 画布以格子中心显示，故加 0.5 偏移
        self.mouse_current_x = 7.5
        self.mouse_current_y = 0.5
        self.mouse_orientation = 0 # 0: North, 1: East, 2: South, 3: West
        self.gyro_angle = 0.0  # 陀螺仪角度（度）
        self.run_mode = "停止"  # 运行模式：停止、迷宫模式
        self.mouse_path_x = [self.mouse_current_x]
        self.mouse_path_y = [self.mouse_current_y]
        # 轨迹回放存储
        self.replay_runs = []
        
        # 路径优化相关
        # 终点区域：3,3 到 4,4 之间（含边界）
        self.goal_min_x = 3
        self.goal_max_x = 4
        self.goal_min_y = 3
        self.goal_max_y = 4
        self.optimized_paths = []  # 存储优化后的路径列表
        self.current_run_path = []  # 当前运行的路径（格子坐标）
        self.has_reached_goal = False  # 是否已到达终点
        self.best_path_info = None  # 最优路径（长度最短）
        self.max_replay_saved = 60  # 回放列表最多保留条数，超出删除最旧
        self.wall_map = {}  # {(x,y): wall_mask} 记录已知墙体
        self.auto_send_best_path = False  # 是否到达终点后自动发送最优路径
        self.default_view_mode = "2D"  # 默认视图模式

        # Settings init
        self.settings = QSettings("MicromouseLab", "MicromouseApp")
        self.theme_pref = self.settings.value("general/theme", "light")
        self.pref_show_sidebar = self.settings.value("general/showSidebarOnStart", True, type=bool)

        # Apply font and theme first
        # 全局字体与控件基线尺寸：适配更宽界面同时避免纵向撑高
        self.setFont(QFont("Microsoft YaHei", 11))
        # Fix Matplotlib Chinese font & minus sign
        rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
        rcParams["axes.unicode_minus"] = False
        self.apply_theme()
        # 统一字体/高度，避免按钮过大或过小
        self.setStyleSheet(
            """
            QWidget { font-size: 13px; }
            QPushButton {
                min-height: 38px;
                font-size: 14px;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                min-height: 36px;
                font-size: 13px;
            }
            QTextEdit {
                font-size: 13px;
            }
            """
        )

        # Base widgets and layout
        self.central_widget = QWidget()
        if not self.as_page:
            self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 顶部轻量状态条（连接/速率/模式 + 长任务进度）
        self.top_status_widget = self._build_top_status_bar()
        self.layout.addWidget(self.top_status_widget)
        self._set_connection_state(False)
        self._set_run_mode("空闲", busy=False)
        self._set_data_state("无连接", "#cbd5e1", "数据状态")

        # Menus / status bar
        if not self.as_page:
            self.init_menu_bar()
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)

        # For realtime log subscribers (需要在init_ui之前初始化，因为页面可能访问它)
        self.log_subscribers = []  # list of callables: fn(timestamp, direction, text)
        
        # Main UI
        self.init_ui()
        if not self.as_page:
            self.status_bar.showMessage("就绪")

        # Apply persisted preferences
        self.apply_settings_to_ui()
        self.error_frame_count = 0
        self.bytes_received_window = deque(maxlen=200)
        self.bytes_sent_window = deque(maxlen=200)
        self.last_data_time = None  # 最后接收数据的时间
        self.frame_count = 0  # 接收到的帧数
        self._throughput_timer = QTimer(self)
        self._throughput_timer.setInterval(500)
        self._throughput_timer.timeout.connect(self._purge_old_bytes)
        self._throughput_timer.start()
        
        # 数据状态更新定时器
        self._data_status_timer = QTimer(self)
        self._data_status_timer.setInterval(1000)  # 每秒更新一次
        self._data_status_timer.timeout.connect(self._update_data_status)
        self._data_status_timer.start()
        
        # 串口自动刷新定时器
        self._port_refresh_timer = QTimer(self)
        self._port_refresh_timer.setInterval(2000)  # 每2秒刷新一次
        self._port_refresh_timer.timeout.connect(self.populate_ports)
        self._port_refresh_timer.start()

    # ------------------------------ UI Helpers ------------------------------
    def _icon(self, key: str):
        """统一图标出口：优先 FluentIcon，其次 Qt 标准图标"""
        mapping = {
            "refresh": (getattr(FIF, "SYNC", None) if QFW_AVAILABLE else QStyle.SP_BrowserReload),
            "connect": (getattr(FIF, "CONNECT", None) if QFW_AVAILABLE else QStyle.SP_DialogApplyButton),
            "disconnect": (getattr(FIF, "DISCONNECT", None) if QFW_AVAILABLE else QStyle.SP_DialogCancelButton),
            "sidebar": (getattr(FIF, "NAVIGATION", None) if QFW_AVAILABLE else QStyle.SP_ArrowLeft),
            "help": (getattr(FIF, "HELP", None) if QFW_AVAILABLE else QStyle.SP_DialogHelpButton),
            "about": (getattr(FIF, "INFO", None) if QFW_AVAILABLE else QStyle.SP_MessageBoxInformation),
            "send": (getattr(FIF, "SEND", None) if QFW_AVAILABLE else QStyle.SP_DialogYesButton),
            "start": (getattr(FIF, "PLAY", None) if QFW_AVAILABLE else QStyle.SP_MediaPlay),
            "stop": (getattr(FIF, "STOP", None) if QFW_AVAILABLE else QStyle.SP_MediaStop),
            "reset": (getattr(FIF, "SYNC", None) if QFW_AVAILABLE else QStyle.SP_BrowserReload),
            "rescue_left": (getattr(FIF, "ARROW_LEFT", None) if QFW_AVAILABLE else QStyle.SP_ArrowLeft),
            "rescue_right": (getattr(FIF, "ARROW_RIGHT", None) if QFW_AVAILABLE else QStyle.SP_ArrowRight),
            "send_path": (getattr(FIF, "SEND", None) if QFW_AVAILABLE else QStyle.SP_ArrowRight),
        }
        icon_obj = mapping.get(key)
        if icon_obj is None:
            return QIcon()
        try:
            if QFW_AVAILABLE and hasattr(icon_obj, "icon"):
                return icon_obj.icon()
        except Exception:
            pass
        if isinstance(icon_obj, QStyle.StandardPixmap):
            return self.style().standardIcon(icon_obj)
        return QIcon()

    def _mark_secondary(self, button: QPushButton):
        """给次要操作设置描边/浅色风格"""
        button.setProperty("class", "secondary")
        button.style().unpolish(button)
        button.style().polish(button)
        button.update()

    def _build_top_status_bar(self) -> QWidget:
        """顶部状态条：彩色点 + 标签 + 长任务进度"""
        wrap = QWidget()
        layout = QHBoxLayout(wrap)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(14)

        def make_chip(title: str, color: str, text: str):
            chip = QWidget()
            h = QHBoxLayout(chip)
            h.setContentsMargins(10, 6, 10, 6)
            h.setSpacing(8)
            chip.setStyleSheet(
                "QWidget { background:#ffffff; border:1px solid #e0e0e0; border-radius:16px; }"
            )
            dot = QLabel()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"background:{color}; border-radius:8px; border:1px solid #e0e0e0;")
            label = QLabel(text)
            sub = QLabel(title)
            sub.setStyleSheet("color:#6b7280; font-size:11px;")
            h.addWidget(dot)
            h.addWidget(label)
            h.addWidget(sub)
            return chip, dot, label, sub

        # 连接状态
        self.conn_chip, self.conn_dot, self.conn_label, self.conn_sub = make_chip("连接状态", "#94a3b8", "未连接")
        layout.addWidget(self.conn_chip)

        # 运行模式
        self.mode_chip, self.mode_dot, self.mode_label, self.mode_sub = make_chip("运行模式", "#cbd5e1", "空闲")
        layout.addWidget(self.mode_chip)

        # 数据状态
        self.data_chip, self.data_dot, self.data_label, self.data_sub = make_chip("数据状态", "#cbd5e1", "无数据")
        layout.addWidget(self.data_chip)

        layout.addStretch(1)

        # 长任务进度条
        self.long_task_wrap = QWidget()
        lt = QHBoxLayout(self.long_task_wrap)
        lt.setContentsMargins(8, 4, 8, 4)
        lt.setSpacing(8)
        self.long_task_label = QLabel("正在处理...")
        self.long_task_progress = QProgressBar()
        self.long_task_progress.setRange(0, 0)
        self.long_task_progress.setTextVisible(True)
        self.long_task_progress.setFixedHeight(14)
        self.long_task_progress.setMinimumWidth(220)
        lt.addWidget(self.long_task_label)
        lt.addWidget(self.long_task_progress)
        self.long_task_wrap.hide()
        layout.addWidget(self.long_task_wrap)

        return wrap

    def _set_chip_state(self, dot: QLabel, label: QLabel, sub: QLabel, color: str, text: str, subtitle: str):
        dot.setStyleSheet(f"background:{color}; border-radius:8px; border:1px solid #e0e0e0;")
        label.setText(text)
        sub.setText(subtitle)

    def _set_connection_state(self, connected: bool, port: str = "", baud: str = ""):
        color = "#22c55e" if connected else "#94a3b8"
        text = f"{port} 已连接" if connected and port else "未连接"
        subtitle = f"@{baud}" if connected and baud else "串口状态"
        self._set_chip_state(self.conn_dot, self.conn_label, self.conn_sub, color, text, subtitle)

    def _set_run_mode(self, mode_text: str, busy: bool = False):
        color = "#6366f1" if busy else "#cbd5e1"
        self._set_chip_state(self.mode_dot, self.mode_label, self.mode_sub, color, mode_text, "运行模式")

    def _set_data_state(self, text: str, color: str = "#cbd5e1", subtitle: str = "数据状态"):
        """更新数据状态显示"""
        self._set_chip_state(self.data_dot, self.data_label, self.data_sub, color, text, subtitle)

    def _update_data_status(self):
        """更新数据状态显示"""
        if not self.serial.isOpen():
            self._set_data_state("无连接", "#cbd5e1", "数据状态")
            return
        
        current_time = time.time()
        
        # 检查是否有数据接收
        if self.last_data_time is None:
            self._set_data_state("等待数据", "#f59e0b", "数据状态")
            return
        
        # 计算距离最后接收数据的时间
        time_since_last = current_time - self.last_data_time
        
        if time_since_last < 2.0:
            # 最近2秒内有数据接收，显示正常
            if self.error_frame_count == 0:
                status_text = f"{self.frame_count}帧"
                color = "#22c55e"  # 绿色
                subtitle = "数据正常"
            else:
                status_text = f"{self.frame_count}帧"
                color = "#f59e0b"  # 橙色
                subtitle = f"错误{self.error_frame_count}"
        elif time_since_last < 5.0:
            # 2-5秒没有数据，警告
            status_text = f"{int(time_since_last)}秒前"
            color = "#f59e0b"  # 橙色
            subtitle = "数据延迟"
        else:
            # 超过5秒没有数据，错误
            status_text = f"{int(time_since_last)}秒前"
            color = "#ef4444"  # 红色
            subtitle = "数据中断"
        
        self._set_data_state(status_text, color, subtitle)

    def show_long_task(self, text: str = "正在处理..."):
        self.long_task_label.setText(text)
        self.long_task_progress.setRange(0, 0)
        self.long_task_wrap.show()

    def finish_long_task(self, text: str = "完成", delay_ms: int = 700):
        self.long_task_label.setText(text)
        self.long_task_progress.setRange(0, 1)
        self.long_task_progress.setValue(1)
        QTimer.singleShot(delay_ms, self.long_task_wrap.hide)

    def show_toast(self, text: str, level: str = "info", duration: int = 2000):
        """轻量提示：优先 InfoBar，fallback 半透明标签"""
        if QFW_AVAILABLE:
            try:
                if level == "success":
                    InfoBar.success(title="成功", content=text, position=InfoBarPosition.TOP_RIGHT, parent=self, duration=duration)
                    return
                if level == "error":
                    InfoBar.error(title="错误", content=text, position=InfoBarPosition.TOP_RIGHT, parent=self, duration=duration)
                    return
                if level == "warning":
                    InfoBar.warning(title="提示", content=text, position=InfoBarPosition.TOP_RIGHT, parent=self, duration=duration)
                    return
                InfoBar.info(title="提示", content=text, position=InfoBarPosition.TOP_RIGHT, parent=self, duration=duration)
                return
            except Exception:
                pass

        bg_map = {"success": "#16a34a", "error": "#dc2626", "warning": "#f59e0b", "info": "#0ea5e9"}
        bg = bg_map.get(level, "#0ea5e9")
        label = QLabel(text, self)
        label.setStyleSheet(
            f"color:white; background:{bg}; padding:12px 18px; border-radius:16px; "
            f"border:none;"
        )
        label.adjustSize()
        label.move(self.width() - label.width() - 24, 16)
        label.show()
        QTimer.singleShot(duration, label.deleteLater)

    def init_menu_bar(self):
        menu_bar: QMenuBar = self.menuBar()
        device_menu = menu_bar.addMenu("设备")
        view_menu = menu_bar.addMenu("视图")
        help_menu = menu_bar.addMenu("帮助")

        self.act_refresh = QAction(self._icon("refresh"), "刷新串口", self)
        self.act_connect = QAction(self._icon("connect"), "连接", self)
        self.act_disconnect = QAction(self._icon("disconnect"), "断开", self)
        self.act_toggle_sidebar = QAction(self._icon("sidebar"), "隐藏侧栏", self)
        self.act_toggle_sidebar.setCheckable(True)
        self.act_help = QAction(self._icon("help"), "使用说明", self)
        self.act_about = QAction(self._icon("about"), "关于", self)

        device_menu.addAction(self.act_refresh)
        device_menu.addSeparator()
        device_menu.addAction(self.act_connect)
        device_menu.addAction(self.act_disconnect)
        view_menu.addAction(self.act_toggle_sidebar)
        help_menu.addAction(self.act_help)
        help_menu.addAction(self.act_about)

        # Wire actions
        self.act_refresh.triggered.connect(self.populate_ports)
        self.act_connect.triggered.connect(self.connect_serial)
        self.act_disconnect.triggered.connect(self.disconnect_serial)
        self.act_help.triggered.connect(self.show_help)
        self.act_about.triggered.connect(self.show_about_dialog)
        self.act_toggle_sidebar.toggled.connect(self.toggle_sidebar)

    def init_ui(self):
        # 创建主布局：左侧导航栏 + 右侧内容区域
        main_h_layout = QHBoxLayout()
        main_h_layout.setContentsMargins(0, 0, 0, 0)
        main_h_layout.setSpacing(0)
        
        # 创建左侧导航栏
        self.nav_bar = NavigationBar(self)
        self.nav_bar.itemClicked.connect(self.on_nav_item_clicked)
        main_h_layout.addWidget(self.nav_bar)
        
        # 创建右侧内容区域（使用QStackedWidget）
        self.content_stack = QStackedWidget()
        main_h_layout.addWidget(self.content_stack, 1)
        
        # 创建各个页面
        self.create_main_control_page()  # 主控制页面
        self.create_realtime_log_page()  # 实时日志页面
        self.create_replay_page()  # 轨迹回放页面
        self.create_settings_page()  # 设置页面
        self.create_docs_page()  # 文档页面
        self.create_about_page()  # 关于页面
        
        # 将主布局添加到central widget
        content_widget = QWidget()
        content_widget.setLayout(main_h_layout)
        self.layout.addWidget(content_widget)
        
        # 默认显示主控制页面
        self.content_stack.setCurrentIndex(0)
    
    def on_nav_item_clicked(self, index):
        """处理导航栏点击事件"""
        self.content_stack.setCurrentIndex(index)
    
    def create_main_control_page(self):
        """创建主控制页面 - 重新规划布局，现代化设计"""
        page = QWidget()
        page.setStyleSheet("background-color: #f8fafc;")
        page_layout = QHBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)
        
        # 左侧控制面板 - 双列网格，减少纵向长度
        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: #f8fafc;")
        # 限制宽度，避免在大屏上过宽导致控件显得“散”
        left_panel.setMaximumWidth(520)
        left_grid = QGridLayout(left_panel)
        left_grid.setContentsMargins(16, 16, 16, 16)
        left_grid.setHorizontalSpacing(16)
        left_grid.setVerticalSpacing(14)
        
        # Serial Port Configuration - 重新设计为更紧凑的两列布局
        serial_group = QGroupBox("串口配置")
        serial_config_layout = QGridLayout()
        serial_config_layout.setContentsMargins(16, 20, 16, 16)
        serial_config_layout.setHorizontalSpacing(12)
        serial_config_layout.setVerticalSpacing(12)
        
        # 第一行：串口和波特率
        self.port_label = QLabel("串口:")
        self.port_label.setStyleSheet("font-weight: 500; color: #475569;")
        serial_config_layout.addWidget(self.port_label, 0, 0)
        
        self.port_selector = QComboBox()
        self.populate_ports()
        self.port_selector.setFixedHeight(38)
        serial_config_layout.addWidget(self.port_selector, 0, 1, 1, 2)

        self.baud_label = QLabel("波特率:")
        self.baud_label.setStyleSheet("font-weight: 500; color: #475569;")
        serial_config_layout.addWidget(self.baud_label, 0, 3)

        common_baud_rates = [
            "9600", "19200", "38400", "57600",
            "115200", "230400", "460800", "921600"
        ]
        self.baud_rate_selector = QComboBox()
        self.baud_rate_selector.addItems(common_baud_rates)
        self.baud_rate_selector.setCurrentText("115200")
        self.baud_rate_selector.setFixedHeight(38)
        serial_config_layout.addWidget(self.baud_rate_selector, 0, 4, 1, 2)

        # 第二行：数据位、停止位、校验位
        self.data_bits_label = QLabel("数据位:")
        self.data_bits_label.setStyleSheet("font-weight: 500; color: #475569;")
        serial_config_layout.addWidget(self.data_bits_label, 1, 0)
        self.data_bits_selector = QComboBox()
        self.data_bits_selector.addItems(["5", "6", "7", "8"])
        self.data_bits_selector.setCurrentText("8")
        self.data_bits_selector.setFixedHeight(38)
        serial_config_layout.addWidget(self.data_bits_selector, 1, 1)

        self.stop_bits_label = QLabel("停止位:")
        self.stop_bits_label.setStyleSheet("font-weight: 500; color: #475569;")
        serial_config_layout.addWidget(self.stop_bits_label, 1, 2)
        self.stop_bits_selector = QComboBox()
        self.stop_bits_selector.addItems(["1", "1.5", "2"])
        self.stop_bits_selector.setCurrentText("1")
        self.stop_bits_selector.setFixedHeight(38)
        serial_config_layout.addWidget(self.stop_bits_selector, 1, 3)

        self.parity_label = QLabel("校验位:")
        self.parity_label.setStyleSheet("font-weight: 500; color: #475569;")
        serial_config_layout.addWidget(self.parity_label, 1, 4)
        self.parity_selector = QComboBox()
        self.parity_selector.addItems(["无", "奇", "偶", "Mark", "Space"])
        self.parity_selector.setCurrentText("无")
        self.parity_selector.setFixedHeight(38)
        serial_config_layout.addWidget(self.parity_selector, 1, 5)

        # 第三行：连接和断开按钮 - 美化设计
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.connect_button = QPushButton("连接")
        icon = self._icon("connect")
        if not icon.isNull():
            self.connect_button.setIcon(icon)
            self.connect_button.setIconSize(QSize(18, 18))
        self.connect_button.setFixedHeight(42)
        self.connect_button.setProperty("class", "primary")
        self.connect_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: #ffffff;
                border: none;
                border-radius: 16px;
                font-weight: 600;
                font-size: 14px;
                padding: 0px 24px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #9e9e9e;
            }
        """)
        button_layout.addWidget(self.connect_button)

        self.disconnect_button = QPushButton("断开")
        icon_disconnect = self._icon("disconnect")
        if not icon_disconnect.isNull():
            self.disconnect_button.setIcon(icon_disconnect)
            self.disconnect_button.setIconSize(QSize(18, 18))
        self.disconnect_button.setEnabled(False)
        self.disconnect_button.setFixedHeight(42)
        self.disconnect_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #f44336;
                border: 2px solid #f44336;
                border-radius: 16px;
                font-weight: 600;
                font-size: 14px;
                padding: 0px 24px;
            }
            QPushButton:hover {
                background-color: #ffebee;
                border-color: #e53935;
            }
            QPushButton:pressed {
                background-color: #ffcdd2;
                border-color: #c62828;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #9e9e9e;
                border-color: #e0e0e0;
            }
        """)
        button_layout.addWidget(self.disconnect_button)
        
        serial_config_layout.addLayout(button_layout, 2, 0, 1, 6)

        self.connect_button.clicked.connect(self.connect_serial)
        self.disconnect_button.clicked.connect(self.disconnect_serial)

        serial_group.setLayout(serial_config_layout)

        # Serial Data Send - 美化设计
        send_group = QGroupBox("发送数据")
        send_main_layout = QVBoxLayout()
        send_main_layout.setContentsMargins(16, 20, 16, 16)
        send_main_layout.setSpacing(12)
        
        # 输入框和发送按钮在同一行
        send_input_layout = QHBoxLayout()
        send_input_layout.setSpacing(10)
        self.send_data_input = QLineEdit()
        self.send_data_input.setPlaceholderText("输入要发送的数据")
        self.send_data_input.setFixedHeight(42)
        self.send_data_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 16px;
                padding: 0px 20px;
                font-size: 13px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #2196f3;
                background-color: #ffffff;
            }
            QLineEdit:hover {
                border: 2px solid #bdbdbd;
            }
        """)
        send_input_layout.addWidget(self.send_data_input, 1)

        self.send_button = QPushButton("发送")
        icon_send = self._icon("send")
        if not icon_send.isNull():
            self.send_button.setIcon(icon_send)
            self.send_button.setIconSize(QSize(18, 18))
        self.send_button.setEnabled(False)
        self.send_button.setFixedWidth(100)
        self.send_button.setFixedHeight(42)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: #ffffff;
                border: none;
                border-radius: 16px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #1565c0;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #9e9e9e;
            }
        """)
        send_input_layout.addWidget(self.send_button)
        send_main_layout.addLayout(send_input_layout)
        
        # Protocol hint - 美化提示信息
        self.protocol_hint = QLabel(
            "协议帧: s,X,Y,O,Angle,Front,Left,Right,Mode\\r\\n"
            "X/Y:0-7, O:0北1东2南3西, Angle:角度(度), 传感器:0有墙/1没墙, Mode:0停止/1迷宫模式"
        )
        self.protocol_hint.setWordWrap(True)
        self.protocol_hint.setStyleSheet("""
            color: #757575; 
            font-size: 11px; 
            padding: 12px 16px;
            background-color: #f5f5f5;
            border-radius: 16px;
            border: 1px solid #e0e0e0;
        """)
        send_main_layout.addWidget(self.protocol_hint)
        send_group.setLayout(send_main_layout)

        self.send_button.clicked.connect(self.send_serial_data)

        # Maze Plotter - 现在占据整个右侧区域
        self.maze_plotter = MazePlotter(self, self)

        # Right side: 迷宫绘图区域 + 指南针（放在右上角）- 美化设计
        plot_wrap = QGroupBox("迷宫与轨迹")
        pv = QVBoxLayout()
        pv.setContentsMargins(20, 16, 20, 20)  # 减少上边距，让轨迹图更靠近顶部
        pv.setSpacing(8)  # 减少间距
        
        # 创建顶部布局：指南针和切换按钮在右上角
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)
        top_layout.addStretch(1)  # 左侧弹性空间
        
        # 2D/3D切换按钮 - 美化设计
        self.view_toggle_button = QPushButton("3D视图", self)
        self.view_toggle_button.setFixedSize(90, 36)
        self.view_toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #2196f3;
                border: 2px solid #2196f3;
                border-radius: 16px;
                font-size: 13px;
                font-weight: 600;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
                border-color: #1976d2;
                color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #bbdefb;
                border-color: #1565c0;
                color: #1565c0;
            }
        """)
        self.view_toggle_button.clicked.connect(self.toggle_maze_view)
        top_layout.addWidget(self.view_toggle_button, alignment=Qt.AlignTop | Qt.AlignRight)
        
        # 指南针组件（缩小尺寸，放在右上角）
        self.compass_widget = CompassWidget(self)
        top_layout.addWidget(self.compass_widget, alignment=Qt.AlignTop | Qt.AlignRight)
        top_layout.setAlignment(self.compass_widget, Qt.AlignTop | Qt.AlignRight)
        
        pv.addLayout(top_layout)
        pv.addWidget(self.maze_plotter, 1)  # 迷宫图占据剩余空间
        plot_wrap.setLayout(pv)

        # 左侧面板已在上方创建，这里添加组件
        left_grid.addWidget(serial_group, 0, 0, 1, 2)
        left_grid.addWidget(send_group, 1, 0, 1, 2)

        # Control Panel Group - 重新设计为网格布局，更美观
        control_group = QGroupBox("控制面板")
        control_layout = QGridLayout()
        control_layout.setContentsMargins(16, 20, 16, 16)
        control_layout.setHorizontalSpacing(10)
        control_layout.setVerticalSpacing(10)

        # 开始按钮 - 主要操作，使用绿色
        self.start_button = QPushButton("▶ 开始")
        icon_start = self._icon("start")
        if not icon_start.isNull():
            self.start_button.setIcon(icon_start)
            self.start_button.setIconSize(QSize(18, 18))
        self.start_button.setFixedHeight(48)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: #ffffff;
                border: none;
                border-radius: 20px;
                font-weight: 600;
                font-size: 15px;
                padding: 0px 24px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #9e9e9e;
            }
        """)
        control_layout.addWidget(self.start_button, 0, 0, 1, 2)

        # 停止和复位按钮 - 使用网格布局
        self.stop_button = QPushButton("■ 停止")
        icon_stop = self._icon("stop")
        if not icon_stop.isNull():
            self.stop_button.setIcon(icon_stop)
            self.stop_button.setIconSize(QSize(18, 18))
        self.stop_button.setFixedHeight(44)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #f44336;
                border: 2px solid #f44336;
                border-radius: 16px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ffebee;
                border-color: #e53935;
            }
            QPushButton:pressed {
                background-color: #ffcdd2;
                border-color: #c62828;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #9e9e9e;
                border-color: #e0e0e0;
            }
        """)
        control_layout.addWidget(self.stop_button, 1, 0)

        self.reset_button = QPushButton("↻ 复位")
        icon_reset = self._icon("reset")
        if not icon_reset.isNull():
            self.reset_button.setIcon(icon_reset)
            self.reset_button.setIconSize(QSize(18, 18))
        self.reset_button.setFixedHeight(44)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #ff9800;
                border: 2px solid #ff9800;
                border-radius: 16px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #fff3e0;
                border-color: #fb8c00;
            }
            QPushButton:pressed {
                background-color: #ffe0b2;
                border-color: #f57c00;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #9e9e9e;
                border-color: #e0e0e0;
            }
        """)
        control_layout.addWidget(self.reset_button, 1, 1)

        # 救援按钮区域 - 使用网格布局
        self.rescue_left_button = QPushButton("← 左救援")
        icon_rescue_left = self._icon("rescue_left")
        if not icon_rescue_left.isNull():
            self.rescue_left_button.setIcon(icon_rescue_left)
            self.rescue_left_button.setIconSize(QSize(18, 18))
        self.rescue_left_button.setFixedHeight(44)
        self.rescue_left_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #2196f3;
                border: 2px solid #2196f3;
                border-radius: 16px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
                border-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #bbdefb;
                border-color: #1565c0;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #9e9e9e;
                border-color: #e0e0e0;
            }
        """)
        control_layout.addWidget(self.rescue_left_button, 2, 0)

        self.rescue_right_button = QPushButton("→ 右救援")
        icon_rescue_right = self._icon("rescue_right")
        if not icon_rescue_right.isNull():
            self.rescue_right_button.setIcon(icon_rescue_right)
            self.rescue_right_button.setIconSize(QSize(18, 18))
        self.rescue_right_button.setFixedHeight(44)
        self.rescue_right_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #2196f3;
                border: 2px solid #2196f3;
                border-radius: 16px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
                border-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #bbdefb;
                border-color: #1565c0;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #9e9e9e;
                border-color: #e0e0e0;
            }
        """)
        control_layout.addWidget(self.rescue_right_button, 2, 1)

        # 发送优化路径按钮 - 跨两列
        self.send_path_button = QPushButton("📤 发送优化路径")
        icon_send_path = self._icon("send_path")
        if not icon_send_path.isNull():
            self.send_path_button.setIcon(icon_send_path)
            self.send_path_button.setIconSize(QSize(18, 18))
        self.send_path_button.setFixedHeight(44)
        self.send_path_button.setStyleSheet("""
            QPushButton {
                background-color: #9c27b0;
                color: #ffffff;
                border: none;
                border-radius: 16px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8e24aa;
            }
            QPushButton:pressed {
                background-color: #7b1fa2;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #9e9e9e;
            }
        """)
        control_layout.addWidget(self.send_path_button, 3, 0, 1, 2)

        control_group.setLayout(control_layout)
        left_grid.addWidget(control_group, 2, 0)

        self.start_button.clicked.connect(self.start_mouse)
        self.stop_button.clicked.connect(self.stop_mouse)
        self.reset_button.clicked.connect(self.reset_mouse)
        self.rescue_left_button.clicked.connect(self.rescue_left)
        self.rescue_right_button.clicked.connect(self.rescue_right)
        self.send_path_button.clicked.connect(self.send_optimized_path)

        # Sensor Data Group - 美化设计，使用网格布局
        sensor_group = QGroupBox("传感器数据")
        sensor_layout = QGridLayout()
        sensor_layout.setContentsMargins(16, 20, 16, 16)
        sensor_layout.setHorizontalSpacing(12)
        sensor_layout.setVerticalSpacing(12)

        self.sensor_labels = {}
        sensor_names = [
            ("左传感器:", "left"),
            ("右传感器:", "right"),
            ("前传感器:", "front"),
            ("电池电压:", "battery")
        ]
        
        row = 0
        for name, key in sensor_names:
            label = QLabel(name)
            label.setStyleSheet("font-weight: 500; color: #475569; font-size: 13px;")
            sensor_layout.addWidget(label, row, 0)
            
            value_label = QLabel("N/A")
            value_label.setObjectName("sensor_value_label")
            value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            value_label.setStyleSheet("""
                QLabel#sensor_value_label {
                    font-weight: 600;
                    color: #1976d2;
                    font-size: 14px;
                    padding: 10px 18px;
                    background: #e3f2fd;
                    border-radius: 16px;
                    border: 1px solid #bbdefb;
                    min-width: 80px;
                }
            """)
            self.sensor_labels[name] = value_label
            sensor_layout.addWidget(value_label, row, 1)
            row += 1

        sensor_group.setLayout(sensor_layout)
        left_grid.addWidget(sensor_group, 2, 1)

        left_grid.setRowStretch(3, 1)
        self.left_panel = left_panel

        # Top-level horizontal splitter: left controls (minor), right plot (major)
        h_splitter = QSplitter(Qt.Horizontal)
        h_splitter.addWidget(left_panel)
        h_splitter.addWidget(plot_wrap)
        h_splitter.setStretchFactor(0, 1)
        h_splitter.setStretchFactor(1, 10)
        # Initial sizes: left more compact, right wider for plot
        h_splitter.setSizes([380, 1200])  # 增加左侧宽度以适应新的布局
        self.h_splitter = h_splitter
        
        page_layout.addWidget(h_splitter)
        self.content_stack.addWidget(page)
    
    def create_realtime_log_page(self):
        """创建实时日志页面"""
        if hasattr(self, '_realtime_log_page'):
            page = self._realtime_log_page
        else:
            page = RealtimeLogPage(self, self)
            self._realtime_log_page = page
        self.content_stack.addWidget(page)
    
    def create_replay_page(self):
        """创建轨迹回放页面"""
        if hasattr(self, '_replay_page'):
            page = self._replay_page
        else:
            page = ReplayPage(self, self)
            self._replay_page = page
        self.content_stack.addWidget(page)
    
    def create_settings_page(self):
        """创建设置页面"""
        if hasattr(self, '_settings_page'):
            page = self._settings_page
        else:
            page = SettingsPage(self, self)
            self._settings_page = page
        self.content_stack.addWidget(page)
    
    def create_docs_page(self):
        """创建文档页面"""
        if hasattr(self, '_docs_page'):
            page = self._docs_page
        else:
            page = DocsPage(self)
            self._docs_page = page
        self.content_stack.addWidget(page)
    
    def create_about_page(self):
        """创建关于页面"""
        if hasattr(self, '_about_page'):
            page = self._about_page
        else:
            page = AboutPage(self)
            self._about_page = page
        self.content_stack.addWidget(page)

    def toggle_maze_view(self):
        """切换迷宫2D/3D视图"""
        if hasattr(self, "maze_plotter"):
            self.maze_plotter.toggle_view_mode()
            # 更新按钮文本
            if self.maze_plotter.view_mode == "3D":
                self.view_toggle_button.setText("2D视图")
                if hasattr(self, "status_bar"):
                    self.status_bar.showMessage("已切换到3D视图", 2000)
            else:
                self.view_toggle_button.setText("3D视图")
                if hasattr(self, "status_bar"):
                    self.status_bar.showMessage("已切换到2D视图", 2000)
            # 如果有当前位置数据，重新更新显示
            if hasattr(self, "mouse_current_x") and hasattr(self, "mouse_current_y"):
                if hasattr(self, "mouse_path_x") and hasattr(self, "mouse_path_y"):
                    self.maze_plotter.update_plot(
                        self.mouse_current_x,
                        self.mouse_current_y,
                        getattr(self, "mouse_orientation", 0),
                        self.mouse_path_x,
                        self.mouse_path_y
                    )
    
    def toggle_sidebar(self, checked: bool):
        if checked:
            # Hide navigation bar
            if hasattr(self, "nav_bar"):
                self.nav_bar.setVisible(False)
            if hasattr(self, "status_bar"):
                self.status_bar.showMessage("已隐藏导航栏", 2000)
        else:
            # Show navigation bar
            if hasattr(self, "nav_bar"):
                self.nav_bar.setVisible(True)
            if hasattr(self, "status_bar"):
                self.status_bar.showMessage("已显示导航栏", 2000)

    def apply_settings_to_ui(self):
        """从 QSettings 读取默认值并应用到界面控件。"""
        # Serial defaults
        baud = self.settings.value("serial/baudRate", "115200")
        data_bits = self.settings.value("serial/dataBits", "8")
        stop_bits = self.settings.value("serial/stopBits", "1")
        parity = self.settings.value("serial/parity", "无")
        tail_len = self.settings.value("general/tailLength", 200, type=int)
        tail_fade = float(self.settings.value("general/tailFadePower", 0.85))

        try:
            baud_str = str(baud)
            items = [self.baud_rate_selector.itemText(i) for i in range(self.baud_rate_selector.count())]
            if baud_str not in items:
                self.baud_rate_selector.addItem(baud_str)
            self.baud_rate_selector.setCurrentText(baud_str)
        except Exception:
            pass
        # 应用尾迹参数到绘图
        if hasattr(self, "maze_plotter"):
            self.maze_plotter.set_tail_style(tail_len, tail_fade)
        if data_bits in ["5", "6", "7", "8"]:
            self.data_bits_selector.setCurrentText(data_bits)
        if stop_bits in ["1", "1.5", "2"]:
            self.stop_bits_selector.setCurrentText(stop_bits)
        if parity in ["无", "奇", "偶", "Mark", "Space"]:
            self.parity_selector.setCurrentText(parity)

        if hasattr(self, 'nav_bar') and not self.as_page:
            show_sidebar = self.settings.value("general/showSidebarOnStart", True, type=bool)
            self.nav_bar.setVisible(show_sidebar)
            if hasattr(self, 'act_toggle_sidebar'):
                self.act_toggle_sidebar.setChecked(not show_sidebar)

    def reload_settings(self):
        """从 QSettings 重新加载设置（主题/串口/侧栏）。"""
        self.theme_pref = self.settings.value("general/theme", "light")
        self.apply_theme()
        self.apply_settings_to_ui()

    def apply_theme(self):
        """现代化美观主题样式/Fluent 主题切换"""
        # Prefer Fluent Light theme if library available
        if QFW_AVAILABLE:
            try:
                if str(getattr(self, 'theme_pref', 'light')).lower() == 'dark':
                    setTheme(Theme.DARK)
                else:
                    setTheme(Theme.LIGHT)
                setThemeColor('#3b82f6')
            except Exception:
                pass

        style_sheet = """
        /* 完全扁平化设计 - 圆滑处理 */

        QMainWindow {
            background-color: #f5f5f5;
        }

        /* 中央控件和内容区域背景 */
        QWidget#central_widget {
            background-color: #f5f5f5;
        }

        QStackedWidget {
            background-color: #f5f5f5;
        }

        /* 页面容器背景 */
        QWidget[class="page"] {
            background-color: #f5f5f5;
        }

        /* 导航栏样式 - 完全扁平化 */
        NavigationBar {
            background-color: #ffffff;
            border-right: 1px solid #e0e0e0;
        }
        
        QPushButton#navButton {
            text-align: left;
            padding: 16px 24px;
            border: none;
            border-radius: 16px;
            background-color: transparent;
            color: #666666;
            font-size: 14px;
            font-weight: 500;
            margin: 4px 12px;
            min-height: 24px;
        }
        QPushButton#navButton:hover {
            background-color: #f0f0f0;
            color: #333333;
        }
        QPushButton#navButton:checked {
            background-color: #e3f2fd;
            color: #1976d2;
            font-weight: 600;
        }

        QWidget {
            background-color: transparent;
            color: #212121;
            font-family: "Microsoft YaHei UI", "Segoe UI", "SF Pro Display", "PingFang SC", sans-serif;
            font-size: 13px;
            font-weight: 400;
        }
        
        /* 确保页面有背景 */
        QWidget > QWidget {
            background-color: #f5f5f5;
        }
        
        /* 分割器背景 - 完全扁平化 */
        QSplitter {
            background-color: #f5f5f5;
        }
        
        /* 各个页面背景 */
        QWidget#settingsPage,
        QWidget#docsPage,
        QWidget#aboutPage,
        QWidget#realtimeLogPage,
        QWidget#replayPage {
            background-color: #f5f5f5;
        }

        /* 卡片 - 完全扁平化，大圆角 */
        QGroupBox {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            margin-top: 20px;
            padding-top: 20px;
            font-weight: 600;
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            subcontrol-position: top left; 
            padding: 0 16px; 
            margin-left: 20px; 
            color: #212121; 
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }

        /* 按钮 - 完全扁平化，大圆角 */
        QPushButton {
            background-color: #2196f3;
            color: #ffffff;
            border: none;
            padding: 12px 24px;
            border-radius: 16px;
            font-weight: 600;
            font-size: 13px;
            min-height: 44px;
            min-width: 88px;
            letter-spacing: 0.2px;
            text-align: center;
        }
        QPushButton::text {
            color: #ffffff;
            background: transparent;
        }
        QPushButton:hover {
            background-color: #1976d2;
        }
        QPushButton:pressed {
            background-color: #1565c0;
        }
        QPushButton:disabled {
            background-color: #e0e0e0;
            color: #9e9e9e;
        }
        /* 主要按钮样式 - 绿色 */
        QPushButton[class="primary"] {
            background-color: #4caf50;
            color: #ffffff;
            border: none;
        }
        QPushButton[class="primary"]:hover {
            background-color: #45a049;
        }
        QPushButton[class="primary"]:pressed {
            background-color: #3d8b40;
        }
        /* 次要按钮 - 完全扁平化 */
        QPushButton[class="secondary"] {
            background-color: #ffffff;
            color: #2196f3;
            border: 2px solid #2196f3;
            font-weight: 600;
        }
        QPushButton[class="secondary"]:hover {
            background-color: #e3f2fd;
            border-color: #1976d2;
            color: #1976d2;
        }
        QPushButton[class="secondary"]:pressed {
            background-color: #bbdefb;
            border-color: #1565c0;
            color: #1565c0;
        }

        /* 输入控件 - 完全扁平化，大圆角 */
        QLineEdit, QComboBox, QTextEdit {
            background-color: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 16px;
            padding: 12px 20px;
            font-size: 13px;
            selection-background-color: #bbdefb;
            selection-color: #1565c0;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #2196f3;
            background-color: #ffffff;
            outline: none;
        }
        QComboBox:focus { border: 2px solid #2196f3; }
        QLineEdit:hover, QComboBox:hover, QTextEdit:hover {
            border: 2px solid #bdbdbd;
            background-color: #fafafa;
        }
        QComboBox::drop-down {
            border: none;
            border-left: 1px solid #e0e0e0;
            border-radius: 0 16px 16px 0;
            width: 32px;
            background-color: #f5f5f5;
        }
        QComboBox::drop-down:hover {
            background-color: #eeeeee;
        }
        QComboBox::down-arrow { width: 14px; height: 14px; margin: 4px; }
        QComboBox QAbstractItemView {
            border: 1px solid #e0e0e0;
            border-radius: 16px;
            background-color: #ffffff;
            selection-background-color: #bbdefb;
            selection-color: #1565c0;
            padding: 8px;
        }

        /* 菜单与状态栏 - 完全扁平化 */
        QMenuBar {
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
            padding: 10px 16px;
            font-size: 13px;
            font-weight: 500;
        }
        QMenuBar::item {
            padding: 10px 20px;
            border-radius: 12px;
            margin: 2px;
            background: transparent;
        }
        QMenuBar::item:selected {
            background-color: #f0f0f0;
            color: #212121;
        }
        QMenuBar::item:pressed {
            background-color: #e0e0e0;
        }
        QMenu {
            border: 1px solid #e0e0e0;
            background-color: #ffffff;
            border-radius: 16px;
            padding: 8px;
        }
        QMenu::item {
            padding: 12px 32px 12px 20px;
            border-radius: 12px;
            margin: 2px;
            background: transparent;
        }
        QMenu::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QMenu::separator {
            height: 1px;
            background-color: #e0e0e0;
            margin: 8px 12px;
        }

        /* 状态栏 - 完全扁平化 */
        QStatusBar {
            background-color: #ffffff;
            border-top: 1px solid #e0e0e0;
            color: #666666;
            padding: 10px 16px;
            font-size: 12px;
            font-weight: 500;
        }

        /* 分割器 - 完全扁平化 */
        QSplitter::handle { 
            background-color: #e0e0e0;
            width: 2px;
            height: 2px;
        }
        QSplitter::handle:hover { background-color: #2196f3; }
        QSplitter::handle:horizontal { width: 2px; }
        QSplitter::handle:vertical { height: 2px; }

        /* 标签 */
        QLabel { font-size: 13px; color: #212121; }
        QLabel#sensor_value_label { 
            font-weight: 600; 
            color: #1976d2; 
            font-size: 14px;
            padding: 8px 16px;
            background: #e3f2fd;
            border-radius: 12px;
            border: 1px solid #bbdefb;
        }

        /* 文本编辑 - 完全扁平化，大圆角 */
        QTextEdit {
            background-color: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 16px;
            font-family: "Consolas", "Monaco", "Courier New", monospace;
            font-size: 12px;
            line-height: 1.5;
            padding: 12px;
        }
        QTextEdit:focus { border: 2px solid #2196f3; background-color: #ffffff; }

        /* 复选框 - 完全扁平化，大圆角 */
        QCheckBox { font-size: 13px; color: #212121; spacing: 12px; font-weight: 500; }
        QCheckBox::indicator {
            width: 22px; height: 22px;
            border: 2px solid #bdbdbd;
            border-radius: 6px;
            background-color: #ffffff;
        }
        QCheckBox::indicator:hover {
            border-color: #9e9e9e;
            background-color: #f5f5f5;
        }
        QCheckBox::indicator:checked {
            background-color: #2196f3;
            border-color: #2196f3;
        }

        /* 进度条 - 完全扁平化，大圆角 */
        QProgressBar {
            border: none;
            border-radius: 12px;
            background-color: #e0e0e0;
            text-align: center;
            height: 10px;
        }
        QProgressBar::chunk {
            background-color: #2196f3;
            border-radius: 12px;
        }

        /* 滚动条 - 完全扁平化，大圆角 */
        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 12px;
        }
        QScrollBar::handle:vertical {
            background-color: #bdbdbd;
            border-radius: 8px;
            min-height: 30px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #9e9e9e;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }

        QScrollBar:horizontal {
            border: none;
            background: transparent;
            height: 12px;
        }
        QScrollBar::handle:horizontal {
            background-color: #bdbdbd;
            border-radius: 8px;
            min-width: 30px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #9e9e9e;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }

        /* 对话框 / 提示框 - 完全扁平化，大圆角 */
        QDialog, QMessageBox {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
        }
        QMessageBox QLabel {
            color: #212121;
            font-size: 14px;
            font-weight: 500;
        }
        QMessageBox QPushButton {
            background-color: #2196f3;
            color: #ffffff;
            border: none;
            padding: 12px 24px;
            border-radius: 16px;
            font-weight: 600;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #1976d2;
        }
        QMessageBox QPushButton:pressed {
            background-color: #1565c0;
        }

        /* 说明和关于页面卡片样式 - 完全扁平化 */
        QWidget#titleCard {
            background-color: #2196f3;
            border-radius: 20px;
            border: none;
        }
        QLabel#pageTitle {
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
            background: transparent;
        }
        QLabel#pageSubtitle {
            font-size: 14px;
            color: #ffffff;
            background: transparent;
        }

        QWidget#appInfoCard {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
        }
        QLabel#appNameLabel {
            font-size: 32px;
            font-weight: 700;
            color: #212121;
            background: transparent;
        }
        QLabel#versionLabel {
            font-size: 16px;
            font-weight: 500;
            color: #757575;
            background: transparent;
        }
        QLabel#appDescLabel {
            font-size: 14px;
            color: #616161;
            background: transparent;
        }

        QWidget#sectionCard {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            padding: 8px;
        }
        QLabel#sectionTitle {
            font-size: 18px;
            font-weight: 600;
            color: #212121;
            background: transparent;
            padding-bottom: 8px;
        }
        QLabel#sectionContent {
            font-size: 13px;
            color: #424242;
            background: transparent;
            line-height: 1.6;
        }
        /* 设置页卡片 - 完全扁平化 */
        QWidget#settingsCard {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
        }
        QLabel#settingsTitle {
            font-size: 16px;
            font-weight: 600;
            color: #212121;
        }
        QLabel#infoKeyLabel {
            font-size: 13px;
            font-weight: 500;
            color: #757575;
            background: transparent;
        }
        QLabel#infoValueLabel {
            font-size: 13px;
            color: #212121;
            background: transparent;
        }
        """
        self.setStyleSheet(style_sheet)
        try:
            app = QApplication.instance()
            if app is not None:
                app.setStyleSheet(style_sheet)
        except Exception:
            pass

    def show_help(self):
        text = (
            "使用说明（统一协议）\n\n"
            "1) 基本操作：在'串口配置'中选择串口参数并连接；在'发送数据'中输入文本点击发送。\n"
            "2) 控制台：显示所有收发数据（可用于调试）。\n\n"
            "3) 串口数据协议：\n"
            "   - 帧格式：s,X,Y,O,Angle,Front,Left,Right,Mode\\r\\n\n"
            "   - X: 列(0-7)、Y: 行(0-7)、O: 朝向(0=北,1=东,2=南,3=西)\n"
            "   - Angle: 陀螺仪角度（度，0度=北，顺时针增加）\n"
            "   - Front/Left/Right: 前/左/右传感器值（0=有墙，1=没墙）\n"
            "   - Mode: 运行模式（0=停止，1=迷宫模式）\n"
            "   - 示例：s,3,4,1,45.5,0,1,1,1\\r\\n  (位置3,4，朝东，角度45.5°，前方有墙，左右无墙，迷宫模式)\n\n"
            "   - 墙体自动判断：\n"
            "     · 系统根据位置、朝向和传感器数据自动判断并绘制墙体\n"
            "     · 传感器值0表示有墙，1表示没墙\n"
            "     · 小车一格一格移动，每格自动更新墙体信息\n\n"
            "4) 其它：菜单栏可刷新串口、清空控制台、隐藏侧栏、查看本说明。\n\n"
            f"开发者：{APP_DEVELOPER}（{APP_SCHOOL}）\n"
            f"用途：{APP_PROJECT}\n"
            f"联系方式：{APP_EMAIL}"
        )
        QMessageBox.information(self, "使用说明", text)
    
    def show_about_dialog(self):
        """显示关于对话框"""
        about_text = (
            f"{APP_NAME}\n\n"
            f"版本：{APP_VERSION}\n\n"
            f"开发者：{APP_DEVELOPER}\n"
            f"学校：{APP_SCHOOL}\n"
            f"项目：{APP_PROJECT}\n\n"
            f"联系方式：{APP_EMAIL}\n"
            f"网址：{APP_URL}\n\n"
            f"技术栈：\n"
            f"  • PyQt5 {PYQT_VERSION_STR}\n"
            f"  • Qt {QT_VERSION_STR}\n"
            f"  • Python {sys.version.split(' ')[0]}\n"
            f"  • Matplotlib\n\n"
            f"{APP_COPYRIGHT} {APP_DEVELOPER}\n"
            f"本软件为电子系统设计课程项目，仅供学习交流使用。"
        )
        QMessageBox.about(self, "关于", about_text)

    def populate_ports(self):
        # 如果串口已连接，不自动刷新（避免干扰）
        if self.serial.isOpen():
            return
        
        # 保存当前选中的端口名称
        current_port = self.port_selector.currentText() if self.port_selector.count() > 0 else ""
        
        # 获取当前可用的串口列表
        available_ports = [p.portName() for p in QSerialPortInfo.availablePorts()]
        
        # 如果列表没有变化，不更新（避免闪烁）
        current_list = [self.port_selector.itemText(i) for i in range(self.port_selector.count())]
        if current_list == available_ports:
            return
        
        # 清空并重新填充
        self.port_selector.clear()
        for port_name in available_ports:
            self.port_selector.addItem(port_name)
        
        # 如果之前选中的端口仍然存在，恢复选择
        if current_port and current_port in available_ports:
            self.port_selector.setCurrentText(current_port)
        elif self.port_selector.count() > 0:
            # 如果之前选中的端口不存在了，选择第一个可用端口
            self.port_selector.setCurrentIndex(0)

    def connect_serial(self):
        # 连接前先刷新一次串口列表，确保使用最新的串口信息
        self.populate_ports()
        self.show_long_task("正在连接串口...")
        
        port_name = self.port_selector.currentText()
        if not port_name:
            self.finish_long_task("等待操作", 300)
            self.show_toast("请先选择串口", "warning")
            return
        
        baud_rate = self.baud_rate_selector.currentText()
        data_bits_str = self.data_bits_selector.currentText()
        stop_bits_str = self.stop_bits_selector.currentText()
        parity_str = self.parity_selector.currentText()
        
        self.serial.setPortName(port_name)
        try:
            self.serial.setBaudRate(int(baud_rate))
        except ValueError:
            self.finish_long_task("连接失败", 400)
            self.show_toast("无效的波特率", "error")
            return

        # Set Data Bits
        if data_bits_str == "5":
            self.serial.setDataBits(QSerialPort.Data5)
        elif data_bits_str == "6":
            self.serial.setDataBits(QSerialPort.Data6)
        elif data_bits_str == "7":
            self.serial.setDataBits(QSerialPort.Data7)
        elif data_bits_str == "8":
            self.serial.setDataBits(QSerialPort.Data8)

        # Set Stop Bits
        if stop_bits_str == "1":
            self.serial.setStopBits(QSerialPort.OneStop)
        elif stop_bits_str == "1.5":
            self.serial.setStopBits(QSerialPort.OneAndHalfStop)
        elif stop_bits_str == "2":
            self.serial.setStopBits(QSerialPort.TwoStop)

        # Set Parity
        if parity_str == "无":
            self.serial.setParity(QSerialPort.NoParity)
        elif parity_str == "奇":
            self.serial.setParity(QSerialPort.OddParity)
        elif parity_str == "偶":
            self.serial.setParity(QSerialPort.EvenParity)
        elif parity_str == "Mark":
            self.serial.setParity(QSerialPort.MarkParity)
        elif parity_str == "Space":
            self.serial.setParity(QSerialPort.SpaceParity)

        if not self.serial.open(QIODevice.ReadWrite):
            self.finish_long_task("连接失败", 500)
            self.show_toast(f"无法打开串口 {port_name}: {self.serial.errorString()}", "error", 2600)
            self._set_connection_state(False)
        else:
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.send_button.setEnabled(True)
            self._set_connection_state(True, port_name, baud_rate)
            # 重置数据统计
            self.frame_count = 0
            self.error_frame_count = 0
            self.last_data_time = None
            self._set_data_state("等待数据", "#f59e0b", "数据状态")
            self.finish_long_task("连接成功", 500)
            self.show_toast(f"已连接到 {port_name} @ {baud_rate}", "success")

    def disconnect_serial(self):
        if self.serial.isOpen():
            self.show_long_task("正在断开...")
            self.serial.close()
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.send_button.setEnabled(False)
            # 断开后刷新串口列表，以便检测新插入的设备
            self.populate_ports()
            self._set_connection_state(False)
            self._set_run_mode("空闲", busy=False)
            self._set_data_state("无连接", "#cbd5e1", "数据状态")
            self.finish_long_task("已断开", 400)
            self.show_toast("串口已断开", "warning")

    def send_serial_data(self):
        if self.serial.isOpen():
            data_to_send = self.send_data_input.text()
            if data_to_send:
                self.serial.write(data_to_send.encode('utf-8'))
                self.update_console(data_to_send, True)
                self._emit_log('TX', data_to_send)
                self.bytes_sent_window.append((time.time(), len(data_to_send.encode('utf-8'))))
                # Optionally clear the input field
                # self.send_data_input.clear()
            else:
                self.show_toast("发送内容不能为空", "warning")
        else:
            self.show_toast("请先连接串口", "warning")

    def send_command(self, command):
        if self.serial.isOpen():
            self.serial.write(command.encode('utf-8'))
            self.update_console(f"Command sent: {command}", True)
            self._emit_log('TX', command)
            self.bytes_sent_window.append((time.time(), len(command.encode('utf-8'))))
        else:
            self.show_toast("请先连接串口", "warning")

    def start_mouse(self):
        self.send_command("start")
        self._set_run_mode("运行中", busy=True)
        self.show_toast("已发送启动命令", "success", 1500)

    def stop_mouse(self):
        self.send_command("stop")
        self._set_run_mode("空闲", busy=False)
        # 重置路径记录
        self.current_run_path = []
        self.has_reached_goal = False
        self.show_toast("已发送停止命令", "info", 1500)

    def reset_mouse(self):
        self.send_command("reset")
        self._set_run_mode("空闲", busy=False)
        # 重置路径记录
        self.current_run_path = []
        self.has_reached_goal = False
        self.best_path_info = None
        # 重置当前位置到起点
        self.mouse_current_x = 7.5
        self.mouse_current_y = 0.5
        self.mouse_path_x = [self.mouse_current_x]
        self.mouse_path_y = [self.mouse_current_y]
        self.show_toast("已发送复位命令", "warning", 1500)

    def rescue_left(self):
        """左救援：小车向左后退脱离卡住状态"""
        self.send_command("rescue_left")
        self.show_toast("已发送左救援命令", "info", 1500)

    def rescue_right(self):
        """右救援：小车向右后退脱离卡住状态"""
        self.send_command("rescue_right")
        self.show_toast("已发送右救援命令", "info", 1500)

    def update_console(self, data, is_send):
        """Log data (控制台已移除，此方法保留用于调试)"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = ">>" if is_send else "<<"
        print(f"[{timestamp}] {prefix} {data}")  # 输出到终端而不是界面

    def _calculate_walls_from_sensors(self, x, y, orientation, front_val, left_val, right_val):
        """
        根据当前位置、朝向和传感器值计算墙体位掩码
        传感器值：0=有墙，1=没墙
        朝向：0=北，1=东，2=南，3=西
        墙体方向（位掩码）：1=右(+X), 2=上(+Y), 4=左(-X), 8=下(-Y)
        """
        wall_mask = 0
        
        # 根据朝向映射传感器到墙体方向
        if orientation == 0:  # 北
            if front_val == 0:  # 前方有墙
                wall_mask |= 0x02  # 上墙(+Y)
            if left_val == 0:  # 左侧有墙
                wall_mask |= 0x04  # 左墙(-X)
            if right_val == 0:  # 右侧有墙
                wall_mask |= 0x01  # 右墙(+X)
        elif orientation == 1:  # 东
            if front_val == 0:  # 前方有墙
                wall_mask |= 0x01  # 右墙(+X)
            if left_val == 0:  # 左侧有墙
                wall_mask |= 0x02  # 上墙(+Y)
            if right_val == 0:  # 右侧有墙
                wall_mask |= 0x08  # 下墙(-Y)
        elif orientation == 2:  # 南
            if front_val == 0:  # 前方有墙
                wall_mask |= 0x08  # 下墙(-Y)
            if left_val == 0:  # 左侧有墙
                wall_mask |= 0x01  # 右墙(+X)
            if right_val == 0:  # 右侧有墙
                wall_mask |= 0x04  # 左墙(-X)
        elif orientation == 3:  # 西
            if front_val == 0:  # 前方有墙
                wall_mask |= 0x04  # 左墙(-X)
            if left_val == 0:  # 左侧有墙
                wall_mask |= 0x08  # 下墙(-Y)
            if right_val == 0:  # 右侧有墙
                wall_mask |= 0x02  # 上墙(+Y)
        
        return wall_mask
    
    def snapshot_current_run(self, name: str = None):
        """将当前轨迹保存为可回放的记录"""
        if not self.mouse_path_x or not self.mouse_path_y:
            return
        if name is None or not name.strip():
            name = f"run_{len(self.replay_runs)+1}"
        self.replay_runs.append({
            "name": name.strip(),
            "path_x": list(self.mouse_path_x),
            "path_y": list(self.mouse_path_y),
        })

    def _snapshot_path_cells(self, path_cells, name: str):
        """将格子路径(整数坐标)保存到回放列表，转换为中心点显示坐标"""
        if not path_cells:
            return
        path_x = [cx + 0.5 for cx, _ in path_cells]
        path_y = [cy + 0.5 for _, cy in path_cells]
        self._append_or_replace_replay_run(name.strip(), path_x, path_y)

    def _append_or_replace_replay_run(self, name: str, path_x, path_y):
        """在回放列表中按名称替换或追加，并限制长度"""
        # 替换同名
        for i, run in enumerate(self.replay_runs):
            if run.get("name") == name:
                self.replay_runs[i] = {"name": name, "path_x": list(path_x), "path_y": list(path_y)}
                break
        else:
            self.replay_runs.append({"name": name, "path_x": list(path_x), "path_y": list(path_y)})

        # 限制回放列表长度，超出时丢弃最旧
        if len(self.replay_runs) > self.max_replay_saved:
            overflow = len(self.replay_runs) - self.max_replay_saved
            self.replay_runs = self.replay_runs[overflow:]
    
    def _on_reach_goal(self):
        """到达终点时的处理：记录路径并优化"""
        if not self.current_run_path:
            return
        
        # 记录原始路径
        original_path = list(self.current_run_path)
        
        # 优化路径
        optimized_path = self._optimize_path(original_path)
        
        # 保存优化后的路径
        path_info = {
            "original_path": original_path,
            "optimized_path": optimized_path,
            "original_length": len(original_path),
            "optimized_length": len(optimized_path),
            "timestamp": time.time()
        }
        self.optimized_paths.append(path_info)
        
        # 显示提示
        reduction = len(original_path) - len(optimized_path)
        reduction_percent = (reduction / len(original_path) * 100) if original_path else 0
        self.show_toast(
            f"到达终点！路径已优化：{len(original_path)}步 → {len(optimized_path)}步（减少{reduction}步，{reduction_percent:.1f}%）",
            "success",
            3000
        )
        
        # 自动保存到回放列表（原始 + 优化）
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 原始轨迹（带插值）已经在 mouse_path_x/y 中，保留
        self.snapshot_current_run(f"原始轨迹_{timestamp}")
        # 优化轨迹（按格子中心点）
        self._snapshot_path_cells(optimized_path, f"优化轨迹_{timestamp}")

        # 维护最优路径
        if (self.best_path_info is None) or (len(optimized_path) < self.best_path_info["optimized_length"]):
            self.best_path_info = {
                "optimized_path": optimized_path,
                "optimized_length": len(optimized_path),
                "timestamp": timestamp,
            }
            # 保存/覆盖"最优路径"到回放列表
            self._snapshot_path_cells(optimized_path, "最优路径")

        # 自动发送最优路径（如开启）
        if self.auto_send_best_path:
            try:
                self.send_optimized_path()
            except Exception:
                pass
    
    def _optimize_path(self, path):
        """优化路径：去除冗余路径，找到最短路径"""
        if not path or len(path) <= 1:
            return path
        
        # 预清理：去重连续、消除 A-B-A
        cleaned = []
        for c in path:
            if cleaned and cleaned[-1] == c:
                continue
            if len(cleaned) >= 2 and cleaned[-2] == c:
                cleaned.pop()
                continue
            cleaned.append(c)

        # 使用已知墙信息做 BFS 寻找最短路径（仅用已知墙，未知视为可通行）
        start = cleaned[0]
        goal_cells = {(x, y) for x in range(self.goal_min_x, self.goal_max_x + 1)
                      for y in range(self.goal_min_y, self.goal_max_y + 1)}
        grid_size = 8  # 8x8 迷宫

        def has_wall(a, b):
            ax, ay = a
            bx, by = b
            dx, dy = bx - ax, by - ay
            # 仅四邻
            if abs(dx) + abs(dy) != 1:
                return True
            mask_a = self.wall_map.get(a, 0)
            mask_b = self.wall_map.get(b, 0)
            # +X 右墙 0x01, +Y 上墙 0x02, -X 左墙 0x04, -Y 下墙 0x08
            if dx == 1:  # a -> right
                if mask_a & 0x01: return True
                if mask_b & 0x04: return True
            if dx == -1:  # a -> left
                if mask_a & 0x04: return True
                if mask_b & 0x01: return True
            if dy == 1:  # a -> up (+Y)
                if mask_a & 0x02: return True
                if mask_b & 0x08: return True
            if dy == -1:  # a -> down (-Y)
                if mask_a & 0x08: return True
                if mask_b & 0x02: return True
            return False

        from collections import deque
        q = deque([start])
        prev = {start: None}
        found = None
        while q:
            cur = q.popleft()
            if cur in goal_cells:
                found = cur
                break
            cx, cy = cur
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if nx < 0 or ny < 0 or nx >= grid_size or ny >= grid_size:
                    continue
                nxt = (nx, ny)
                if nxt in prev:
                    continue
                if has_wall(cur, nxt):
                    continue
                prev[nxt] = cur
                q.append(nxt)

        if found is None:
            # 未找到基于墙信息的更短路径，退回 cleaned
            return cleaned

        # 回溯得到最短路径
        path_nodes = []
        cur = found
        while cur is not None:
            path_nodes.append(cur)
            cur = prev[cur]
        path_nodes.reverse()
        return path_nodes
    
    def get_best_optimized_path(self):
        """获取最短的优化路径"""
        if not self.optimized_paths:
            if self.best_path_info:
                return self.best_path_info.get("optimized_path")
            return None
        
        # 找到最短的优化路径
        best = min(self.optimized_paths, key=lambda p: p["optimized_length"])
        return best["optimized_path"]
    
    def send_optimized_path(self):
        """通过串口发送最短优化路径"""
        if not self.serial.isOpen():
            self.show_toast("请先连接串口", "warning")
            return
        
        best_path = self.get_best_optimized_path()
        if not best_path:
            self.show_toast("没有可用的优化路径", "warning")
            return
        
        # 将路径转换为命令格式
        # 帧格式：
        # path:x1,y1;x2,y2;x3,y3;...;xn,yn\n
        # 说明：坐标为格子坐标整数；顺序为起点到终点的最优路径
        path_str = ";".join([f"{x},{y}" for x, y in best_path])
        command = f"path:{path_str}\n"
        
        self.send_command(command)
        self.show_toast(f"已发送优化路径（{len(best_path)}步）", "success", 2000)

    def _is_at_goal(self, grid_x: int, grid_y: int) -> bool:
        """判断当前位置是否在终点区域内"""
        return (self.goal_min_x <= grid_x <= self.goal_max_x) and (self.goal_min_y <= grid_y <= self.goal_max_y)

    def _handle_frame(self, line: str):
        """处理完整帧：s,X,Y,O,Angle,Front,Left,Right,Mode"""
        line = line.strip().replace('\r', '').replace('\n', '')
        if not line:
            return
        if line[0].lower() == 's':
            line = line[1:]
        if line.startswith(','):
            line = line[1:]

        parts = line.split(',')
        # 过滤空字段（处理连续逗号或末尾逗号的情况）
        parts = [p.strip() for p in parts if p.strip()]
        
        # 支持新旧两种格式
        if len(parts) < 6:
            raise ValueError(f"帧字段不足 (got {len(parts)} fields, need at least 6): {line}")

        # 新格式：s,X,Y,O,Angle,Front,Left,Right,Mode（去掉s后8个字段）
        # 旧格式：s,X,Y,O,Front,Left,Right（去掉s后6个字段，兼容）
        if len(parts) >= 8:
            # 新格式：X,Y,O,Angle,Front,Left,Right,Mode
            x_str, y_str, o_str = parts[0], parts[1], parts[2]
            angle_str = parts[3]  # 角度可以是小数
            front_val, left_val, right_val = int(parts[4]), int(parts[5]), int(parts[6])
            mode_str = parts[7] if len(parts) > 7 else "停止"
        else:
            # 旧格式兼容：X,Y,O,Front,Left,Right
            x_str, y_str, o_str = parts[0], parts[1], parts[2]
            angle_str = "0"
            front_val, left_val, right_val = int(parts[3]), int(parts[4]), int(parts[5])
            mode_str = "停止"

        x = float(x_str) + 0.5  # Center the mouse in the cell
        y = float(y_str) + 0.5  # Center the mouse in the cell
        orientation = int(o_str)
        
        # 获取格子坐标（用于路径记录和终点检测）
        grid_x = int(float(x_str))
        grid_y = int(float(y_str))
        
        # 解析角度（度）
        try:
            self.gyro_angle = float(angle_str)
        except (ValueError, IndexError):
            self.gyro_angle = 0.0
        
        # 解析运行模式
        mode_text = mode_str.strip() if mode_str else "停止"
        if mode_text == "0" or mode_text.lower() == "stop":
            mode_text = "停止"
        elif mode_text == "1" or mode_text.lower() == "maze":
            mode_text = "迷宫模式"
        self.run_mode = mode_text

        # 更新位置和朝向
        self.mouse_orientation = orientation
        
        # 记录当前格子坐标到路径中（只在迷宫模式下记录）
        if mode_text == "迷宫模式":
            # 如果当前格子与上一个格子不同，添加到路径
            if not self.current_run_path or self.current_run_path[-1] != (grid_x, grid_y):
                self.current_run_path.append((grid_x, grid_y))
            
            # 检测是否到达终点区域
            if self._is_at_goal(grid_x, grid_y) and not self.has_reached_goal:
                self.has_reached_goal = True
                self._on_reach_goal()
        else:
            # 停止模式时重置
            if self.current_run_path:
                self.current_run_path = []
                self.has_reached_goal = False
        
        # 更新指南针
        if hasattr(self, 'compass_widget'):
            self.compass_widget.update_angle(self.gyro_angle)
        
        # 更新运行模式显示
        busy = (self.run_mode != "停止")
        self._set_run_mode(self.run_mode, busy=busy)

        # 平滑插值：将上一点到新点分成若干小步，减少跳变
        if self.mouse_path_x and self.mouse_path_y:
            last_x = self.mouse_path_x[-1]
            last_y = self.mouse_path_y[-1]
            dx = x - last_x
            dy = y - last_y
            dist = (dx * dx + dy * dy) ** 0.5
            steps = min(10, max(1, int(dist / 0.4)))  # 每步约0.4格
            for i in range(1, steps + 1):
                t = i / (steps + 1)
                self.mouse_path_x.append(last_x + dx * t)
                self.mouse_path_y.append(last_y + dy * t)

        # 追加最终点
        self.mouse_path_x.append(x)
        self.mouse_path_y.append(y)

        # 截断尾迹长度
        max_len = getattr(self.maze_plotter, "path_max_len", 200)
        if len(self.mouse_path_x) > max_len:
            trim = len(self.mouse_path_x) - max_len
            self.mouse_path_x = self.mouse_path_x[trim:]
            self.mouse_path_y = self.mouse_path_y[trim:]

        self.mouse_current_x = self.mouse_path_x[-1]
        self.mouse_current_y = self.mouse_path_y[-1]

        # 更新传感器标签显示
        self.sensor_labels["前传感器:"].setText(str(front_val))
        self.sensor_labels["左传感器:"].setText(str(left_val))
        self.sensor_labels["右传感器:"].setText(str(right_val))

        # 根据传感器数据自动计算并绘制墙体
        cell_x = int(float(x_str))
        cell_y = int(float(y_str))
        wall_mask = self._calculate_walls_from_sensors(
            cell_x, cell_y, orientation,
            front_val, left_val, right_val
        )
        if wall_mask > 0:
            self.maze_plotter.draw_maze_wall(cell_x, cell_y, wall_mask)
            # 记录已知墙体（合并）
            existing = self.wall_map.get((cell_x, cell_y), 0)
            self.wall_map[(cell_x, cell_y)] = existing | wall_mask

        # 更新迷宫图
        self.maze_plotter.update_plot(
            self.mouse_current_x,
            self.mouse_current_y,
            self.mouse_orientation,
            self.mouse_path_x,
            self.mouse_path_y
        )

    def read_serial_data(self):
        raw = self.serial.readAll()
        data = raw.data().decode('utf-8', errors='replace')
        self.bytes_received_window.append((time.time(), len(raw)))
        self.update_console(data, False)
        self._emit_log('RX', data)

        # 累积缓冲，改进的分片数据处理
        self.rx_buffer += data
        
        # 处理缓冲区中所有完整的帧
        # 策略：查找以's'开头的完整行（以\n结尾）
        while True:
            # 查找第一个's'的位置（不区分大小写）
            s_idx = -1
            for i in range(len(self.rx_buffer)):
                if self.rx_buffer[i].lower() == 's':
                    s_idx = i
                    break
            
            if s_idx == -1:
                # 没有找到's'，如果缓冲区太长，清空（可能是错误数据）
                if len(self.rx_buffer) > 500:
                    self.rx_buffer = ""
                break
            
            # 从's'位置开始，查找下一个'\n'
            remaining = self.rx_buffer[s_idx:]
            if '\n' not in remaining:
                # 没有找到完整的行，保留从's'开始的数据，丢弃之前的数据
                self.rx_buffer = remaining
                break
            
            # 提取完整的一行（从's'到'\n'）
            line_end = remaining.index('\n')
            line = remaining[:line_end].strip()
            self.rx_buffer = remaining[line_end + 1:]  # 保留剩余数据
            
            # 清理行数据
            line = line.replace('\r', '')
            if not line:
                continue
            
            # 处理这一帧
            try:
                self._handle_frame(line)
                self.frame_count += 1
                self.last_data_time = time.time()
            except Exception as e:
                # 解析失败，记录错误但继续处理下一帧
                print(f"Frame parse error: {e}; line={line[:100]}")
                self.error_frame_count += 1

    def _emit_log(self, direction: str, text: str):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        for cb in list(self.log_subscribers):
            try:
                cb(ts, direction, text)
            except Exception:
                pass

    def _purge_old_bytes(self):
        now = time.time()
        cutoff = now - 5.0  # 5s window
        while self.bytes_received_window and self.bytes_received_window[0][0] < cutoff:
            self.bytes_received_window.popleft()
        while self.bytes_sent_window and self.bytes_sent_window[0][0] < cutoff:
            self.bytes_sent_window.popleft()

    def get_throughput_bps(self):
        rx = sum(n for t, n in self.bytes_received_window)
        tx = sum(n for t, n in self.bytes_sent_window)
        # approximate per 5s window
        return int(rx * 8 / 5.0), int(tx * 8 / 5.0)

class SettingsPage(QWidget):
    def __init__(self, parent=None, app_page: 'MicroMouseApp' = None):
        super().__init__(parent)
        self.setObjectName("settingsPage")
        self.app_page = app_page
        self.settings = QSettings("MicromouseLab", "MicromouseApp")

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)
        # 让设置内容区域居中且宽度适中，避免铺满整个窗口显得空旷
        root.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # 局部样式：卡片、标题和表单控件字号/高度统一
        self.setStyleSheet(
            """
            #settingsCard {
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid #e5e7eb;
            }
            #settingsTitle {
                font-size: 15px;
                font-weight: 600;
                color: #111827;
            }
            #settingsPage QLabel {
                font-size: 13px;
            }
            #settingsPage QCheckBox {
                font-size: 13px;
            }
            #settingsPage QComboBox,
            #settingsPage QSpinBox,
            #settingsPage QDoubleSpinBox,
            #settingsPage QLineEdit {
                min-height: 32px;
                font-size: 13px;
            }
            #settingsPage QPushButton {
                min-height: 34px;
                font-size: 13px;
            }
            """
        )

        # 卡片创建助手
        def make_card(title_text: str):
            card = QWidget()
            card.setObjectName("settingsCard")
            # 限制单个卡片最大宽度，视觉更紧凑
            card.setMaximumWidth(980)
            v = QVBoxLayout(card)
            v.setContentsMargins(20, 16, 20, 16)
            v.setSpacing(12)
            title = QLabel(title_text)
            title.setObjectName("settingsTitle")
            v.addWidget(title)
            return card, v

        # 1. 界面与启动
        ui_card, ui_layout = make_card("界面与启动")
        ui_form = QFormLayout()
        ui_form.setLabelAlignment(Qt.AlignRight)
        ui_form.setSpacing(8)

        self.theme_combo = QComboBox(self)
        self.theme_combo.addItems(["light", "dark"])
        current_theme = self.settings.value("general/theme", "light")
        if current_theme in ["light", "dark"]:
            self.theme_combo.setCurrentText(current_theme)
        ui_form.addRow(QLabel("主题"), self.theme_combo)

        self.sidebar_checkbox = QCheckBox("启动时显示左侧栏", self)
        self.sidebar_checkbox.setChecked(self.settings.value("general/showSidebarOnStart", True, type=bool))
        ui_form.addRow(QLabel("界面"), self.sidebar_checkbox)

        self.default_view_combo = QComboBox(self)
        self.default_view_combo.addItems(["2D", "3D"])
        self.default_view_combo.setCurrentText(str(self.settings.value("general/defaultViewMode", "2D")))
        ui_form.addRow(QLabel("默认视图"), self.default_view_combo)

        self.splash_checkbox = QCheckBox("启动时显示启动动画", self)
        self.splash_checkbox.setChecked(self.settings.value("general/showSplashOnStart", True, type=bool))
        ui_form.addRow(QLabel("启动动画"), self.splash_checkbox)

        self.splash_style_combo = QComboBox(self)
        self.splash_style_combo.addItems(["progress", "gif"])
        self.splash_style_combo.setCurrentText(str(self.settings.value("general/splashStyle", "progress")))
        ui_form.addRow(QLabel("动画样式"), self.splash_style_combo)

        self.splash_duration_spin = QSpinBox(self)
        self.splash_duration_spin.setRange(300, 10000)
        self.splash_duration_spin.setSingleStep(100)
        self.splash_duration_spin.setSuffix(" ms")
        try:
            self.splash_duration_spin.setValue(int(self.settings.value("general/splashDurationMs", 3000, type=int)))
        except Exception:
            self.splash_duration_spin.setValue(3000)
        ui_form.addRow(QLabel("持续时间"), self.splash_duration_spin)

        self.splash_gif_edit = QLineEdit(self)
        self.splash_gif_edit.setPlaceholderText("可选：GIF 文件路径")
        self.splash_gif_edit.setText(str(self.settings.value("general/splashGifPath", "")))
        ui_form.addRow(QLabel("GIF 路径"), self.splash_gif_edit)

        ui_layout.addLayout(ui_form)
        root.addWidget(ui_card)

        # 2. 迷宫与路径
        maze_card, maze_layout = make_card("迷宫与路径")
        maze_form = QFormLayout()
        maze_form.setLabelAlignment(Qt.AlignRight)
        maze_form.setSpacing(8)

        self.tail_len_spin = QSpinBox(self)
        self.tail_len_spin.setRange(20, 800)
        self.tail_len_spin.setSingleStep(20)
        self.tail_len_spin.setSuffix(" 点")
        try:
            self.tail_len_spin.setValue(int(self.settings.value("general/tailLength", 200, type=int)))
        except Exception:
            self.tail_len_spin.setValue(200)
        maze_form.addRow(QLabel("尾迹长度"), self.tail_len_spin)

        self.tail_fade_spin = QDoubleSpinBox(self)
        self.tail_fade_spin.setDecimals(2)
        self.tail_fade_spin.setRange(0.10, 1.20)
        self.tail_fade_spin.setSingleStep(0.05)
        self.tail_fade_spin.setValue(float(self.settings.value("general/tailFadePower", 0.85)))
        maze_form.addRow(QLabel("尾迹渐隐强度"), self.tail_fade_spin)

        # 终点区域
        goal_layout = QHBoxLayout()
        self.goal_min_x_spin = QSpinBox(self); self.goal_min_x_spin.setRange(0, 7)
        self.goal_max_x_spin = QSpinBox(self); self.goal_max_x_spin.setRange(0, 7)
        self.goal_min_y_spin = QSpinBox(self); self.goal_min_y_spin.setRange(0, 7)
        self.goal_max_y_spin = QSpinBox(self); self.goal_max_y_spin.setRange(0, 7)
        self.goal_min_x_spin.setValue(int(self.settings.value("maze/goalMinX", 3)))
        self.goal_max_x_spin.setValue(int(self.settings.value("maze/goalMaxX", 4)))
        self.goal_min_y_spin.setValue(int(self.settings.value("maze/goalMinY", 3)))
        self.goal_max_y_spin.setValue(int(self.settings.value("maze/goalMaxY", 4)))
        goal_layout.addWidget(QLabel("X:"))
        goal_layout.addWidget(self.goal_min_x_spin)
        goal_layout.addWidget(QLabel("~"))
        goal_layout.addWidget(self.goal_max_x_spin)
        goal_layout.addSpacing(12)
        goal_layout.addWidget(QLabel("Y:"))
        goal_layout.addWidget(self.goal_min_y_spin)
        goal_layout.addWidget(QLabel("~"))
        goal_layout.addWidget(self.goal_max_y_spin)
        goal_widget = QWidget()
        goal_widget.setLayout(goal_layout)
        maze_form.addRow(QLabel("终点区域"), goal_widget)

        # 回放保留上限
        self.replay_max_spin = QSpinBox(self)
        self.replay_max_spin.setRange(10, 300)
        self.replay_max_spin.setSingleStep(10)
        self.replay_max_spin.setSuffix(" 条")
        self.replay_max_spin.setValue(int(self.settings.value("replay/maxSaved", 60)))
        maze_form.addRow(QLabel("回放保留"), self.replay_max_spin)

        # 自动发送最优路径
        self.auto_send_best_chk = QCheckBox("到达终点后自动发送最优路径", self)
        self.auto_send_best_chk.setChecked(self.settings.value("maze/autoSendBestPath", False, type=bool))
        maze_form.addRow(QLabel("自动发送"), self.auto_send_best_chk)

        maze_layout.addLayout(maze_form)
        root.addWidget(maze_card)

        # 3. 串口默认值
        serial_card, serial_layout = make_card("串口默认值")
        serial_form = QFormLayout()
        serial_form.setLabelAlignment(Qt.AlignRight)
        serial_form.setSpacing(8)

        common_baud_rates = [
            "9600", "19200", "38400", "57600",
            "115200", "230400", "460800", "921600"
        ]
        self.baud_combo = QComboBox(self)
        self.baud_combo.addItems(common_baud_rates)
        _baud_pref = str(self.settings.value("serial/baudRate", "115200"))
        if _baud_pref not in common_baud_rates:
            self.baud_combo.addItem(_baud_pref)
        self.baud_combo.setCurrentText(_baud_pref)
        serial_form.addRow(QLabel("默认波特率"), self.baud_combo)

        self.data_bits_combo = QComboBox(self)
        self.data_bits_combo.addItems(["5", "6", "7", "8"])
        self.data_bits_combo.setCurrentText(str(self.settings.value("serial/dataBits", "8")))
        serial_form.addRow(QLabel("默认数据位"), self.data_bits_combo)

        self.stop_bits_combo = QComboBox(self)
        self.stop_bits_combo.addItems(["1", "1.5", "2"])
        self.stop_bits_combo.setCurrentText(str(self.settings.value("serial/stopBits", "1")))
        serial_form.addRow(QLabel("默认停止位"), self.stop_bits_combo)

        self.parity_combo = QComboBox(self)
        self.parity_combo.addItems(["无", "奇", "偶", "Mark", "Space"])
        self.parity_combo.setCurrentText(str(self.settings.value("serial/parity", "无")))
        serial_form.addRow(QLabel("默认校验位"), self.parity_combo)

        serial_layout.addLayout(serial_form)
        root.addWidget(serial_card)

        # Buttons
        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("保存设置", self)
        self.apply_btn = QPushButton("应用设置", self)
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.apply_btn)

        root.addLayout(btn_row)
        root.addStretch(1)

        self.save_btn.clicked.connect(self.save_settings)
        self.apply_btn.clicked.connect(self.apply_settings_now)

    def save_settings(self):
        self.settings.setValue("general/theme", self.theme_combo.currentText())
        self.settings.setValue("general/showSidebarOnStart", self.sidebar_checkbox.isChecked())
        self.settings.setValue("general/defaultViewMode", self.default_view_combo.currentText())
        self.settings.setValue("general/showSplashOnStart", self.splash_checkbox.isChecked())
        self.settings.setValue("general/splashStyle", self.splash_style_combo.currentText())
        self.settings.setValue("general/splashDurationMs", int(self.splash_duration_spin.value()))
        self.settings.setValue("general/splashGifPath", self.splash_gif_edit.text().strip())
        self.settings.setValue("general/tailLength", int(self.tail_len_spin.value()))
        self.settings.setValue("general/tailFadePower", float(self.tail_fade_spin.value()))
        self.settings.setValue("maze/goalMinX", int(self.goal_min_x_spin.value()))
        self.settings.setValue("maze/goalMaxX", int(self.goal_max_x_spin.value()))
        self.settings.setValue("maze/goalMinY", int(self.goal_min_y_spin.value()))
        self.settings.setValue("maze/goalMaxY", int(self.goal_max_y_spin.value()))
        self.settings.setValue("maze/autoSendBestPath", self.auto_send_best_chk.isChecked())
        self.settings.setValue("replay/maxSaved", int(self.replay_max_spin.value()))
        self.settings.setValue("serial/baudRate", self.baud_combo.currentText())
        self.settings.setValue("serial/dataBits", self.data_bits_combo.currentText())
        self.settings.setValue("serial/stopBits", self.stop_bits_combo.currentText())
        self.settings.setValue("serial/parity", self.parity_combo.currentText())
        try:
            self.settings.sync()
        except Exception:
            pass
        QMessageBox.information(self, "设置", "已保存设置")

    def apply_settings_now(self):
        self.save_settings()
        if self.app_page is not None:
            self.app_page.reload_settings()
            # 同步尾迹参数到主界面
            if hasattr(self.app_page, "maze_plotter"):
                tail_len = int(self.tail_len_spin.value())
                tail_fade = float(self.tail_fade_spin.value())
                self.app_page.maze_plotter.set_tail_style(tail_len, tail_fade)
            # 同步终点/路径/视图默认配置
            self.app_page.goal_min_x = int(self.goal_min_x_spin.value())
            self.app_page.goal_max_x = int(self.goal_max_x_spin.value())
            self.app_page.goal_min_y = int(self.goal_min_y_spin.value())
            self.app_page.goal_max_y = int(self.goal_max_y_spin.value())
            self.app_page.auto_send_best_path = self.auto_send_best_chk.isChecked()
            self.app_page.max_replay_saved = int(self.replay_max_spin.value())
            # 默认视图
            self.app_page.default_view_mode = self.default_view_combo.currentText()

class DocsPage(QWidget):
    """美观简约的使用说明页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("docsPage")
        
        # 主布局：滚动区域
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(32, 32, 32, 32)
        scroll_layout.setSpacing(24)
        
        # 标题区域
        title_card = QWidget()
        title_card.setObjectName("titleCard")
        title_layout = QVBoxLayout(title_card)
        title_layout.setContentsMargins(24, 24, 24, 24)
        title_layout.setSpacing(8)
        
        title_label = QLabel("📖 使用说明")
        title_label.setObjectName("pageTitle")
        subtitle_label = QLabel("快速了解如何使用电脑鼠迷宫上位机")
        subtitle_label.setObjectName("pageSubtitle")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        scroll_layout.addWidget(title_card)
        
        # 基本操作卡片
        basic_card = self._create_section_card(
            "🚀 基本操作",
            [
                "1. 在「串口配置」区域选择串口和波特率等参数",
                "2. 点击「连接」按钮建立串口连接",
                "3. 在「发送数据」输入框中输入命令并发送",
                "4. 在「控制面板」中使用开始/停止/复位功能",
                "5. 实时查看「传感器数据」和「迷宫轨迹」"
            ]
        )
        scroll_layout.addWidget(basic_card)
        
        # 协议说明卡片
        protocol_card = self._create_section_card(
            "📡 通信协议",
            [
                "帧格式：s,X,Y,O,Angle,Front,Left,Right,Mode\\r\\n",
                "",
                "参数说明：",
                "  • X, Y：坐标位置（0-7）",
                "  • O：朝向（0=北, 1=东, 2=南, 3=西）",
                "  • Angle：陀螺仪角度（度，0度=北，顺时针增加）",
                "  • Front：前传感器值（0=有墙, 1=无墙）",
                "  • Left：左传感器值（0=有墙, 1=无墙）",
                "  • Right：右传感器值（0=有墙, 1=无墙）",
                "  • Mode：运行模式（0=停止, 1=迷宫模式）",
                "",
                "示例：",
                "  s,3,4,1,45.5,0,1,1,1\\r\\n",
                "  表示：位置(3,4)，朝东，角度45.5°，前方有墙，左右无墙，迷宫模式"
            ]
        )
        scroll_layout.addWidget(protocol_card)
        
        # 功能特性卡片
        features_card = self._create_section_card(
            "✨ 功能特性",
            [
                "• 实时轨迹可视化：动态显示电脑鼠在迷宫中的移动轨迹",
                "• 自动墙体绘制：根据传感器数据自动判断并绘制迷宫墙体",
                "• 传感器监控：实时显示前后左右传感器状态",
                "• 轨迹回放：保存并回放历史运行轨迹",
                "• 数据导出：支持导出日志、轨迹等数据",
                "• 现代化界面：简洁美观的用户界面设计"
            ]
        )
        scroll_layout.addWidget(features_card)
        
        scroll_layout.addStretch(1)
        
        # 使用QScrollArea包装
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        main_layout.addWidget(scroll_area)
    
    def _create_section_card(self, title: str, items: list) -> QWidget:
        """创建统一的章节卡片"""
        card = QWidget()
        card.setObjectName("sectionCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(12)
        
        title_label = QLabel(title)
        title_label.setObjectName("sectionTitle")
        card_layout.addWidget(title_label)
        
        for item in items:
            if item.strip():
                content_label = QLabel(item)
                content_label.setObjectName("sectionContent")
                content_label.setWordWrap(True)
                card_layout.addWidget(content_label)
            else:
                card_layout.addSpacing(8)
        
        return card

class AboutPage(QWidget):
    """美观简约的关于页面 - 显示应用信息和开发者信息"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("aboutPage")
        
        # 主布局：滚动区域
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(32, 32, 32, 32)
        scroll_layout.setSpacing(24)
        
        # 应用信息卡片（大卡片，居中显示）
        app_card = QWidget()
        app_card.setObjectName("appInfoCard")
        app_layout = QVBoxLayout(app_card)
        app_layout.setContentsMargins(40, 40, 40, 40)
        app_layout.setSpacing(16)
        app_layout.setAlignment(Qt.AlignCenter)
        
        # 应用图标/名称
        app_name_label = QLabel(APP_NAME)
        app_name_label.setObjectName("appNameLabel")
        app_layout.addWidget(app_name_label, alignment=Qt.AlignCenter)
        
        # 版本号
        version_label = QLabel(f"版本 {APP_VERSION}")
        version_label.setObjectName("versionLabel")
        app_layout.addWidget(version_label, alignment=Qt.AlignCenter)
        
        # 描述
        desc_label = QLabel("电子系统课程设计项目\n实时监控与可视化电脑鼠迷宫探索")
        desc_label.setObjectName("appDescLabel")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        app_layout.addWidget(desc_label, alignment=Qt.AlignCenter)
        
        scroll_layout.addWidget(app_card)
        
        # 开发者信息卡片
        dev_card = self._create_info_card(
            "👨‍💻 开发者信息",
            [
                ("开发者", APP_DEVELOPER),
                ("学校", APP_SCHOOL),
                ("项目", APP_PROJECT),
                ("邮箱", APP_EMAIL),
                ("网址", APP_URL if APP_URL else "暂无")
            ]
        )
        scroll_layout.addWidget(dev_card)
        
        # 技术栈卡片
        tech_card = self._create_info_card(
            "🔧 技术栈",
            [
                ("GUI框架", f"PyQt5 {PYQT_VERSION_STR}"),
                ("Qt版本", QT_VERSION_STR),
                ("Python版本", sys.version.split(" ")[0]),
                ("绘图库", "Matplotlib"),
                ("通信协议", "串口通信 (QSerialPort)")
            ]
        )
        scroll_layout.addWidget(tech_card)
        
        # 版权信息卡片
        copyright_card = QWidget()
        copyright_card.setObjectName("sectionCard")
        copyright_layout = QVBoxLayout(copyright_card)
        copyright_layout.setContentsMargins(24, 20, 24, 20)
        copyright_layout.setSpacing(12)
        
        copyright_title = QLabel("📄 版权信息")
        copyright_title.setObjectName("sectionTitle")
        copyright_layout.addWidget(copyright_title)
        
        copyright_text = QLabel(
            f"{APP_COPYRIGHT} {APP_DEVELOPER}\n\n"
            "本软件为电子系统设计课程项目，仅供学习交流使用。\n"
            "所有权利保留。"
        )
        copyright_text.setObjectName("sectionContent")
        copyright_text.setWordWrap(True)
        copyright_layout.addWidget(copyright_text)
        
        scroll_layout.addWidget(copyright_card)
        
        # 操作按钮区域
        buttons_card = QWidget()
        buttons_card.setObjectName("sectionCard")
        buttons_layout = QVBoxLayout(buttons_card)
        buttons_layout.setContentsMargins(24, 20, 24, 20)
        buttons_layout.setSpacing(12)
        
        # 按钮标题
        buttons_title = QLabel("🔗 快速操作")
        buttons_title.setObjectName("sectionTitle")
        buttons_layout.addWidget(buttons_title)
        
        # 按钮行
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        
        # 复制邮箱按钮
        copy_email_btn = QPushButton("📧 复制邮箱", self)
        copy_email_btn.clicked.connect(lambda: self._copy_to_clipboard(APP_EMAIL, "邮箱"))
        btn_row.addWidget(copy_email_btn)

        # 复制版本信息按钮
        copy_info_btn = QPushButton("📋 复制应用信息", self)
        copy_info_btn.clicked.connect(self._copy_app_info)
        btn_row.addWidget(copy_info_btn)

        # 检查更新按钮
        check_update_btn = QPushButton("🔄 检查更新", self)
        check_update_btn.clicked.connect(self._check_for_updates)
        btn_row.addWidget(check_update_btn)
        
        btn_row.addStretch(1)
        buttons_layout.addLayout(btn_row)
        scroll_layout.addWidget(buttons_card)
        
        scroll_layout.addStretch(1)
        
        # 使用QScrollArea包装
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        main_layout.addWidget(scroll_area)
    
    def _create_info_card(self, title: str, items: list) -> QWidget:
        """创建信息展示卡片"""
        card = QWidget()
        card.setObjectName("sectionCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(12)
        
        title_label = QLabel(title)
        title_label.setObjectName("sectionTitle")
        card_layout.addWidget(title_label)
        
        for key, value in items:
            info_layout = QHBoxLayout()
            info_layout.setSpacing(16)
            
            key_label = QLabel(f"{key}:")
            key_label.setObjectName("infoKeyLabel")
            key_label.setMinimumWidth(100)
            info_layout.addWidget(key_label)
            
            value_label = QLabel(value)
            value_label.setObjectName("infoValueLabel")
            value_label.setWordWrap(True)
            info_layout.addWidget(value_label, 1)
            
            card_layout.addLayout(info_layout)
        
        return card
    
    def _copy_to_clipboard(self, text: str, label: str):
        """复制文本到剪贴板"""
        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "复制成功", f"{label}已复制到剪贴板：\n{text}")
    
    def _copy_app_info(self):
        """复制应用信息到剪贴板"""
        info = f"""应用名称：{APP_NAME}
版本：{APP_VERSION}
开发者：{APP_DEVELOPER}
学校：{APP_SCHOOL}
项目：{APP_PROJECT}
邮箱：{APP_EMAIL}
网址：{APP_URL}
Python：{sys.version.split(' ')[0]}
Qt：{QT_VERSION_STR}
PyQt5：{PYQT_VERSION_STR}
"""
        QGuiApplication.clipboard().setText(info)
        QMessageBox.information(self, "复制成功", "应用信息已复制到剪贴板")
    
    def _check_for_updates(self):
        """检查更新功能 - 从服务器或本地版本文件检查"""
        # 显示检查中的提示（非模态对话框）
        checking_msg = QMessageBox(self)
        checking_msg.setWindowTitle("检查更新")
        checking_msg.setText("正在检查更新...")
        checking_msg.setStandardButtons(QMessageBox.NoButton)
        checking_msg.setModal(False)  # 设置为非模态，避免阻塞
        checking_msg.show()
        # 确保对话框显示
        QApplication.processEvents()
        
        # 版本检查URL
        version_url_json = "http://154.219.114.232/version.json"
        version_url_txt = "http://154.219.114.232/version.txt"
        
        def check_update_in_thread():
            """在后台线程中执行更新检查"""
            import urllib.request
            import urllib.error
            import json
            import re
            import traceback
            
            latest_version = None
            download_url = None
            release_notes = ""
            error_msg = ""
            
            # 方法1：尝试从网络获取（如果有版本API）
            # 优先尝试JSON格式
            try:
                # User-Agent 必须使用 ASCII 字符，不能包含中文
                user_agent = f'MicromouseApp/{APP_VERSION}'
                req = urllib.request.Request(
                    version_url_json,
                    headers={'User-Agent': user_agent}
                )
                with urllib.request.urlopen(req, timeout=10) as response:
                    content = response.read().decode('utf-8')
                    # 解析JSON格式
                    data = json.loads(content)
                    latest_version = data.get('version')
                    download_url = data.get('download_url', '')
                    release_notes = data.get('release_notes', '')
                    print(f"[更新检查] 成功获取版本信息: {latest_version}")
            except urllib.error.HTTPError as e:
                error_msg = f"HTTP错误 {e.code}: {e.reason}"
                print(f"[更新检查] JSON请求失败: {error_msg}")
                # JSON格式失败，尝试文本格式
                try:
                    # User-Agent 必须使用 ASCII 字符，不能包含中文
                    user_agent = f'MicromouseApp/{APP_VERSION}'
                    req = urllib.request.Request(
                        version_url_txt,
                        headers={'User-Agent': user_agent}
                    )
                    with urllib.request.urlopen(req, timeout=10) as response:
                        content = response.read().decode('utf-8')
                        # 解析纯文本版本号
                        match = re.search(r'version[:\s]+([\d.]+)', content, re.IGNORECASE)
                        if not match:
                            match = re.search(r'(\d+\.\d+\.\d+)', content)
                        if match:
                            latest_version = match.group(1)
                            print(f"[更新检查] 文本格式获取版本: {latest_version}")
                except Exception as e2:
                    error_msg = f"文本格式也失败: {str(e2)}"
                    print(f"[更新检查] {error_msg}")
            except urllib.error.URLError as e:
                error_msg = f"网络连接错误: {str(e.reason)}"
                print(f"[更新检查] {error_msg}")
            except json.JSONDecodeError as e:
                error_msg = f"JSON解析错误: {str(e)}"
                print(f"[更新检查] {error_msg}")
            except Exception as e:
                error_msg = f"未知错误: {str(e)}"
                print(f"[更新检查] {error_msg}")
                traceback.print_exc()
            
            # 方法2：本地版本文件检查（作为备选方案）
            if latest_version is None:
                try:
                    import os
                    app_dir = QApplication.instance().applicationDirPath() if QApplication.instance() else os.getcwd()
                    version_file = os.path.join(app_dir, 'version_info.json')
                    if os.path.exists(version_file):
                        with open(version_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            latest_version = data.get('version', APP_VERSION)
                            download_url = data.get('download_url', APP_URL)
                            release_notes = data.get('release_notes', '')
                            print(f"[更新检查] 使用本地版本文件: {latest_version}")
                except Exception as e:
                    print(f"[更新检查] 本地版本文件读取失败: {str(e)}")
            
            # 在主线程中更新UI
            # 使用队列在线程间传递结果
            print(f"[更新检查] 准备显示结果: latest_version={latest_version}, download_url={download_url}")
            
            # 将结果放入队列，由主线程的定时器检查
            result_queue.put((
                latest_version, download_url, release_notes, error_msg
            ))
        
        # 创建结果队列
        result_queue = queue.Queue()
        
        # 在后台线程中执行网络请求
        thread = threading.Thread(target=check_update_in_thread, daemon=True)
        thread.start()
        
        # 使用定时器定期检查结果队列
        def check_result():
            try:
                latest_version, download_url, release_notes, error_msg = result_queue.get_nowait()
                timer.stop()
                # 关闭检查中的对话框
                checking_msg.hide()  # 先隐藏
                checking_msg.close()  # 然后关闭
                checking_msg.deleteLater()  # 标记为待删除，确保完全释放
                # 处理事件，确保对话框关闭
                QApplication.processEvents()
                # 稍微延迟，确保对话框完全关闭
                QTimer.singleShot(50, lambda: self._show_update_result(
                    latest_version, download_url, release_notes, error_msg
                ))
            except queue.Empty:
                pass
        
        timer = QTimer(self)
        timer.timeout.connect(check_result)
        timer.start(100)  # 每100ms检查一次
    
    def _show_update_result(self, latest_version, download_url, release_notes, error_msg):
        """在主线程中显示更新检查结果"""
        # 比较版本号
        if latest_version:
            if self._compare_versions(APP_VERSION, latest_version) < 0:
                # 有新版本
                msg_text = (
                    f"发现新版本！\n\n"
                    f"当前版本：{APP_VERSION}\n"
                    f"最新版本：{latest_version}\n\n"
                )
                if release_notes:
                    # 处理换行符
                    notes = release_notes.replace('\\n', '\n')
                    msg_text += f"{notes}\n\n"
                msg_text += "是否访问下载页面？"
                
                msg = QMessageBox(self)
                msg.setWindowTitle("发现新版本")
                msg.setIcon(QMessageBox.Information)
                msg.setText(msg_text)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setDefaultButton(QMessageBox.Yes)
                
                if msg.exec_() == QMessageBox.Yes:
                    # 打开下载链接
                    import webbrowser
                    target_url = download_url if download_url else APP_URL
                    webbrowser.open(target_url)
            else:
                # 已是最新版本
                QMessageBox.information(
                    self,
                    "检查更新",
                    f"当前版本：{APP_VERSION}\n\n"
                    "您使用的是最新版本！"
                )
        else:
            # 无法检查更新
            error_info = f"\n\n错误信息：{error_msg}" if error_msg else ""
            QMessageBox.warning(
                self,
                "检查更新",
                f"当前版本：{APP_VERSION}\n\n"
                "无法连接到更新服务器。" + error_info + "\n\n"
                "请检查网络连接或稍后重试。\n\n"
                f"更新服务器地址：http://154.219.114.232/version.json"
            )
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """比较版本号
        返回: -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2
        """
        def normalize_version(v):
            # 将版本号转换为可比较的元组
            parts = []
            for part in v.split('.'):
                try:
                    parts.append(int(part))
                except ValueError:
                    parts.append(0)
            # 补齐到3位
            while len(parts) < 3:
                parts.append(0)
            return tuple(parts)
        
        n1 = normalize_version(v1)
        n2 = normalize_version(v2)
        
        if n1 < n2:
            return -1
        elif n1 > n2:
            return 1
        else:
            return 0

class SupportPage(QWidget):
    def __init__(self, parent=None, app_page: 'MicroMouseApp' = None):
        super().__init__(parent)
        self.setObjectName("supportPage")
        self.app_page = app_page

        outer = QVBoxLayout(self)
        form = QFormLayout()
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(8)

        # Basic env info
        self.lbl_py = QLabel(sys.version.split(" ")[0])
        self.lbl_qt = QLabel(QT_VERSION_STR)
        self.lbl_pyqt = QLabel(PYQT_VERSION_STR)
        self.lbl_ports = QLabel("点击刷新…")
        form.addRow(QLabel("Python:"), self.lbl_py)
        form.addRow(QLabel("Qt 版本:"), self.lbl_qt)
        form.addRow(QLabel("GUI 框架:"), self.lbl_pyqt)
        form.addRow(QLabel("可用串口:"), self.lbl_ports)

        # Buttons
        btn_row = QHBoxLayout()
        self.refresh_btn = QPushButton("刷新串口", self)
        self.copy_btn = QPushButton("复制诊断", self)
        btn_row.addWidget(self.refresh_btn)
        btn_row.addWidget(self.copy_btn)

        outer.addLayout(form)
        outer.addLayout(btn_row)
        outer.addStretch(1)

        self.refresh_btn.clicked.connect(self.refresh_ports)
        self.copy_btn.clicked.connect(self.copy_diagnostics)
        self.refresh_ports()

    def refresh_ports(self):
        try:
            ports = [p.portName() for p in QSerialPortInfo.availablePorts()]
            self.lbl_ports.setText(", ".join(ports) if ports else "(无)")
        except Exception as e:
            self.lbl_ports.setText(f"错误: {e}")

    def build_diagnostics(self) -> str:
        from datetime import datetime
        lines = []
        lines.append(f"时间: {datetime.now().isoformat(timespec='seconds')}")
        lines.append(f"Python: {sys.version}")
        lines.append(f"Qt: {QT_VERSION_STR}")
        lines.append(f"PyQt: {PYQT_VERSION_STR}")
        # Screen info
        try:
            screen = QGuiApplication.primaryScreen()
            if screen is not None:
                size = screen.size()
                lines.append(f"屏幕: {size.width()}x{size.height()}")
        except Exception:
            pass
        # Ports
        try:
            ports = [p.portName() for p in QSerialPortInfo.availablePorts()]
            lines.append("串口: " + (", ".join(ports) if ports else "(无)"))
        except Exception as e:
            lines.append(f"串口查询错误: {e}")

        return "\n".join(lines)

    def copy_diagnostics(self):
        text = self.build_diagnostics()
        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "诊断", "诊断信息已复制到剪贴板")

class RealtimeLogPage(QWidget):
    def __init__(self, parent=None, app_page: 'MicroMouseApp' = None):
        super().__init__(parent)
        self.setObjectName("realtimeLogPage")
        self.app_page = app_page

        root = QVBoxLayout(self)

        # Controls row: filter + pause + export
        tools = QHBoxLayout()
        self.filter_edit = QLineEdit(self)
        self.filter_edit.setPlaceholderText("过滤关键字（留空不过滤）")
        self.pause_chk = QCheckBox("暂停滚动", self)
        self.show_rx_chk = QCheckBox("显示接收", self)
        self.show_rx_chk.setChecked(True)
        self.show_tx_chk = QCheckBox("显示发送", self)
        self.show_tx_chk.setChecked(True)
        self.export_btn = QPushButton("导出日志", self)
        tools.addWidget(QLabel("筛选:"))
        tools.addWidget(self.filter_edit, 1)
        tools.addWidget(self.show_rx_chk)
        tools.addWidget(self.show_tx_chk)
        tools.addWidget(self.pause_chk)
        tools.addWidget(self.export_btn)

        # Split RX/TX consoles
        splitter = QSplitter(Qt.Vertical)
        self.rx_edit = QTextEdit(self)
        self.rx_edit.setReadOnly(True)
        self.rx_edit.setPlaceholderText("接收日志…")
        self.tx_edit = QTextEdit(self)
        self.tx_edit.setReadOnly(True)
        self.tx_edit.setPlaceholderText("发送日志…")
        splitter.addWidget(self.rx_edit)
        splitter.addWidget(self.tx_edit)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        # Stats row
        stats_row = QHBoxLayout()
        self.lbl_rx_bps = QLabel("RX: 0 bps")
        self.lbl_tx_bps = QLabel("TX: 0 bps")
        self.lbl_err = QLabel("错误帧: 0")
        stats_row.addWidget(self.lbl_rx_bps)
        stats_row.addSpacing(12)
        stats_row.addWidget(self.lbl_tx_bps)
        stats_row.addSpacing(12)
        stats_row.addWidget(self.lbl_err)
        stats_row.addStretch(1)

        root.addLayout(tools)
        root.addWidget(splitter)
        root.addLayout(stats_row)

        # Wire
        if self.app_page is not None:
            self.app_page.log_subscribers.append(self.on_log)

        self.export_btn.clicked.connect(self.export_logs)

        # Timer for throughput
        self._stats_timer = QTimer(self)
        self._stats_timer.setInterval(500)
        self._stats_timer.timeout.connect(self.update_stats)
        self._stats_timer.start()

        self._rx_buffer = []
        self._tx_buffer = []

    def on_log(self, timestamp: str, direction: str, text: str):
        # filter
        key = self.filter_edit.text().strip()
        if key and key not in text and key not in direction:
            return
        if direction == 'RX' and not self.show_rx_chk.isChecked():
            return
        if direction == 'TX' and not self.show_tx_chk.isChecked():
            return
        line = f"[{timestamp}] {direction} {text}"
        if direction == 'RX':
            self._rx_buffer.append(line)
            self.rx_edit.append(line)
            if not self.pause_chk.isChecked():
                self.rx_edit.moveCursor(self.rx_edit.textCursor().End)
        else:
            self._tx_buffer.append(line)
            self.tx_edit.append(line)
            if not self.pause_chk.isChecked():
                self.tx_edit.moveCursor(self.tx_edit.textCursor().End)

    def update_stats(self):
        if self.app_page is None:
            return
        rx_bps, tx_bps = self.app_page.get_throughput_bps()
        self.lbl_rx_bps.setText(f"RX: {rx_bps} bps")
        self.lbl_tx_bps.setText(f"TX: {tx_bps} bps")
        self.lbl_err.setText(f"错误帧: {self.app_page.error_frame_count}")

    def export_logs(self):
        all_text = "\n".join(["--- RX ---"] + self._rx_buffer + ["", "--- TX ---"] + self._tx_buffer)
        path, _ = QFileDialog.getSaveFileName(self, "导出日志", "logs.txt", "Text Files (*.txt)")
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(all_text)
                QMessageBox.information(self, "导出日志", "日志已保存")
            except Exception as e:
                QMessageBox.critical(self, "导出失败", str(e))

class ReplayPage(QWidget):
    """轨迹回放页：列表查看、播放/暂停/倍速、叠加对比、导出"""
    def __init__(self, parent=None, app_page: 'MicroMouseApp' = None):
        super().__init__(parent)
        self.setObjectName("replayPage")
        self.app_page = app_page
        self.current_run = None

        root = QVBoxLayout(self)
        top = QHBoxLayout()
        root.addLayout(top)

        # 左侧：列表与操作
        left = QVBoxLayout()
        self.list = QListWidget(self)
        self.list.setSelectionMode(QListWidget.ExtendedSelection)
        self.list.itemSelectionChanged.connect(self.draw_selected)
        left.addWidget(self.list)

        btn_row1 = QHBoxLayout()
        self.btn_refresh = QPushButton("刷新列表", self)
        self.btn_save = QPushButton("保存当前轨迹", self)
        btn_row1.addWidget(self.btn_refresh)
        btn_row1.addWidget(self.btn_save)
        left.addLayout(btn_row1)

        # 改为直接展示，无播放控制
        btn_row2 = QHBoxLayout()
        self.overlay_chk = QCheckBox("叠加多条轨迹", self)
        self.overlay_chk.stateChanged.connect(self.draw_selected)
        btn_row2.addWidget(self.overlay_chk)
        btn_row2.addStretch(1)
        left.addLayout(btn_row2)

        btn_row4 = QHBoxLayout()
        self.btn_export_csv = QPushButton("导出 CSV", self)
        self.btn_export_png = QPushButton("导出 PNG", self)
        btn_row4.addWidget(self.btn_export_csv)
        btn_row4.addWidget(self.btn_export_png)
        left.addLayout(btn_row4)

        top.addLayout(left, 1)

        # 右侧：绘图
        self.replay_fig = Figure(figsize=(5, 5), dpi=100, facecolor='#fafbfc')
        self.replay_ax = self.replay_fig.add_subplot(111)
        self._init_plot_style()
        self.replay_canvas = FigureCanvas(self.replay_fig)
        top.addWidget(self.replay_canvas, 2)

        # 绑定事件
        self.btn_refresh.clicked.connect(self.refresh_list)
        self.btn_save.clicked.connect(self.save_current_run)
        self.btn_export_csv.clicked.connect(self.export_csv)
        self.btn_export_png.clicked.connect(self.export_png)

        # 初始数据
        self.refresh_list()
        self.draw_selected()

    def _init_plot_style(self):
        ax = self.replay_ax
        ax.clear()
        ax.set_facecolor('#ffffff')
        ax.set_xlim(-0.5, 8.5)
        ax.set_ylim(-0.5, 8.5)
        ax.set_xticks(range(9))
        ax.set_yticks(range(9))
        ax.grid(True, color='#e5e7eb', linewidth=0.9, alpha=0.8)
        for spine in ax.spines.values():
            spine.set_color('#e5e7eb')
            spine.set_linewidth(1.0)
        ax.set_title("轨迹回放", color="#111827", fontsize=14, fontweight='600', pad=12)

    def refresh_list(self):
        self.list.clear()
        if not self.app_page:
            return
        for run in self.app_page.replay_runs:
            item = QListWidgetItem(run.get("name", ""))
            self.list.addItem(item)

    def save_current_run(self):
        if not self.app_page:
            return
        name = f"run_{len(self.app_page.replay_runs)+1}"
        self.app_page.snapshot_current_run(name=name)
        self.refresh_list()
        QMessageBox.information(self, "保存轨迹", f"已保存为 {name}")

    def draw_selected(self):
        self._init_plot_style()
        if not self.app_page:
            self.replay_canvas.draw_idle()
            return
        selected = [i.row() for i in self.list.selectedIndexes()]
        if not selected and self.app_page.replay_runs:
            selected = [len(self.app_page.replay_runs) - 1]
            self.list.setCurrentRow(selected[0])
        palette = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#0ea5e9", "#3b82f6"]
        draw_all = self.overlay_chk.isChecked()
        targets = selected if draw_all else selected[:1]
        for k, idx in enumerate(targets):
            if idx >= len(self.app_page.replay_runs):
                continue
            run = self.app_page.replay_runs[idx]
            xs = run.get("path_x", [])
            ys = run.get("path_y", [])
            color = palette[k % len(palette)]
            self.replay_ax.plot(xs, ys, color=color, linewidth=2.5, alpha=0.9)
            if xs and ys:
                self.replay_ax.plot(xs[0], ys[0], 'o', color="#22c55e", markersize=8, markeredgecolor="#fff", markeredgewidth=2)
                self.replay_ax.plot(xs[-1], ys[-1], 'o', color="#ef4444", markersize=9, markeredgecolor="#fff", markeredgewidth=2)
        self.replay_canvas.draw_idle()

    def export_csv(self):
        if not self.app_page:
            return
        idxs = self.list.selectedIndexes()
        if not idxs:
            QMessageBox.warning(self, "导出", "请选择要导出的轨迹")
            return
        sel = idxs[0].row()
        run = self.app_page.replay_runs[sel] if sel < len(self.app_page.replay_runs) else None
        if not run:
            return
        path, _ = QFileDialog.getSaveFileName(self, "导出轨迹 CSV", f"{run.get('name','run')}.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("x,y\n")
                for x, y in zip(run.get("path_x", []), run.get("path_y", [])):
                    f.write(f"{x},{y}\n")
            QMessageBox.information(self, "导出", "CSV 导出成功")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", str(e))

    def export_png(self):
        idxs = self.list.selectedIndexes()
        if not idxs:
            QMessageBox.warning(self, "导出", "请选择要导出的轨迹")
            return
        # 先绘制叠加（如果需要）
        self.draw_overlay()
        path, _ = QFileDialog.getSaveFileName(self, "导出轨迹 PNG", "replay.png", "PNG Files (*.png)")
        if not path:
            return
        try:
            self.replay_fig.savefig(path, dpi=180, bbox_inches='tight')
            QMessageBox.information(self, "导出", "PNG 导出成功")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", str(e))


class StartupSplash(QWidget):
    def __init__(self, theme: str = "light", mode: str = "progress", duration_ms: int = 1800, gif_path: str = ""):
        super().__init__(None, Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setObjectName("startupSplash")

        self._mode = mode  # "progress" | "gif"
        self._duration_ms = max(300, int(duration_ms))
        self._movie = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(0)

        card = QWidget(self)
        card.setObjectName("splashCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QLabel(APP_NAME, card)
        subtitle = QLabel(f"{APP_SCHOOL} · {APP_PROJECT}", card)
        title_style_light = "font-size:18px; font-weight:700; color:#111827;"
        sub_style_light = "font-size:12px; color:#4b5563;"
        title_style_dark = "font-size:18px; font-weight:700; color:#f9fafb;"
        sub_style_dark = "font-size:12px; color:#d1d5db;"
        is_dark = str(theme).lower() == "dark"
        if is_dark:
            title.setStyleSheet(title_style_dark)
            subtitle.setStyleSheet(sub_style_dark)
            card.setStyleSheet("#splashCard{background:#212121; border:1px solid #424242; border-radius:20px;}")
        else:
            title.setStyleSheet(title_style_light)
            subtitle.setStyleSheet(sub_style_light)
            card.setStyleSheet("#splashCard{background:#ffffff; border:1px solid #e0e0e0; border-radius:20px;}")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Content area: gif or progress
        self._content_wrap = QWidget(card)
        content_layout = QVBoxLayout(self._content_wrap)
        content_layout.setContentsMargins(0, 8, 0, 0)
        content_layout.setSpacing(8)

        if self._mode == "gif" and gif_path:
            self._gif_label = QLabel(self._content_wrap)
            self._gif_label.setAlignment(Qt.AlignCenter)
            try:
                self._movie = QMovie(gif_path)
                self._gif_label.setMovie(self._movie)
                self._movie.start()
            except Exception:
                self._gif_label.setText("加载 GIF 失败，切换为进度条模式…")
                self._mode = "progress"
            content_layout.addWidget(self._gif_label)

        if self._mode != "gif":
            self._progress = QProgressBar(self._content_wrap)
            self._progress.setRange(0, 0)  # 不确定进度，使用忙等待样式
            self._progress.setTextVisible(False)
            # 确保完整可见与适配主题
            self._progress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self._progress.setMinimumWidth(360)
            self._progress.setFixedHeight(12)
            if is_dark:
                self._progress.setStyleSheet(
                    "QProgressBar{background-color:#424242; border:1px solid #616161; border-radius:12px;}"
                    "QProgressBar::chunk{background-color:#2196f3; border-radius:12px;}"
                )
            else:
                self._progress.setStyleSheet(
                    "QProgressBar{background-color:#e0e0e0; border:1px solid #bdbdbd; border-radius:12px;}"
                    "QProgressBar::chunk{background-color:#2196f3; border-radius:12px;}"
                )
            content_layout.addWidget(self._progress)

        layout.addWidget(self._content_wrap)
        outer.addWidget(card)

        self.resize(460, 240)
        try:
            screen = QGuiApplication.primaryScreen()
            if screen is not None:
                geo = screen.geometry()
                self.move(
                    geo.center().x() - self.width() // 2,
                    geo.center().y() - self.height() // 2,
                )
        except Exception:
            pass

        # Auto-close timer
        self._close_timer = QTimer(self)
        self._close_timer.setSingleShot(True)
        self._close_timer.setInterval(self._duration_ms)
        self._close_timer.timeout.connect(self.finish)
        self._close_timer.start()

    def finish(self):
        try:
            if self._movie is not None:
                self._movie.stop()
        except Exception:
            pass
        self.close()

def run_fluent_window():
    # Create a FluentWindow shell and add pages
    from qfluentwidgets import FluentWindow
    win = FluentWindow()
    win.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
    # Enable Windows 11 Mica (fallback自动存在)
    try:
        win.setMicaEffectEnabled(True)
    except Exception:
        pass

    # Main run page
    run_page_container = QWidget()
    run_page_container.setObjectName("runPage")
    run_layout = QVBoxLayout(run_page_container)
    # 将现有界面作为子页面嵌入
    app_page = MicroMouseApp(as_page=True)
    run_layout.addWidget(app_page.central_widget)

    # 迷宫绘图页就是主页面；可再添加设置/关于等
    win.addSubInterface(run_page_container, FIF.HOME, "运行", NavigationItemPosition.TOP)

    # 设置页
    settings_page = SettingsPage(parent=win, app_page=app_page)
    win.addSubInterface(settings_page, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM)

    # 文档与支持页（放底部）
    docs_page = DocsPage(parent=win)
    win.addSubInterface(docs_page, FIF.BOOK_SHELF, "使用说明", NavigationItemPosition.BOTTOM)

    # 关于页面
    about_page = AboutPage(parent=win)
    try:
        # 尝试使用INFO图标，如果不可用则使用HELP
        about_icon = getattr(FIF, "INFO", FIF.HELP) if QFW_AVAILABLE else None
    except:
        about_icon = FIF.HELP if QFW_AVAILABLE else None
    win.addSubInterface(about_page, about_icon, "关于", NavigationItemPosition.BOTTOM)

    support_page = SupportPage(parent=win, app_page=app_page)
    win.addSubInterface(support_page, FIF.SETTING, "支持/诊断", NavigationItemPosition.BOTTOM)

    # 实时数据与日志
    rtlog_page = RealtimeLogPage(parent=win, app_page=app_page)
    win.addSubInterface(rtlog_page, FIF.SEND, "实时日志", NavigationItemPosition.TOP)

    # 轨迹回放页
    replay_page = ReplayPage(parent=win, app_page=app_page)
    win.addSubInterface(replay_page, FIF.INFO, "轨迹回放", NavigationItemPosition.TOP)

    win.resize(1200, 760)
    win.show()
    return win


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 可选启动动画
    settings = QSettings("MicromouseLab", "MicromouseApp")
    try:
        settings.sync()
    except Exception:
        pass
    show_splash = settings.value("general/showSplashOnStart", True, type=bool)
    splash_style = str(settings.value("general/splashStyle", "progress"))
    try:
        splash_duration = int(settings.value("general/splashDurationMs", 3000, type=int))
    except Exception:
        splash_duration = 3000
    splash_gif = str(settings.value("general/splashGifPath", ""))
    theme_pref = str(settings.value("general/theme", "light"))
    splash = None
    if show_splash:
        try:
            splash = StartupSplash(theme=theme_pref, mode=splash_style, duration_ms=splash_duration, gif_path=splash_gif)
            splash.show()
            # 让动画先渲染一帧
            app.processEvents()
        except Exception:
            splash = None

    # 使用标准 PyQt5 界面
    window = MicroMouseApp()
    window.show()
    sys.exit(app.exec_())
