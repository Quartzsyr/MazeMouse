# decompyle3 version 3.9.3
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.15 (default, Nov 24 2022, 14:38:14) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: main.py
"""电脑鼠迷宫上位机
开发者：石殷睿（苏州大学电子信息学院）
用途：电子系统课程设计
联系方式：yinrui_shi@163.com
"""
APP_VERSION = "3.4.2"
APP_NAME = "电脑鼠迷宫上位机"
APP_DEVELOPER = "石殷睿"
APP_SCHOOL = "苏州大学电子信息学院"
APP_EMAIL = "yinrui_shi@163.com"
APP_PROJECT = "电子系统课程设计"
APP_URL = "https://www.quartz.xin"
APP_COPYRIGHT = "Copyright © 2025"
import sys, threading, queue
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QGridLayout, QComboBox, QPushButton, QLabel, QLineEdit, QMessageBox, QTextEdit, QMenuBar, QAction, QGroupBox, QSplitter, QStatusBar, QSizePolicy, QStackedWidget, QFormLayout, QCheckBox, QFileDialog, QProgressBar, QSpinBox, QDoubleSpinBox, QListWidget, QListWidgetItem, QScrollArea
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, Qt, QSettings, QT_VERSION_STR, PYQT_VERSION_STR, QTimer, QPoint, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QGuiApplication, QMovie, QIcon, QPainter, QPen, QBrush, QColor, QPolygon
from PyQt5.QtWidgets import QStyle
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
import numpy as np, time
from collections import deque
QFW_AVAILABLE = False
try:
    from qfluentwidgets import setTheme, Theme, setThemeColor, ComboBox as QfwComboBox, LineEdit as QfwLineEdit, PrimaryPushButton as QfwPrimaryPushButton, PushButton as QfwPushButton, InfoBar, InfoBarPosition, NavigationItemPosition, FluentWindow, FluentIcon as FIF
    QFW_AVAILABLE = True
except Exception:
    QFW_AVAILABLE = False

FRAM_AVAILABLE = False
try:
    from qframelesswindow import FramelessWindow, StandardTitleBar
    FRAM_AVAILABLE = True
except Exception:
    FRAM_AVAILABLE = False

plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

class CompassArea(QWidget):
            __doc__ = "指南针绘制区域"

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
                rect = self.rect()
                center_x = rect.width() / 2
                center_y = rect.height() / 2
                radius = min(center_x, center_y) - 5
                painter.setPen(QPen(QColor("#e2e8f0"), 2))
                painter.setBrush(QBrush(QColor("#f8fafc")))
                painter.drawEllipse(int(center_x - radius), int(center_y - radius), int(radius * 2), int(radius * 2))
                font = QFont("Arial", 8, QFont.Bold)
                painter.setFont(font)
                painter.setPen(QPen(QColor("#64748b"), 1))
                painter.drawText(int(center_x - 5), int(center_y - radius + 12), "N")
                painter.drawText(int(center_x + radius - 12), int(center_y + 4), "E")
                painter.drawText(int(center_x - 5), int(center_y + radius - 2), "S")
                painter.drawText(int(center_x - radius + 2), int(center_y + 4), "W")
                painter.save()
                painter.translate(center_x, center_y)
                qt_angle = 90 - self.angle
                painter.rotate(qt_angle)
                arrow_size = radius - 8
                painter.setPen(QPen(QColor("#10b981"), 3))
                painter.setBrush(QBrush(QColor("#10b981")))
                arrow_points = [
                 QPoint(0, -int(arrow_size)),
                 QPoint(-8, -int(arrow_size) + 12),
                 QPoint(-3, -int(arrow_size) + 8),
                 QPoint(-3, 0),
                 QPoint(3, 0),
                 QPoint(3, -int(arrow_size) + 8),
                 QPoint(8, -int(arrow_size) + 12)]
                polygon = QPolygon(arrow_points)
                painter.drawPolygon(polygon)
                painter.restore()
                painter.setPen(QPen(QColor("#0f172a"), 2))
                painter.setBrush(QBrush(QColor("#0f172a")))
                painter.drawEllipse(int(center_x - 3), int(center_y - 3), 6, 6)


class CompassWidget(QWidget):
            __doc__ = "角度显示组件 - 显示小车角度（0-360度）和动态指南针"

            def __init__(self, parent=None):
                super().__init__(parent)
                self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.setFixedSize(120, 120)
                self.setStyleSheet("\n            QWidget {\n                background-color: #ffffff;\n                border: 1px solid #e2e8f0;\n                border-radius: 8px;\n            }\n        ")
                layout = QVBoxLayout()
                layout.setContentsMargins(8, 8, 8, 8)
                layout.setSpacing(4)
                self.angle_label = QLabel("0.0°")
                self.angle_label.setStyleSheet("\n            QLabel {\n                color: #0f172a;\n                font-size: 16px;\n                font-weight: 600;\n                font-family: 'Microsoft YaHei', 'Arial';\n                background-color: transparent;\n            }\n        ")
                self.angle_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(self.angle_label)
                self.compass_area = CompassArea(self)
                self.compass_area.setFixedSize(80, 80)
                layout.addWidget((self.compass_area), alignment=(Qt.AlignCenter))
                self.setLayout(layout)
                self.current_angle = 0.0
                self.update_angle(0.0)

            def update_angle(self, angle_degrees: float):
                """更新角度显示（角度以度为单位，0-360度）"""
                self.current_angle = angle_degrees
                normalized_angle = angle_degrees % 360.0
                if normalized_angle < 0:
                    normalized_angle += 360.0
                self.angle_label.setText(f"{normalized_angle:.1f}°")
                self.compass_area.set_angle(normalized_angle)


class MazePlotter(FigureCanvas):

            def __init__(self, parent=None, width=5, height=5, dpi=100):
                fig = Figure(figsize=(width, height), dpi=dpi, facecolor="#fafbfc")
                self.axes = fig.add_subplot(111)
                super().__init__(fig)
                self.setParent(parent)
                self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.setMinimumSize(400, 300)
                self.path_points = []
                self.path_max_len = 200
                self.path_fade_power = 0.85
                self.path_collection = LineCollection([], linewidths=3.0, colors="#6366f1", alpha=0.9, zorder=5)
                self.axes.add_collection(self.path_collection)
                self.arrow_timer = QTimer(self)
                self.arrow_timer.setInterval(120)
                self.arrow_timer.timeout.connect(self._pulse_arrow)
                self.arrow_phase = 0.0
                self.arrow_timer.start()
                self.view_mode = "2D"
                self.axes_3d = None
                self.path_collection_3d = None
                self.mouse_pos_3d = None
                self.arrow_3d = None
                self.arrow_head_3d = None
                self.drawn_walls_3d = {}
                self.wall_data_cache = {}
                self.setup_maze_plot()

            def setup_maze_plot(self):
                """设置2D迷宫显示"""
                self.figure.clear()
                self.axes = self.figure.add_subplot(111)
                self.figure.patch.set_facecolor("#fafbfc")
                self.axes.set_facecolor("#ffffff")
                self.axes.set_aspect("equal", adjustable="box")
                self.axes.set_xlim(-0.5, 8.5)
                self.axes.set_ylim(-0.5, 8.5)
                self.axes.set_xticks(range(9))
                self.axes.set_yticks(range(9))
                self.axes.grid(True, color="#f1f5f9", linewidth=1.0, alpha=0.8, linestyle="-", zorder=1)
                self.axes.set_title("电脑鼠迷宫轨迹", color="#0f172a",
                  fontsize=16,
                  fontweight="600",
                  fontfamily="Microsoft YaHei",
                  pad=20)
                self.axes.tick_params(axis="x", colors="#64748b", labelsize=11, width=0.5)
                self.axes.tick_params(axis="y", colors="#64748b", labelsize=11, width=0.5)
                for spine in self.axes.spines.values():
                    spine.set_color("#e2e8f0")
                    spine.set_linewidth(1.2)

                self.mouse_pos, = self.axes.plot([], [], "o", color="#ef4444", markersize=14,
                  markeredgecolor="#ffffff",
                  markeredgewidth=2.5,
                  zorder=10)
                self.path_collection = LineCollection([], linewidths=3.0, colors="#6366f1", alpha=0.9, zorder=5)
                self.axes.add_collection(self.path_collection)
                self.arrow = None
                self.drawn_walls = {}
                self.draw()

            def draw_maze_wall(self, x, y, wall_direction):
                """绘制迷宫墙体（根据模式选择2D或3D）"""
                self.wall_data_cache[(x, y)] = wall_direction
                if self.view_mode == "3D":
                    self.draw_maze_wall_3d(x, y, wall_direction)
                    return
                line_width = 3.5
                line_color = "#1e293b"
                highlight_color = "#f97316"
                highlight_width = 4.5

                def _animate_wall(key, xs, ys):
                    if key not in self.drawn_walls:
                        wall = self.axes.plot(xs, ys, color=highlight_color, linewidth=highlight_width, alpha=0.0)[0]
                        self.drawn_walls[key] = wall
                        for step, alpha in enumerate([0.3, 0.6, 0.9, 1.0]):
                            QTimer.singleShot(step * 40, lambda w=wall, a=alpha: (w.set_alpha(a), self.draw_idle()))

                        QTimer.singleShot(200, lambda w=wall: (w.set_color(line_color), w.set_linewidth(line_width), self.draw_idle()))
                    else:
                        self.drawn_walls[key].set_data(xs, ys)

                def _remove_wall(key):
                    if key in self.drawn_walls:
                        try:
                            self.drawn_walls[key].remove()
                        except Exception:
                            pass
                        else:
                            del self.drawn_walls[key]

                if wall_direction & 1:
                    _animate_wall((x, y, "right"), [x + 1, x + 1], [y, y + 1])
                else:
                    _remove_wall((x, y, "right"))
                if wall_direction & 2:
                    _animate_wall((x, y, "top"), [x, x + 1], [y + 1, y + 1])
                else:
                    _remove_wall((x, y, "top"))
                if wall_direction & 4:
                    _animate_wall((x, y, "left"), [x, x], [y, y + 1])
                else:
                    _remove_wall((x, y, "left"))
                if wall_direction & 8:
                    _animate_wall((x, y, "bottom"), [x, x + 1], [y, y])
                else:
                    _remove_wall((x, y, "bottom"))
                self.draw()

            def update_plot(self, x, y, orientation, path_x, path_y):
                """更新显示（根据模式选择2D或3D）"""
                if self.view_mode == "3D":
                    self.update_plot_3d(x, y, orientation, path_x, path_y)
                    return
                self.mouse_pos.set_data([x], [y])
                points = list(zip(path_x, path_y))
                self.path_points = points[-self.path_max_len:]
                if len(self.path_points) >= 2:
                    segments = [[self.path_points[i], self.path_points[i + 1]] for i in range(len(self.path_points) - 1)]
                    n = len(segments)
                    base_rgba = mcolors.to_rgba("#6366f1")
                    fade_power = getattr(self, "path_fade_power", 0.85)
                    alphas = [0.08 + 0.92 * ((i + 1) / n) ** fade_power for i in range(n)]
                    colors = [(base_rgba[0], base_rgba[1], base_rgba[2], a) for a in alphas]
                    self.path_collection.set_segments(segments)
                    self.path_collection.set_color(colors)
                else:
                    self.path_collection.set_segments([])
                if self.arrow:
                    self.arrow.remove()
                dx, dy = (0, 0)
                if orientation == 0:
                    dx, dy = (0, 0.4)
                elif orientation == 1:
                    dx, dy = (0.4, 0)
                elif orientation == 2:
                    dx, dy = (0, -0.4)
                elif orientation == 3:
                    dx, dy = (-0.4, 0)
                self.arrow = self.axes.arrow(x, y, dx, dy, head_width=0.24,
                  head_length=0.24,
                  fc="#10b981",
                  ec="#059669",
                  linewidth=2.0,
                  zorder=15,
                  alpha=0.95)
                self.draw()

            def _pulse_arrow(self):
                """方向箭头呼吸动效：轻微变化透明度/线宽"""
                if self.view_mode == "3D":
                    if not self.arrow_3d:
                        return
                    self.arrow_phase = (self.arrow_phase + 0.2) % (2 * math.pi)
                    alpha = 0.75 + 0.2 * (0.5 * (1 + math.sin(self.arrow_phase)))
                    lw = 2.5 + 0.5 * (0.5 * (1 + math.sin(self.arrow_phase)))
                    try:
                        self.arrow_3d.set_alpha(alpha)
                        self.arrow_3d.set_linewidth(lw)
                        if self.arrow_head_3d:
                            self.arrow_head_3d.set_alpha(alpha)
                        self.draw_idle()
                    except Exception:
                        pass

                if not self.arrow:
                    return
                self.arrow_phase = (self.arrow_phase + 0.2) % (2 * math.pi)
                alpha = 0.75 + 0.2 * (0.5 * (1 + math.sin(self.arrow_phase)))
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
                for (x, y), wall_mask in self.wall_data_cache.items():
                    if wall_mask > 0:
                        self.draw_maze_wall(x, y, wall_mask)

            def setup_3d_plot(self):
                """设置3D迷宫显示"""
                self.figure.clear()
                self.axes_3d = self.figure.add_subplot(111, projection="3d")
                self.axes_3d.view_init(elev=75, azim=45)
                self.figure.patch.set_facecolor("#f5f5f5")
                self.axes_3d.set_facecolor("#2d2d2d")
                self.axes_3d.set_xlim(-0.5, 8.5)
                self.axes_3d.set_ylim(-0.5, 8.5)
                self.axes_3d.set_zlim(0, 0.05)
                self.axes_3d.set_xlabel("X", color="#9ca3af", fontsize=10)
                self.axes_3d.set_ylabel("Y", color="#9ca3af", fontsize=10)
                self.axes_3d.set_zlabel("Z", color="#9ca3af", fontsize=10)
                self.axes_3d.tick_params(axis="x", colors="#9ca3af", labelsize=9)
                self.axes_3d.tick_params(axis="y", colors="#9ca3af", labelsize=9)
                self.axes_3d.tick_params(axis="z", colors="#9ca3af", labelsize=9)
                self.axes_3d.set_title("电脑鼠迷宫轨迹 (3D)", color="#0f172a",
                  fontsize=16,
                  fontweight="600",
                  fontfamily="Microsoft YaHei",
                  pad=20)
                x_grid = np.arange(-0.5, 9.5, 0.1)
                y_grid = np.arange(-0.5, 9.5, 0.1)
                X_grid, Y_grid = np.meshgrid(x_grid, y_grid)
                Z_grid = np.zeros_like(X_grid)
                self.axes_3d.plot_surface(X_grid, Y_grid, Z_grid, alpha=0.9, color="#2d2d2d", linewidth=0,
                  antialiased=True,
                  shade=True)
                self.path_collection_3d = Line3DCollection([], linewidths=3.5, colors="#3b82f6", alpha=0.9)
                self.axes_3d.add_collection3d(self.path_collection_3d)
                self.mouse_pos_3d, = self.axes_3d.plot([], [], [], "o", color="#ef4444", markersize=16,
                  markeredgecolor="#ffffff",
                  markeredgewidth=3.0)
                self.arrow_3d = None
                self.arrow_head_3d = None
                self.drawn_walls_3d = {}
                if not hasattr(self, "wall_data_cache"):
                    self.wall_data_cache = {}
                self.draw()

            def draw_maze_wall_3d(self, x, y, wall_direction):
                """在3D模式下绘制墙体 - 参考真实迷宫风格，水平长方形贴地放置"""
                wall_thickness = 0.02
                wall_color = "#f5f5dc"
                red_stripe_color = "#dc2626"
                edge_color = "#d4d4d4"
                highlight_color = "#f97316"
                stripe_thickness = 0.005

                def _animate_wall_3d(key, vertices, top_vertices=None):
                    if key not in self.drawn_walls_3d:
                        wall = Poly3DCollection([vertices], facecolors=highlight_color, edgecolors=edge_color,
                          linewidths=1.5,
                          alpha=0.0)
                        self.axes_3d.add_collection3d(wall)
                        red_stripe = None
                        if top_vertices:
                            red_stripe = Poly3DCollection([top_vertices], facecolors=highlight_color, edgecolors=red_stripe_color,
                              linewidths=1.0,
                              alpha=0.0)
                            self.axes_3d.add_collection3d(red_stripe)
                        self.drawn_walls_3d[key] = {'wall':wall,  'stripe':red_stripe}
                        for step, alpha in enumerate([0.3, 0.6, 0.9, 1.0]):
                            QTimer.singleShot(step * 40, lambda w=wall, s=red_stripe, a=alpha: (
                             w.set_alpha(a),
                             s.set_alpha(a) if s else None,
                             self.draw_idle()))

                        QTimer.singleShot(200, lambda w=wall, s=red_stripe: (
                         w.set_facecolor(wall_color), w.set_alpha(0.95),
                         s.set_facecolor(red_stripe_color) if s else None,
                         s.set_alpha(0.95) if s else None,
                         self.draw_idle()))
                    else:
                        self.drawn_walls_3d[key]["wall"].set_verts([vertices])
                        if top_vertices:
                            if self.drawn_walls_3d[key]["stripe"]:
                                self.drawn_walls_3d[key]["stripe"].set_verts([top_vertices])

                def _remove_wall_3d(key):
                    if key in self.drawn_walls_3d:
                        try:
                            wall_obj = self.drawn_walls_3d[key]
                            if isinstance(wall_obj, dict):
                                if wall_obj["wall"]:
                                    wall_obj["wall"].remove()
                                if wall_obj.get("stripe"):
                                    wall_obj["stripe"].remove()
                            else:
                                wall_obj.remove()
                        except Exception:
                            pass
                        else:
                            del self.drawn_walls_3d[key]

                if wall_direction & 1:
                    vertices = [
                     [
                      x + 1, y, 0],
                     [
                      x + 1, y + 1, 0],
                     [
                      x + 1, y + 1, wall_thickness - stripe_thickness],
                     [
                      x + 1, y, wall_thickness - stripe_thickness]]
                    top_vertices = [
                     [
                      x + 1, y, wall_thickness - stripe_thickness],
                     [
                      x + 1, y + 1, wall_thickness - stripe_thickness],
                     [
                      x + 1, y + 1, wall_thickness],
                     [
                      x + 1, y, wall_thickness]]
                    _animate_wall_3d((x, y, "right"), vertices, top_vertices)
                else:
                    _remove_wall_3d((x, y, "right"))
                if wall_direction & 2:
                    vertices = [
                     [
                      x, y + 1, 0],
                     [
                      x + 1, y + 1, 0],
                     [
                      x + 1, y + 1, wall_thickness - stripe_thickness],
                     [
                      x, y + 1, wall_thickness - stripe_thickness]]
                    top_vertices = [
                     [
                      x, y + 1, wall_thickness - stripe_thickness],
                     [
                      x + 1, y + 1, wall_thickness - stripe_thickness],
                     [
                      x + 1, y + 1, wall_thickness],
                     [
                      x, y + 1, wall_thickness]]
                    _animate_wall_3d((x, y, "top"), vertices, top_vertices)
                else:
                    _remove_wall_3d((x, y, "top"))
                if wall_direction & 4:
                    vertices = [
                     [
                      x, y, 0],
                     [
                      x, y + 1, 0],
                     [
                      x, y + 1, wall_thickness - stripe_thickness],
                     [
                      x, y, wall_thickness - stripe_thickness]]
                    top_vertices = [
                     [
                      x, y, wall_thickness - stripe_thickness],
                     [
                      x, y + 1, wall_thickness - stripe_thickness],
                     [
                      x, y + 1, wall_thickness],
                     [
                      x, y, wall_thickness]]
                    _animate_wall_3d((x, y, "left"), vertices, top_vertices)
                else:
                    _remove_wall_3d((x, y, "left"))
                if wall_direction & 8:
                    vertices = [
                     [
                      x, y, 0],
                     [
                      x + 1, y, 0],
                     [
                      x + 1, y, wall_thickness - stripe_thickness],
                     [
                      x, y, wall_thickness - stripe_thickness]]
                    top_vertices = [
                     [
                      x, y, wall_thickness - stripe_thickness],
                     [
                      x + 1, y, wall_thickness - stripe_thickness],
                     [
                      x + 1, y, wall_thickness],
                     [
                      x, y, wall_thickness]]
                    _animate_wall_3d((x, y, "bottom"), vertices, top_vertices)
                else:
                    _remove_wall_3d((x, y, "bottom"))
                self.draw()

            def update_plot_3d(self, x, y, orientation, path_x, path_y):
                """更新3D模式下的显示"""
                self.mouse_pos_3d.set_data_3d([x], [y], [0.01])
                points = list(zip(path_x, path_y))
                self.path_points = points[-self.path_max_len:]
                if len(self.path_points) >= 2:
                    segments = []
                    for i in range(len(self.path_points) - 1):
                        x1, y1 = self.path_points[i]
                        x2, y2 = self.path_points[i + 1]
                        segments.append([(x1, y1, 0.01), (x2, y2, 0.01)])

                    n = len(segments)
                    base_rgba = mcolors.to_rgba("#3b82f6")
                    fade_power = getattr(self, "path_fade_power", 0.85)
                    alphas = [0.15 + 0.85 * ((i + 1) / n) ** fade_power for i in range(n)]
                    colors = [(base_rgba[0], base_rgba[1], base_rgba[2], a) for a in alphas]
                    self.path_collection_3d.set_segments(segments)
                    self.path_collection_3d.set_color(colors)
                else:
                    self.path_collection_3d.set_segments([])
                if self.arrow_3d:
                    self.arrow_3d.remove()
                    self.arrow_3d = None
                if self.arrow_head_3d:
                    self.arrow_head_3d.remove()
                    self.arrow_head_3d = None
                dx, dy = (0, 0)
                if orientation == 0:
                    dx, dy = (0, 0.4)
                elif orientation == 1:
                    dx, dy = (0.4, 0)
                elif orientation == 2:
                    dx, dy = (0, -0.4)
                elif orientation == 3:
                    dx, dy = (-0.4, 0)
                self.arrow_3d = self.axes_3d.plot([x, x + dx], [y, y + dy], [0.01, 0.01], color="#10b981",
                  linewidth=3.0,
                  alpha=0.95)[0]
                if orientation == 0:
                    head_x, head_y = x, y + dy
                elif orientation == 1:
                    head_x, head_y = x + dx, y
                elif orientation == 2:
                    head_x, head_y = x, y + dy
                else:
                    head_x, head_y = x + dx, y
                self.arrow_head_3d = self.axes_3d.scatter([head_x], [head_y], [0.01], c="#10b981", s=100, alpha=0.95)
                self.draw()


class MicroMouseApp(QMainWindow):

            def __init__(self, as_page=False):
                super().__init__()
                self.as_page = as_page
                self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
                self.setGeometry(100, 100, 800, 600)
                self.serial = QSerialPort()
                self.rx_buffer = ""
                self.serial.readyRead.connect(self.read_serial_data)
                self.mouse_current_x = 7.5
                self.mouse_current_y = 0.5
                self.mouse_orientation = 0
                self.gyro_angle = 0.0
                self.run_mode = "停止"
                self.mouse_path_x = [self.mouse_current_x]
                self.mouse_path_y = [self.mouse_current_y]
                self.replay_runs = []
                self.goal_min_x = 3
                self.goal_max_x = 4
                self.goal_min_y = 3
                self.goal_max_y = 4
                self.optimized_paths = []
                self.current_run_path = []
                self.has_reached_goal = False
                self.best_path_info = None
                self.max_replay_saved = 60
                self.wall_map = {}
                self.auto_send_best_path = False
                self.default_view_mode = "2D"
                self.settings = QSettings("MicromouseLab", "MicromouseApp")
                self.theme_pref = self.settings.value("general/theme", "light")
                self.pref_show_sidebar = self.settings.value("general/showSidebarOnStart", True, type=bool)
                self.setFont(QFont("Microsoft YaHei", 10))
                rcParams["font.sans-serif"] = [
                 "Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
                rcParams["axes.unicode_minus"] = False
                self.apply_theme()
                self.central_widget = QWidget()
                if not self.as_page:
                    self.setCentralWidget(self.central_widget)
                self.layout = QVBoxLayout(self.central_widget)
                self.top_status_widget = self._build_top_status_bar()
                self.layout.addWidget(self.top_status_widget)
                self._set_connection_state(False)
                self._set_run_mode("空闲", busy=False)
                self._set_data_state("无连接", "#cbd5e1", "数据状态")
                if not self.as_page:
                    self.init_menu_bar()
                    self.status_bar = QStatusBar()
                    self.setStatusBar(self.status_bar)
                self.init_ui()
                if not self.as_page:
                    self.status_bar.showMessage("就绪")
                self.apply_settings_to_ui()
                self.log_subscribers = []
                self.error_frame_count = 0
                self.bytes_received_window = deque(maxlen=200)
                self.bytes_sent_window = deque(maxlen=200)
                self.last_data_time = None
                self.frame_count = 0
                self._throughput_timer = QTimer(self)
                self._throughput_timer.setInterval(500)
                self._throughput_timer.timeout.connect(self._purge_old_bytes)
                self._throughput_timer.start()
                self._data_status_timer = QTimer(self)
                self._data_status_timer.setInterval(1000)
                self._data_status_timer.timeout.connect(self._update_data_status)
                self._data_status_timer.start()
                self._port_refresh_timer = QTimer(self)
                self._port_refresh_timer.setInterval(2000)
                self._port_refresh_timer.timeout.connect(self.populate_ports)
                self._port_refresh_timer.start()

            def _icon(self, key: str):
                """统一图标出口：优先 FluentIcon，其次 Qt 标准图标"""
                mapping = {'refresh':getattr(FIF, "SYNC", None) if QFW_AVAILABLE else (QStyle.SP_BrowserReload), 
                 'connect':getattr(FIF, "CONNECT", None) if QFW_AVAILABLE else (QStyle.SP_DialogApplyButton), 
                 'disconnect':getattr(FIF, "DISCONNECT", None) if QFW_AVAILABLE else (QStyle.SP_DialogCancelButton), 
                 'sidebar':getattr(FIF, "NAVIGATION", None) if QFW_AVAILABLE else (QStyle.SP_ArrowLeft), 
                 'help':getattr(FIF, "HELP", None) if QFW_AVAILABLE else (QStyle.SP_DialogHelpButton), 
                 'about':getattr(FIF, "INFO", None) if QFW_AVAILABLE else (QStyle.SP_MessageBoxInformation), 
                 'send':getattr(FIF, "SEND", None) if QFW_AVAILABLE else (QStyle.SP_DialogYesButton), 
                 'start':getattr(FIF, "PLAY", None) if QFW_AVAILABLE else (QStyle.SP_MediaPlay), 
                 'stop':getattr(FIF, "STOP", None) if QFW_AVAILABLE else (QStyle.SP_MediaStop), 
                 'reset':getattr(FIF, "SYNC", None) if QFW_AVAILABLE else (QStyle.SP_BrowserReload), 
                 'rescue_left':getattr(FIF, "ARROW_LEFT", None) if QFW_AVAILABLE else (QStyle.SP_ArrowLeft), 
                 'rescue_right':getattr(FIF, "ARROW_RIGHT", None) if QFW_AVAILABLE else (QStyle.SP_ArrowRight), 
                 'send_path':getattr(FIF, "SEND", None) if QFW_AVAILABLE else (QStyle.SP_ArrowRight)}
                icon_obj = mapping.get(key)
                if icon_obj is None:
                    return QIcon()
                try:
                    if QFW_AVAILABLE:
                        if hasattr(icon_obj, "icon"):
                            return icon_obj.icon()
                except Exception:
                    pass
                else:
                    if isinstance(icon_obj, QStyle.StandardPixmap):
                        return self.style().standardIcon(icon_obj)
                    else:
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
                    chip.setStyleSheet("QWidget { background:#ffffff; border:1px solid #e5e7eb; border-radius:10px; }")
                    dot = QLabel()
                    dot.setFixedSize(10, 10)
                    dot.setStyleSheet(f"background:{color}; border-radius:5px; border:1px solid #e5e7eb;")
                    label = QLabel(text)
                    sub = QLabel(title)
                    sub.setStyleSheet("color:#6b7280; font-size:11px;")
                    h.addWidget(dot)
                    h.addWidget(label)
                    h.addWidget(sub)
                    return (
                     chip, dot, label, sub)

                (self.conn_chip, self.conn_dot, self.conn_label, self.conn_sub) = make_chip("连接状态", "#94a3b8", "未连接")
                layout.addWidget(self.conn_chip)
                (self.mode_chip, self.mode_dot, self.mode_label, self.mode_sub) = make_chip("运行模式", "#cbd5e1", "空闲")
                layout.addWidget(self.mode_chip)
                (self.data_chip, self.data_dot, self.data_label, self.data_sub) = make_chip("数据状态", "#cbd5e1", "无数据")
                layout.addWidget(self.data_chip)
                layout.addStretch(1)
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

            def _set_chip_state(self, dot, label, sub, color, text, subtitle):
                dot.setStyleSheet(f"background:{color}; border-radius:5px; border:1px solid #e5e7eb;")
                label.setText(text)
                sub.setText(subtitle)

            def _set_connection_state(self, connected: bool, port: str='', baud: str=''):
                color = "#22c55e" if connected else "#94a3b8"
                text = f"{port} 已连接" if connected and port else "未连接"
                subtitle = f"@{baud}" if connected and baud else "串口状态"
                self._set_chip_state(self.conn_dot, self.conn_label, self.conn_sub, color, text, subtitle)

            def _set_run_mode(self, mode_text: str, busy: bool=False):
                color = "#6366f1" if busy else "#cbd5e1"
                self._set_chip_state(self.mode_dot, self.mode_label, self.mode_sub, color, mode_text, "运行模式")

            def _set_data_state(self, text: str, color: str='#cbd5e1', subtitle: str='数据状态'):
                """更新数据状态显示"""
                self._set_chip_state(self.data_dot, self.data_label, self.data_sub, color, text, subtitle)

            def _update_data_status(self):
                """更新数据状态显示"""
                if not self.serial.isOpen():
                    self._set_data_state("无连接", "#cbd5e1", "数据状态")
                    return
                current_time = time.time()
                if self.last_data_time is None:
                    self._set_data_state("等待数据", "#f59e0b", "数据状态")
                    return
                time_since_last = current_time - self.last_data_time
                if time_since_last < 2.0:
                    if self.error_frame_count == 0:
                        status_text = f"{self.frame_count}帧"
                        color = "#22c55e"
                        subtitle = "数据正常"
                    else:
                        status_text = f"{self.frame_count}帧"
                        color = "#f59e0b"
                        subtitle = f"错误{self.error_frame_count}"
                elif time_since_last < 5.0:
                    status_text = f"{int(time_since_last)}秒前"
                    color = "#f59e0b"
                    subtitle = "数据延迟"
                else:
                    status_text = f"{int(time_since_last)}秒前"
                    color = "#ef4444"
                    subtitle = "数据中断"
                self._set_data_state(status_text, color, subtitle)

            def show_long_task(self, text: str='正在处理...'):
                self.long_task_label.setText(text)
                self.long_task_progress.setRange(0, 0)
                self.long_task_wrap.show()

            def finish_long_task(self, text: str='完成', delay_ms: int=700):
                self.long_task_label.setText(text)
                self.long_task_progress.setRange(0, 1)
                self.long_task_progress.setValue(1)
                QTimer.singleShot(delay_ms, self.long_task_wrap.hide)

            def show_toast(self, title: str, content: str, duration: int = 3000):
                pass

            def init_menu_bar(self):
                menu_bar = self.menuBar()
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
                self.act_refresh.triggered.connect(self.populate_ports)
                self.act_connect.triggered.connect(self.connect_serial)
                self.act_disconnect.triggered.connect(self.disconnect_serial)
                self.act_help.triggered.connect(self.show_help)
                self.act_about.triggered.connect(self.show_about_dialog)
                self.act_toggle_sidebar.toggled.connect(self.toggle_sidebar)

            def init_ui(self):
                serial_group = QGroupBox("串口配置")
                serial_config_layout = QGridLayout()
                serial_config_layout.setContentsMargins(16, 20, 16, 16)
                serial_config_layout.setHorizontalSpacing(16)
                serial_config_layout.setVerticalSpacing(12)
                self.port_label = QLabel("串口:")
                serial_config_layout.addWidget(self.port_label, 0, 0)
                self.port_selector = QfwComboBox(self) if QFW_AVAILABLE else QComboBox()
                self.populate_ports()
                self.port_selector.setMinimumWidth(140)
                serial_config_layout.addWidget(self.port_selector, 0, 1)
                self.baud_label = QLabel("波特率:")
                serial_config_layout.addWidget(self.baud_label, 0, 2)
                common_baud_rates = [
                 "9600", "19200", "38400", "57600",
                 "115200", "230400", "460800", "921600"]
                self.baud_rate_selector = QfwComboBox(self) if QFW_AVAILABLE else QComboBox()
                self.baud_rate_selector.addItems(common_baud_rates)
                self.baud_rate_selector.setCurrentText("115200")
                self.baud_rate_selector.setFixedWidth(120)
                serial_config_layout.addWidget(self.baud_rate_selector, 0, 3)
                self.data_bits_label = QLabel("数据位:")
                serial_config_layout.addWidget(self.data_bits_label, 0, 4)
                self.data_bits_selector = QfwComboBox(self) if QFW_AVAILABLE else QComboBox()
                self.data_bits_selector.addItems(["5", "6", "7", "8"])
                self.data_bits_selector.setCurrentText("8")
                self.data_bits_selector.setFixedWidth(80)
                serial_config_layout.addWidget(self.data_bits_selector, 0, 5)
                self.stop_bits_label = QLabel("停止位:")
                serial_config_layout.addWidget(self.stop_bits_label, 0, 6)
                self.stop_bits_selector = QfwComboBox(self) if QFW_AVAILABLE else QComboBox()
                self.stop_bits_selector.addItems(["1", "1.5", "2"])
                self.stop_bits_selector.setCurrentText("1")
                self.stop_bits_selector.setFixedWidth(80)
                serial_config_layout.addWidget(self.stop_bits_selector, 0, 7)
                self.parity_label = QLabel("校验位:")
                serial_config_layout.addWidget(self.parity_label, 1, 0)
                self.parity_selector = QfwComboBox(self) if QFW_AVAILABLE else QComboBox()
                self.parity_selector.addItems(["无","奇","偶","Mark","Space"])
                self.parity_selector.setCurrentText("无")
                self.parity_selector.setFixedWidth(100)
                serial_config_layout.addWidget(self.parity_selector, 1, 1)
                if QFW_AVAILABLE:
                    self.connect_button = QfwPrimaryPushButton("连接", self)
                else:
                    self.connect_button = QPushButton("连接")
                self.connect_button.setIcon(self._icon("connect"))
                serial_config_layout.addWidget(self.connect_button, 1, 6)
                self.disconnect_button = QfwPushButton("断开", self) if QFW_AVAILABLE else QPushButton("断开")
                self.disconnect_button.setIcon(self._icon("disconnect"))
                self.disconnect_button.setEnabled(False)
                self._mark_secondary(self.disconnect_button)
                serial_config_layout.addWidget(self.disconnect_button, 1, 7)
                self.connect_button.clicked.connect(self.connect_serial)
                self.disconnect_button.clicked.connect(self.disconnect_serial)
                serial_config_layout.setColumnStretch(1, 1)
                serial_config_layout.setColumnStretch(3, 1)
                serial_config_layout.setColumnStretch(5, 1)
                serial_config_layout.setColumnStretch(7, 0)
                serial_group.setLayout(serial_config_layout)
                send_group = QGroupBox("发送数据")
                send_layout = QHBoxLayout()
                send_layout.setContentsMargins(16, 20, 16, 16)
                send_layout.setSpacing(12)
                self.send_data_input = QfwLineEdit(self) if QFW_AVAILABLE else QLineEdit()
                self.send_data_input.setPlaceholderText("输入要发送的数据")
                send_layout.addWidget(self.send_data_input)
                self.send_button = QfwPrimaryPushButton("发送", self) if QFW_AVAILABLE else QPushButton("发送")
                self.send_button.setIcon(self._icon("send"))
                self.send_button.setEnabled(False)
                send_layout.addWidget(self.send_button)
                self.protocol_hint = QLabel("协议帧: s,X,Y,O,Angle,Front,Left,Right,Mode\\r\\n\nX/Y:0-7, O:0北1东2南3西, Angle:角度(度), 传感器:0有墙/1没墙\nMode:0停止/1迷宫模式")
                self.protocol_hint.setWordWrap(True)
                send_layout.addWidget(self.protocol_hint)
                send_group.setLayout(send_layout)
                self.send_button.clicked.connect(self.send_serial_data)
                self.maze_plotter = MazePlotter(self)
                plot_wrap = QGroupBox("迷宫与轨迹")
                pv = QVBoxLayout()
                pv.setContentsMargins(20, 24, 20, 20)
                pv.setSpacing(0)
                top_layout = QHBoxLayout()
                top_layout.setContentsMargins(0, 0, 0, 0)
                top_layout.setSpacing(8)
                top_layout.addStretch(1)
                self.view_toggle_button = QfwPushButton("3D视图", self) if QFW_AVAILABLE else QPushButton("3D视图", self)
                self.view_toggle_button.setFixedSize(80, 32)
                self.view_toggle_button.setStyleSheet("\n            QPushButton {\n                background-color: #f1f5f9;\n                color: #0f172a;\n                border: 1px solid #e2e8f0;\n                border-radius: 6px;\n                font-size: 12px;\n                font-weight: 500;\n                padding: 4px 8px;\n            }\n            QPushButton:hover {\n                background-color: #e2e8f0;\n                border-color: #cbd5e1;\n            }\n            QPushButton:pressed {\n                background-color: #cbd5e1;\n            }\n        ")
                self.view_toggle_button.clicked.connect(self.toggle_maze_view)
                top_layout.addWidget((self.view_toggle_button), alignment=(Qt.AlignTop | Qt.AlignRight))
                self.compass_widget = CompassWidget(self)
                top_layout.addWidget((self.compass_widget), alignment=(Qt.AlignTop | Qt.AlignRight))
                top_layout.setAlignment(self.compass_widget, Qt.AlignTop | Qt.AlignRight)
                pv.addLayout(top_layout)
                pv.addWidget(self.maze_plotter, 1)
                plot_wrap.setLayout(pv)
                left_panel = QWidget()
                left_v = QVBoxLayout(left_panel)
                left_v.setContentsMargins(16, 12, 16, 16)
                left_v.setSpacing(16)
                left_v.addWidget(serial_group)
                left_v.addWidget(send_group)
                control_group = QGroupBox("控制面板")
                control_layout = QVBoxLayout()
                control_layout.setContentsMargins(16, 20, 16, 16)
                control_layout.setSpacing(10)
                self.start_button = QfwPrimaryPushButton("开始", self) if QFW_AVAILABLE else QPushButton("开始")
                self.start_button.setIcon(self._icon("start"))
                control_layout.addWidget(self.start_button)
                self.stop_button = QfwPushButton("停止", self) if QFW_AVAILABLE else QPushButton("停止")
                self.stop_button.setIcon(self._icon("stop"))
                self._mark_secondary(self.stop_button)
                control_layout.addWidget(self.stop_button)
                self.reset_button = QfwPushButton("复位", self) if QFW_AVAILABLE else QPushButton("复位")
                self.reset_button.setIcon(self._icon("reset"))
                self._mark_secondary(self.reset_button)
                control_layout.addWidget(self.reset_button)
                rescue_layout = QHBoxLayout()
                rescue_layout.setSpacing(8)
                self.rescue_left_button = QfwPushButton("左救援", self) if QFW_AVAILABLE else QPushButton("左救援")
                self.rescue_left_button.setIcon(self._icon("rescue_left"))
                self._mark_secondary(self.rescue_left_button)
                rescue_layout.addWidget(self.rescue_left_button)
                self.rescue_right_button = QfwPushButton("右救援", self) if QFW_AVAILABLE else QPushButton("右救援")
                self.rescue_right_button.setIcon(self._icon("rescue_right"))
                self._mark_secondary(self.rescue_right_button)
                rescue_layout.addWidget(self.rescue_right_button)
                control_layout.addLayout(rescue_layout)
                self.send_path_button = QfwPrimaryPushButton("发送优化路径", self) if QFW_AVAILABLE else QPushButton("发送优化路径")
                self.send_path_button.setIcon(self._icon("send_path"))
                control_layout.addWidget(self.send_path_button)
                control_group.setLayout(control_layout)
                left_v.addWidget(control_group)
                self.start_button.clicked.connect(self.start_mouse)
                self.stop_button.clicked.connect(self.stop_mouse)
                self.reset_button.clicked.connect(self.reset_mouse)
                self.rescue_left_button.clicked.connect(self.rescue_left)
                self.rescue_right_button.clicked.connect(self.rescue_right)
                self.send_path_button.clicked.connect(self.send_optimized_path)
                sensor_group = QGroupBox("传感器数据")
                sensor_layout = QVBoxLayout()
                sensor_layout.setContentsMargins(16, 20, 16, 16)
                sensor_layout.setSpacing(10)
                self.sensor_labels = {}
                sensor_names = [
                 "左传感器:", "右传感器:", "前传感器:", "电池电压:"]
                for name in sensor_names:
                    h_layout = QHBoxLayout()
                    label = QLabel(name)
                    value_label = QLabel("N/A")
                    value_label.setObjectName("sensor_value_label")
                    self.sensor_labels[name] = value_label
                    h_layout.addWidget(label)
                    h_layout.addStretch(1)
                    h_layout.addWidget(value_label)
                    sensor_layout.addLayout(h_layout)

                sensor_group.setLayout(sensor_layout)
                left_v.addWidget(sensor_group)
                left_v.addStretch(1)
                self.left_panel = left_panel
                h_splitter = QSplitter(Qt.Horizontal)
                h_splitter.addWidget(left_panel)
                h_splitter.addWidget(plot_wrap)
                h_splitter.setStretchFactor(0, 1)
                h_splitter.setStretchFactor(1, 10)
                h_splitter.setSizes([240, 1200])
                self.h_splitter = h_splitter
                self.layout.addWidget(h_splitter)

            def toggle_maze_view(self):
                """切换迷宫2D/3D视图"""
                if hasattr(self, "maze_plotter"):
                    self.maze_plotter.toggle_view_mode()
                    if self.maze_plotter.view_mode == "3D":
                        self.view_toggle_button.setText("2D视图")
                        if hasattr(self, "status_bar"):
                            self.status_bar.showMessage("已切换到3D视图", 2000)
                    else:
                        self.view_toggle_button.setText("3D视图")
                        if hasattr(self, "status_bar"):
                            self.status_bar.showMessage("已切换到2D视图", 2000)
                    if hasattr(self, "mouse_current_x"):
                        if hasattr(self, "mouse_current_y"):
                            if hasattr(self, "mouse_path_x"):
                                if hasattr(self, "mouse_path_y"):
                                    self.maze_plotter.update_plot(self.mouse_current_x, self.mouse_current_y, getattr(self, "mouse_orientation", 0), self.mouse_path_x, self.mouse_path_y)

            def toggle_sidebar(self, checked: bool):
                if checked:
                    self.left_panel.setVisible(False)
                    self.h_splitter.setSizes([0, max(1, self.h_splitter.width() - 0)])
                    if hasattr(self, "status_bar"):
                        self.status_bar.showMessage("已隐藏侧栏", 2000)
                else:
                    self.left_panel.setVisible(True)
                    self.h_splitter.setSizes([240, max(1, self.h_splitter.width() - 240)])
                    if hasattr(self, "status_bar"):
                        self.status_bar.showMessage("已显示侧栏", 2000)

            def apply_settings_to_ui(self):
                """从 QSettings 读取默认值并应用到界面控件。"""
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
                else:
                    if hasattr(self, "maze_plotter"):
                        self.maze_plotter.set_tail_style(tail_len, tail_fade)
                    if data_bits in ('5', '6', '7', '8'):
                        self.data_bits_selector.setCurrentText(data_bits)
                    if stop_bits in ('1', '1.5', '2'):
                        self.stop_bits_selector.setCurrentText(stop_bits)
                    if parity in ('无', '奇', '偶', 'Mark', 'Space'):
                        self.parity_selector.setCurrentText(parity)
                    if hasattr(self, "left_panel") and not self.as_page:
                        show_sidebar = self.settings.value("general/showSidebarOnStart", True, type=bool)
                        self.left_panel.setVisible(show_sidebar)
                        if show_sidebar:
                            self.h_splitter.setSizes([240, max(1, self.h_splitter.width() - 240)])
                    else:
                        self.h_splitter.setSizes([0, max(1, self.h_splitter.width() - 0)])

            def reload_settings(self):
                """从 QSettings 重新加载设置（主题/串口/侧栏）。"""
                self.theme_pref = self.settings.value("general/theme", "light")
                self.apply_theme()
                self.apply_settings_to_ui()

            def apply_theme(self):
                """现代化美观主题样式/Fluent 主题切换"""
                if QFW_AVAILABLE:
                    try:
                        if str(getattr(self, "theme_pref", "light")).lower() == "dark":
                            setTheme(Theme.DARK)
                        else:
                            setTheme(Theme.LIGHT)
                        setThemeColor("#3b82f6")
                    except Exception:
                        pass

                style_sheet = '\n        /* 扁平化主流桌面风格：低饱和、中性、无渐变 */\n\n        QMainWindow { background-color: #f6f7fb; }\n\n        QWidget { \n            background-color: transparent; \n            color: #1f2937; \n            font-family: "Microsoft YaHei UI", "Segoe UI", "SF Pro Display", sans-serif; \n            font-size: 13px;\n        }\n\n        /* 卡片 */\n        QGroupBox { \n            background-color: #ffffff;\n            border: 1px solid #e5e7eb; \n            border-radius: 12px; \n            margin-top: 18px; \n            padding-top: 14px;\n            font-weight: 600;\n        }\n        QGroupBox::title { \n            subcontrol-origin: margin; \n            subcontrol-position: top left; \n            padding: 0 10px; \n            margin-left: 14px; \n            color: #111827; \n            font-size: 13px;\n            font-weight: 600;\n            letter-spacing: 0.2px;\n        }\n\n        /* 按钮：实色扁平 */\n        QPushButton { \n            background: #4f46e5;\n            color: #ffffff; \n            border: none; \n            padding: 10px 18px; \n            border-radius: 8px; \n            font-weight: 500;\n            font-size: 13px;\n            min-height: 20px;\n            letter-spacing: 0.2px;\n        }\n        QPushButton:hover { background: #5b55ec; }\n        QPushButton:pressed { background: #4338ca; padding: 9px 17px; }\n        QPushButton:disabled { background: #e5e7eb; color: #9ca3af; }\n        QPushButton[class="secondary"] {\n            background: #f3f4f6;\n            color: #374151;\n            border: 1px solid #e5e7eb;\n        }\n        QPushButton[class="secondary"]:hover {\n            background: #e5e7eb;\n            border-color: #d1d5db;\n        }\n\n        /* 输入控件 */\n        QLineEdit, QComboBox, QTextEdit { \n            background-color: #ffffff; \n            border: 1.4px solid #e5e7eb; \n            border-radius: 8px; \n            padding: 9px 12px; \n            font-size: 13px;\n            selection-background-color: #e0e7ff;\n            selection-color: #312e81;\n        }\n        QLineEdit:focus, QTextEdit:focus { \n            border: 1.8px solid #6366f1; \n            background-color: #ffffff;\n            outline: none;\n        }\n        QComboBox:focus { border: 1.8px solid #6366f1; }\n        QLineEdit:hover, QComboBox:hover, QTextEdit:hover {\n            border: 1.4px solid #d1d5db;\n            background-color: #fbfbfd;\n        }\n        QComboBox::drop-down { \n            border: none;\n            border-left: 1.2px solid #e5e7eb; \n            border-radius: 0 8px 8px 0;\n            width: 22px;\n            background-color: #f8fafc;\n        }\n        QComboBox::drop-down:hover { background-color: #f1f5f9; }\n        QComboBox::down-arrow { width: 14px; height: 14px; margin: 2px; }\n        QComboBox QAbstractItemView {\n            border: 1px solid #e5e7eb;\n            border-radius: 8px;\n            background-color: #ffffff;\n            selection-background-color: #eef2ff;\n            selection-color: #312e81;\n            padding: 4px;\n        }\n\n        /* 菜单与状态栏 */\n        QMenuBar { \n            background: #ffffff;\n            border-bottom: 1px solid #e5e7eb; \n            padding: 6px 8px;\n            font-size: 13px;\n        }\n        QMenuBar::item { padding: 7px 14px; border-radius: 6px; margin: 2px; }\n        QMenuBar::item:selected { background-color: #f3f4f6; color: #111827; }\n        QMenuBar::item:pressed { background-color: #e5e7eb; }\n        QMenu { \n            border: 1px solid #e5e7eb; \n            background-color: #ffffff; \n            border-radius: 10px;\n            padding: 6px;\n        }\n        QMenu::item { padding: 10px 26px 10px 14px; border-radius: 6px; margin: 2px; }\n        QMenu::item:selected { background-color: #f3f4f6; color: #111827; }\n        QMenu::separator { height: 1px; background: #e5e7eb; margin: 4px 8px; }\n\n        QStatusBar { \n            background: #ffffff;\n            border-top: 1px solid #e5e7eb; \n            color: #6b7280; \n            padding: 6px 12px;\n            font-size: 12px;\n        }\n\n        /* 分割器 */\n        QSplitter::handle { \n            background-color: #e5e7eb;\n            border-radius: 2px;\n            width: 3px;\n            height: 3px;\n        }\n        QSplitter::handle:hover { background-color: #cbd5e1; }\n        QSplitter::handle:horizontal { width: 3px; }\n        QSplitter::handle:vertical { height: 3px; }\n\n        /* 标签 */\n        QLabel { font-size: 13px; color: #1f2937; }\n        QLabel#sensor_value_label { \n            font-weight: 600; \n            color: #4338ca; \n            font-size: 14px;\n            padding: 6px 12px;\n            background: #eef2ff;\n            border-radius: 6px;\n            border: 1px solid #c7d2fe;\n        }\n\n        /* 文本编辑 */\n        QTextEdit {\n            background-color: #fbfbfd;\n            border: 1.4px solid #e5e7eb;\n            border-radius: 8px;\n            font-family: "Consolas", "Monaco", "Courier New", monospace;\n            font-size: 12px;\n            line-height: 1.5;\n            padding: 8px;\n        }\n        QTextEdit:focus { border: 1.8px solid #6366f1; background-color: #ffffff; }\n\n        /* 复选框 */\n        QCheckBox { font-size: 13px; color: #1f2937; spacing: 8px; }\n        QCheckBox::indicator {\n            width: 18px; height: 18px;\n            border: 1.6px solid #cbd5e1;\n            border-radius: 4px;\n            background-color: #ffffff;\n        }\n        QCheckBox::indicator:hover { border-color: #94a3b8; background-color: #f8fafc; }\n        QCheckBox::indicator:checked {\n            background: #4f46e5;\n            border-color: #4f46e5;\n        }\n\n        /* 进度条 */\n        QProgressBar {\n            border: none;\n            border-radius: 6px;\n            background-color: #f3f4f6;\n            text-align: center;\n            height: 8px;\n        }\n        QProgressBar::chunk {\n            background: #4f46e5;\n            border-radius: 6px;\n        }\n\n        /* 滚动条 */\n        QScrollBar:vertical {\n            border: none;\n            background: #f3f4f6;\n            width: 10px;\n            border-radius: 5px;\n        }\n        QScrollBar::handle:vertical {\n            background: #cbd5e1;\n            border-radius: 5px;\n            min-height: 20px;\n        }\n        QScrollBar::handle:vertical:hover { background: #94a3b8; }\n        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }\n\n        QScrollBar:horizontal {\n            border: none;\n            background: #f3f4f6;\n            height: 10px;\n            border-radius: 5px;\n        }\n        QScrollBar::handle:horizontal {\n            background: #cbd5e1;\n            border-radius: 5px;\n            min-width: 20px;\n        }\n        QScrollBar::handle:horizontal:hover { background: #94a3b8; }\n        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }\n\n        /* 对话框 / 提示框 */\n        QDialog, QMessageBox {\n            background: #ffffff;\n            border: 1px solid #e5e7eb;\n            border-radius: 12px;\n        }\n        QMessageBox QLabel {\n            color: #1f2937;\n            font-size: 13px;\n        }\n        QMessageBox QPushButton {\n            background: #4f46e5;\n            color: #ffffff;\n            border: none;\n            padding: 8px 14px;\n            border-radius: 8px;\n            font-weight: 500;\n            min-width: 64px;\n        }\n        QMessageBox QPushButton:hover { background: #5b55ec; }\n        QMessageBox QPushButton:pressed { background: #4338ca; }\n\n        /* 说明和关于页面卡片样式 */\n        QWidget#titleCard {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n            border-radius: 16px;\n            border: none;\n        }\n        QLabel#pageTitle {\n            font-size: 28px;\n            font-weight: 700;\n            color: #000000;\n            background: transparent;\n        }\n        QLabel#pageSubtitle {\n            font-size: 14px;\n            color: #000000;\n            background: transparent;\n        }\n\n        QWidget#appInfoCard {\n            background-color: #ffffff;\n            border: 1px solid #e5e7eb;\n            border-radius: 16px;\n        }\n        QLabel#appNameLabel {\n            font-size: 32px;\n            font-weight: 700;\n            color: #111827;\n            background: transparent;\n        }\n        QLabel#versionLabel {\n            font-size: 16px;\n            font-weight: 500;\n            color: #6b7280;\n            background: transparent;\n        }\n        QLabel#appDescLabel {\n            font-size: 14px;\n            color: #4b5563;\n            background: transparent;\n        }\n\n        QWidget#sectionCard {\n            background-color: #ffffff;\n            border: 1px solid #e5e7eb;\n            border-radius: 12px;\n            padding: 4px;\n        }\n        QLabel#sectionTitle {\n            font-size: 18px;\n            font-weight: 600;\n            color: #111827;\n            background: transparent;\n            padding-bottom: 4px;\n        }\n        QLabel#sectionContent {\n            font-size: 13px;\n            color: #000000;\n            background: transparent;\n            line-height: 1.6;\n        }\n        /* 设置页卡片 */\n        QWidget#settingsCard {\n            background: #ffffff;\n            border: 1px solid #e5e7eb;\n            border-radius: 12px;\n        }\n        QLabel#settingsTitle {\n            font-size: 16px;\n            font-weight: 600;\n            color: #0f172a;\n        }\n        QLabel#infoKeyLabel {\n            font-size: 13px;\n            font-weight: 500;\n            color: #6b7280;\n            background: transparent;\n        }\n        QLabel#infoValueLabel {\n            font-size: 13px;\n            color: #111827;\n            background: transparent;\n        }\n        '
                self.setStyleSheet(style_sheet)
                try:
                    app = QApplication.instance()
                    if app is not None:
                        app.setStyleSheet(style_sheet)
                except Exception:
                    pass

            def show_help(self):
                text = f"使用说明（统一协议）\n\n1) 基本操作：在‘串口配置’中选择串口参数并连接；在‘发送数据’中输入文本点击发送。\n2) 控制台：显示所有收发数据（可用于调试）。\n\n3) 串口数据协议：\n   - 帧格式：s,X,Y,O,Angle,Front,Left,Right,Mode\\r\\n\n   - X: 列(0-7)、Y: 行(0-7)、O: 朝向(0=北,1=东,2=南,3=西)\n   - Angle: 陀螺仪角度（度，0度=北，顺时针增加）\n   - Front/Left/Right: 前/左/右传感器值（0=有墙，1=没墙）\n   - Mode: 运行模式（0=停止，1=迷宫模式）\n   - 示例：s,3,4,1,45.5,0,1,1,1\\r\\n  (位置3,4，朝东，角度45.5°，前方有墙，左右无墙，迷宫模式)\n\n   - 墙体自动判断：\n     · 系统根据位置、朝向和传感器数据自动判断并绘制墙体\n     · 传感器值0表示有墙，1表示没墙\n     · 小车一格一格移动，每格自动更新墙体信息\n\n4) 其它：菜单栏可刷新串口、清空控制台、隐藏侧栏、查看本说明。\n\n开发者：{APP_DEVELOPER}（{APP_SCHOOL}）\n用途：{APP_PROJECT}\n联系方式：{APP_EMAIL}"
                QMessageBox.information(self, "使用说明", text)

            def show_about_dialog(self):
                """显示关于对话框"""
                about_text = f'{APP_NAME}\n\n版本：{APP_VERSION}\n\n开发者：{APP_DEVELOPER}\n学校：{APP_SCHOOL}\n项目：{APP_PROJECT}\n\n联系方式：{APP_EMAIL}\n网址：{APP_URL}\n\n技术栈：\n  • PyQt5 {PYQT_VERSION_STR}\n  • Qt {QT_VERSION_STR}\n  • Python {sys.version.split(" ")[0]}\n  • Matplotlib\n\n{APP_COPYRIGHT} {APP_DEVELOPER}\n本软件为电子系统设计课程项目，仅供学习交流使用。'
                QMessageBox.about(self, "关于", about_text)

            def populate_ports(self):
                if self.serial.isOpen():
                    return
                current_port = self.port_selector.currentText() if self.port_selector.count() > 0 else ""
                available_ports = [p.portName() for p in QSerialPortInfo.availablePorts()]
                current_list = [self.port_selector.itemText(i) for i in range(self.port_selector.count())]
                if current_list == available_ports:
                    return
                self.port_selector.clear()
                for port_name in available_ports:
                    self.port_selector.addItem(port_name)

                if current_port and current_port in available_ports:
                    self.port_selector.setCurrentText(current_port)
                elif self.port_selector.count() > 0:
                    self.port_selector.setCurrentIndex(0)

            def connect_serial(self):
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
                if data_bits_str == "5":
                    self.serial.setDataBits(QSerialPort.Data5)
                elif data_bits_str == "6":
                    self.serial.setDataBits(QSerialPort.Data6)
                elif data_bits_str == "7":
                    self.serial.setDataBits(QSerialPort.Data7)
                elif data_bits_str == "8":
                    self.serial.setDataBits(QSerialPort.Data8)
                if stop_bits_str == "1":
                    self.serial.setStopBits(QSerialPort.OneStop)
                elif stop_bits_str == "1.5":
                    self.serial.setStopBits(QSerialPort.OneAndHalfStop)
                elif stop_bits_str == "2":
                    self.serial.setStopBits(QSerialPort.TwoStop)
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
                        self.serial.write(data_to_send.encode("utf-8"))
                        self.update_console(data_to_send, True)
                        self._emit_log("TX", data_to_send)
                        self.bytes_sent_window.append((time.time(), len(data_to_send.encode("utf-8"))))
                    else:
                        self.show_toast("发送内容不能为空", "warning")
                else:
                    self.show_toast("请先连接串口", "warning")

            def send_command(self, command):
                if self.serial.isOpen():
                    self.serial.write(command.encode("utf-8"))
                    self.update_console(f"Command sent: {command}", True)
                    self._emit_log("TX", command)
                    self.bytes_sent_window.append((time.time(), len(command.encode("utf-8"))))
                else:
                    self.show_toast("请先连接串口", "warning")

            def start_mouse(self):
                self.send_command("start")
                self._set_run_mode("运行中", busy=True)
                self.show_toast("已发送启动命令", "success", 1500)

            def stop_mouse(self):
                self.send_command("stop")
                self._set_run_mode("空闲", busy=False)
                self.current_run_path = []
                self.has_reached_goal = False
                self.show_toast("已发送停止命令", "info", 1500)

            def reset_mouse(self):
                self.send_command("reset")
                self._set_run_mode("空闲", busy=False)
                self.current_run_path = []
                self.has_reached_goal = False
                self.best_path_info = None
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
                print(f"[{timestamp}] {prefix} {data}")

            def _calculate_walls_from_sensors(self, x, y, orientation, front_val, left_val, right_val):
                """
        根据当前位置、朝向和传感器值计算墙体位掩码
        传感器值：0=有墙，1=没墙
        朝向：0=北，1=东，2=南，3=西
        墙体方向（位掩码）：1=右(+X), 2=上(+Y), 4=左(-X), 8=下(-Y)
        """
                wall_mask = 0
                if orientation == 0:
                    if front_val == 0:
                        wall_mask |= 2
                    if left_val == 0:
                        wall_mask |= 4
                    if right_val == 0:
                        wall_mask |= 1
                elif orientation == 1:
                    if front_val == 0:
                        wall_mask |= 1
                    if left_val == 0:
                        wall_mask |= 2
                    if right_val == 0:
                        wall_mask |= 8
                elif orientation == 2:
                    if front_val == 0:
                        wall_mask |= 8
                    if left_val == 0:
                        wall_mask |= 1
                    if right_val == 0:
                        wall_mask |= 4
                elif orientation == 3:
                    if front_val == 0:
                        wall_mask |= 4
                    if left_val == 0:
                        wall_mask |= 8
                    if right_val == 0:
                        wall_mask |= 2
                return wall_mask

            def snapshot_current_run(self, name: str=None):
                """将当前轨迹保存为可回放的记录"""
                if not (self.mouse_path_x and self.mouse_path_y):
                    return
                if name is None or not name.strip():
                    name = f"run_{len(self.replay_runs) + 1}"
                self.replay_runs.append({'name':(name.strip)(), 
                 'path_x':list(self.mouse_path_x), 
                 'path_y':list(self.mouse_path_y)})

            def _snapshot_path_cells(self, path_cells, name: str):
                """将格子路径(整数坐标)保存到回放列表，转换为中心点显示坐标"""
                if not path_cells:
                    return
                path_x = [cx + 0.5 for cx, _ in path_cells]
                path_y = [cy + 0.5 for _, cy in path_cells]
                self._append_or_replace_replay_run(name.strip(), path_x, path_y)

            def _append_or_replace_replay_run(self, name: str, path_x, path_y):
                """在回放列表中按名称替换或追加，并限制长度"""
                for (i, run) in enumerate(self.replay_runs):
                    if run.get("name") == name:
                        self.replay_runs[i] = {'name':name, 
                         'path_x':list(path_x),  'path_y':list(path_y)}
                        break
                else:
                    self.replay_runs.append({'name':name,  'path_x':list(path_x),  'path_y':list(path_y)})

                if len(self.replay_runs) > self.max_replay_saved:
                    overflow = len(self.replay_runs) - self.max_replay_saved
                    self.replay_runs = self.replay_runs[overflow:]

            def _on_reach_goal(self):
                """到达终点时的处理：记录路径并优化"""
                if not self.current_run_path:
                    return
                original_path = list(self.current_run_path)
                optimized_path = self._optimize_path(original_path)
                path_info = {'original_path':original_path, 
                 'optimized_path':optimized_path, 
                 'original_length':len(original_path), 
                 'optimized_length':len(optimized_path), 
                 'timestamp':(time.time)()}
                self.optimized_paths.append(path_info)
                reduction = len(original_path) - len(optimized_path)
                reduction_percent = reduction / len(original_path) * 100 if original_path else 0
                self.show_toast(f"到达终点！路径已优化：{len(original_path)}步 → {len(optimized_path)}步（减少{reduction}步，{reduction_percent:.1f}%）", "success", 3000)
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.snapshot_current_run(f"原始轨迹_{timestamp}")
                self._snapshot_path_cells(optimized_path, f"优化轨迹_{timestamp}")
                if self.best_path_info is None or len(optimized_path) < self.best_path_info["optimized_length"]:
                    self.best_path_info = {'optimized_path':optimized_path,  'optimized_length':len(optimized_path), 
                     'timestamp':timestamp}
                    self._snapshot_path_cells(optimized_path, "最优路径")
                if self.auto_send_best_path:
                    try:
                        self.send_optimized_path()
                    except Exception:
                        pass

            def _optimize_path(self, path):
                pass

            def get_best_optimized_path(self):
                """获取最短的优化路径"""
                if not self.optimized_paths:
                    if self.best_path_info:
                        return self.best_path_info.get("optimized_path")
                    return
                best = min((self.optimized_paths), key=(lambda p: p["optimized_length"]))
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
                path_str = ";".join([f"{x},{y}" for x, y in best_path])
                command = f"path:{path_str}\n"
                self.send_command(command)
                self.show_toast(f"已发送优化路径（{len(best_path)}步）", "success", 2000)

            def _is_at_goal(self, grid_x: int, grid_y: int) -> bool:
                """判断当前位置是否在终点区域内"""
                return self.goal_min_x <= grid_x <= self.goal_max_x and self.goal_min_y <= grid_y <= self.goal_max_y

            def _handle_frame(self, line: str):
                """处理完整帧：s,X,Y,O,Angle,Front,Left,Right,Mode"""
                line = line.strip().replace("\r", "").replace("\n", "")
                if not line:
                    return
                if line[0].lower() == "s":
                    line = line[1:]
                if line.startswith(","):
                    line = line[1:]
                parts = line.split(",")
                parts = [p.strip() for p in parts if p.strip()]
                if len(parts) < 6:
                    raise ValueError(f"帧字段不足 (got {len(parts)} fields, need at least 6): {line}")
                if len(parts) >= 8:
                    x_str, y_str, o_str = parts[0], parts[1], parts[2]
                    angle_str = parts[3]
                    front_val, left_val, right_val = int(parts[4]), int(parts[5]), int(parts[6])
                    mode_str = parts[7] if len(parts) > 7 else "停止"
                else:
                    x_str, y_str, o_str = parts[0], parts[1], parts[2]
                    angle_str = "0"
                    front_val, left_val, right_val = int(parts[3]), int(parts[4]), int(parts[5])
                    mode_str = "停止"
                x = float(x_str) + 0.5
                y = float(y_str) + 0.5
                orientation = int(o_str)
                grid_x = int(float(x_str))
                grid_y = int(float(y_str))
                try:
                    self.gyro_angle = float(angle_str)
                except (ValueError, IndexError):
                    self.gyro_angle = 0.0
                else:
                    mode_text = mode_str.strip() if mode_str else "停止"
                    if mode_text == "0" or mode_text.lower() == "stop":
                        mode_text = "停止"
                    else:
                        if mode_text == "1" or mode_text.lower() == "maze":
                            mode_text = "迷宫模式"
                    self.run_mode = mode_text
                    self.mouse_orientation = orientation
                    if not mode_text == "迷宫模式":
                        if not self.current_run_path or self.current_run_path[-1] != (grid_x, grid_y):
                            self.current_run_path.append((grid_x, grid_y))
                if self._is_at_goal(grid_x, grid_y) and not self.has_reached_goal:
                    self.has_reached_goal = True
                    self._on_reach_goal()
                else:
                    if self.current_run_path:
                        self.current_run_path = []
                        self.has_reached_goal = False
                    if hasattr(self, "compass_widget"):
                        self.compass_widget.update_angle(self.gyro_angle)
                    busy = self.run_mode != "停止"
                    self._set_run_mode((self.run_mode), busy=busy)
                    if self.mouse_path_x and self.mouse_path_y:
                        last_x = self.mouse_path_x[-1]
                        last_y = self.mouse_path_y[-1]
                        dx = x - last_x
                        dy = y - last_y
                        dist = (dx * dx + dy * dy) ** 0.5
                        steps = min(10, max(1, int(dist / 0.4)))
                        for i in range(1, steps + 1):
                            t = i / (steps + 1)
                            self.mouse_path_x.append(last_x + dx * t)
                            self.mouse_path_y.append(last_y + dy * t)

                        self.mouse_path_x.append(x)
                        self.mouse_path_y.append(y)
                        max_len = getattr(self.maze_plotter, "path_max_len", 200)
                        if len(self.mouse_path_x) > max_len:
                            trim = len(self.mouse_path_x) - max_len
                            self.mouse_path_x = self.mouse_path_x[trim:]
                            self.mouse_path_y = self.mouse_path_y[trim:]
                        self.mouse_current_x = self.mouse_path_x[-1]
                        self.mouse_current_y = self.mouse_path_y[-1]
                        self.sensor_labels["前传感器:"].setText(str(front_val))
                        self.sensor_labels["左传感器:"].setText(str(left_val))
                        self.sensor_labels["右传感器:"].setText(str(right_val))
                        cell_x = int(float(x_str))
                        cell_y = int(float(y_str))
                        wall_mask = self._calculate_walls_from_sensors(cell_x, cell_y, orientation, front_val, left_val, right_val)
                        if wall_mask > 0:
                            self.maze_plotter.draw_maze_wall(cell_x, cell_y, wall_mask)
                            existing = self.wall_map.get((cell_x, cell_y), 0)
                            self.wall_map[(cell_x, cell_y)] = existing | wall_mask
                        self.maze_plotter.update_plot(self.mouse_current_x, self.mouse_current_y, self.mouse_orientation, self.mouse_path_x, self.mouse_path_y)

            def read_serial_data(self):
                raw = self.serial.readAll()
                data = raw.data().decode("utf-8", errors="replace")
                self.bytes_received_window.append((time.time(), len(raw)))
                self.update_console(data, False)
                self._emit_log("RX", data)
                self.rx_buffer += data
                while True:
                    s_idx = -1
                    for i in range(len(self.rx_buffer)):
                        if self.rx_buffer[i].lower() == "s":
                            s_idx = i
                            break

                    if s_idx == -1:
                        if len(self.rx_buffer) > 500:
                            self.rx_buffer = ""
                        break
                    remaining = self.rx_buffer[s_idx:]
                    if "\n" not in remaining:
                        self.rx_buffer = remaining
                        break
                    line_end = remaining.index("\n")
                    line = remaining[:line_end].strip()
                    self.rx_buffer = remaining[line_end + 1:]
                    line = line.replace("\r", "")
                    if not line:
                        pass
                    else:
                        try:
                            self._handle_frame(line)
                            self.frame_count += 1
                            self.last_data_time = time.time()
                        except Exception as e:
                            try:
                                print(f"Frame parse error: {e}; line={line[:100]}")
                                self.error_frame_count += 1
                            finally:
                                e = None
                                del e

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
                cutoff = now - 5.0
                while True:
                    if self.bytes_received_window and self.bytes_received_window[0][0] < cutoff:
                        self.bytes_received_window.popleft()
                    else:
                        break

                while True:
                    if self.bytes_sent_window and self.bytes_sent_window[0][0] < cutoff:
                        self.bytes_sent_window.popleft()
                    else:
                        break

            def get_throughput_bps(self):
                rx = sum((n for t, n in self.bytes_received_window))
                tx = sum((n for t, n in self.bytes_sent_window))
                return (
                 int(rx * 8 / 5.0), int(tx * 8 / 5.0))


class SettingsPage(QWidget):

            def __init__(self, parent=None, app_page=None):
                super().__init__(parent)
                self.setObjectName("settingsPage")
                self.app_page = app_page
                self.settings = QSettings("MicromouseLab", "MicromouseApp")
                root = QVBoxLayout(self)
                root.setContentsMargins(16, 16, 16, 16)
                root.setSpacing(12)

                def make_card(title_text: str):
                    card = QWidget()
                    card.setObjectName("settingsCard")
                    v = QVBoxLayout(card)
                    v.setContentsMargins(20, 16, 20, 16)
                    v.setSpacing(12)
                    title = QLabel(title_text)
                    title.setObjectName("settingsTitle")
                    v.addWidget(title)
                    return (
                     card, v)

                (ui_card, ui_layout) = make_card("界面与启动")
                ui_form = QFormLayout()
                ui_form.setLabelAlignment(Qt.AlignRight)
                ui_form.setSpacing(8)
                self.theme_combo = QfwComboBox(self) if QFW_AVAILABLE else QComboBox(self)
                self.theme_combo.addItems(["light", "dark"])
                current_theme = self.settings.value("general/theme", "light")
                if current_theme in ('light', 'dark'):
                    self.theme_combo.setCurrentText(current_theme)
                ui_form.addRow(QLabel("主题"), self.theme_combo)
                self.sidebar_checkbox = QCheckBox("启动时显示左侧栏", self)
                self.sidebar_checkbox.setChecked(self.settings.value("general/showSidebarOnStart", True, type=bool))
                ui_form.addRow(QLabel("界面"), self.sidebar_checkbox)
                self.default_view_combo = QfwComboBox(self) if QFW_AVAILABLE else QComboBox(self)
                self.default_view_combo.addItems(["2D", "3D"])
                self.default_view_combo.setCurrentText(str(self.settings.value("general/defaultViewMode", "2D")))
                ui_form.addRow(QLabel("默认视图"), self.default_view_combo)
                self.splash_checkbox = QCheckBox("启动时显示启动动画", self)
                self.splash_checkbox.setChecked(self.settings.value("general/showSplashOnStart", True, type=bool))
                ui_form.addRow(QLabel("启动动画"), self.splash_checkbox)
                self.splash_style_combo = QfwComboBox(self) if QFW_AVAILABLE else QComboBox(self)
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
                else:
                    ui_form.addRow(QLabel("持续时间"), self.splash_duration_spin)
                    self.splash_gif_edit = QLineEdit(self)
                    self.splash_gif_edit.setPlaceholderText("可选：GIF 文件路径")
                    self.splash_gif_edit.setText(str(self.settings.value("general/splashGifPath", "")))
                    ui_form.addRow(QLabel("GIF 路径"), self.splash_gif_edit)
                    ui_layout.addLayout(ui_form)
                    root.addWidget(ui_card)
                    (maze_card, maze_layout) = make_card("迷宫与路径")
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
                    else:
                        maze_form.addRow(QLabel("尾迹长度"), self.tail_len_spin)
                        self.tail_fade_spin = QDoubleSpinBox(self)
                        self.tail_fade_spin.setDecimals(2)
                        self.tail_fade_spin.setRange(0.1, 1.2)
                        self.tail_fade_spin.setSingleStep(0.05)
                        self.tail_fade_spin.setValue(float(self.settings.value("general/tailFadePower", 0.85)))
                        maze_form.addRow(QLabel("尾迹渐隐强度"), self.tail_fade_spin)
                        goal_layout = QHBoxLayout()
                        self.goal_min_x_spin = QSpinBox(self)
                        self.goal_min_x_spin.setRange(0, 7)
                        self.goal_max_x_spin = QSpinBox(self)
                        self.goal_max_x_spin.setRange(0, 7)
                        self.goal_min_y_spin = QSpinBox(self)
                        self.goal_min_y_spin.setRange(0, 7)
                        self.goal_max_y_spin = QSpinBox(self)
                        self.goal_max_y_spin.setRange(0, 7)
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
                        self.replay_max_spin = QSpinBox(self)
                        self.replay_max_spin.setRange(10, 300)
                        self.replay_max_spin.setSingleStep(10)
                        self.replay_max_spin.setSuffix(" 条")
                        self.replay_max_spin.setValue(int(self.settings.value("replay/maxSaved", 60)))
                        maze_form.addRow(QLabel("回放保留"), self.replay_max_spin)
                        self.auto_send_best_chk = QCheckBox("到达终点后自动发送最优路径", self)
                        self.auto_send_best_chk.setChecked(self.settings.value("maze/autoSendBestPath", False, type=bool))
                        maze_form.addRow(QLabel("自动发送"), self.auto_send_best_chk)
                        maze_layout.addLayout(maze_form)
                        root.addWidget(maze_card)
                        (serial_card, serial_layout) = make_card("串口默认值")
                        serial_form = QFormLayout()
                        serial_form.setLabelAlignment(Qt.AlignRight)
                        serial_form.setSpacing(8)
                        common_baud_rates = [
                         "9600", "19200", "38400", "57600",
                         "115200", "230400", "460800", "921600"]
                        self.baud_combo = QfwComboBox(self) if QFW_AVAILABLE else QComboBox(self)
                        self.baud_combo.addItems(common_baud_rates)
                        _baud_pref = str(self.settings.value("serial/baudRate", "115200"))
                        if _baud_pref not in common_baud_rates:
                            self.baud_combo.addItem(_baud_pref)
                        self.baud_combo.setCurrentText(_baud_pref)
                        serial_form.addRow(QLabel("默认波特率"), self.baud_combo)
                        self.data_bits_combo = QfwComboBox(self) if QFW_AVAILABLE else QComboBox(self)
                        self.data_bits_combo.addItems(["5", "6", "7", "8"])
                        self.data_bits_combo.setCurrentText(str(self.settings.value("serial/dataBits", "8")))
                        serial_form.addRow(QLabel("默认数据位"), self.data_bits_combo)
                        self.stop_bits_combo = QfwComboBox(self) if QFW_AVAILABLE else QComboBox(self)
                        self.stop_bits_combo.addItems(["1", "1.5", "2"])
                        self.stop_bits_combo.setCurrentText(str(self.settings.value("serial/stopBits", "1")))
                        serial_form.addRow(QLabel("默认停止位"), self.stop_bits_combo)
                        self.parity_combo = QfwComboBox(self) if QFW_AVAILABLE else QComboBox(self)
                        self.parity_combo.addItems(["无","奇","偶","Mark","Space"])
                        self.parity_combo.setCurrentText(str(self.settings.value("serial/parity", "无")))
                        serial_form.addRow(QLabel("默认校验位"), self.parity_combo)
                        serial_layout.addLayout(serial_form)
                        root.addWidget(serial_card)
                        btn_row = QHBoxLayout()
                        self.save_btn = QfwPrimaryPushButton("保存设置", self) if QFW_AVAILABLE else QPushButton("保存设置", self)
                        self.apply_btn = QfwPushButton("应用设置", self) if QFW_AVAILABLE else QPushButton("应用设置", self)
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
                else:
                    QMessageBox.information(self, "设置", "已保存设置")

            def apply_settings_now(self):
                self.save_settings()
                if self.app_page is not None:
                    self.app_page.reload_settings()
                    if hasattr(self.app_page, "maze_plotter"):
                        tail_len = int(self.tail_len_spin.value())
                        tail_fade = float(self.tail_fade_spin.value())
                        self.app_page.maze_plotter.set_tail_style(tail_len, tail_fade)
                    self.app_page.goal_min_x = int(self.goal_min_x_spin.value())
                    self.app_page.goal_max_x = int(self.goal_max_x_spin.value())
                    self.app_page.goal_min_y = int(self.goal_min_y_spin.value())
                    self.app_page.goal_max_y = int(self.goal_max_y_spin.value())
                    self.app_page.auto_send_best_path = self.auto_send_best_chk.isChecked()
                    self.app_page.max_replay_saved = int(self.replay_max_spin.value())
                    self.app_page.default_view_mode = self.default_view_combo.currentText()


class DocsPage(QWidget):
            __doc__ = "美观简约的使用说明页面"

            def __init__(self, parent=None):
                super().__init__(parent)
                self.setObjectName("docsPage")
                main_layout = QVBoxLayout(self)
                main_layout.setContentsMargins(0, 0, 0, 0)
                main_layout.setSpacing(0)
                scroll_widget = QWidget()
                scroll_layout = QVBoxLayout(scroll_widget)
                scroll_layout.setContentsMargins(32, 32, 32, 32)
                scroll_layout.setSpacing(24)
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
                basic_card = self._create_section_card("🚀 基本操作", [
                 "1. 在「串口配置」区域选择串口和波特率等参数",
                 "2. 点击「连接」按钮建立串口连接",
                 "3. 在「发送数据」输入框中输入命令并发送",
                 "4. 在「控制面板」中使用开始/停止/复位功能",
                 "5. 实时查看「传感器数据」和「迷宫轨迹」"])
                scroll_layout.addWidget(basic_card)
                protocol_card = self._create_section_card("📡 通信协议", [
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
                 "  表示：位置(3,4)，朝东，角度45.5°，前方有墙，左右无墙，迷宫模式"])
                scroll_layout.addWidget(protocol_card)
                features_card = self._create_section_card("✨ 功能特性", [
                 "• 实时轨迹可视化：动态显示电脑鼠在迷宫中的移动轨迹",
                 "• 自动墙体绘制：根据传感器数据自动判断并绘制迷宫墙体",
                 "• 传感器监控：实时显示前后左右传感器状态",
                 "• 轨迹回放：保存并回放历史运行轨迹",
                 "• 数据导出：支持导出日志、轨迹等数据",
                 "• 现代化界面：简洁美观的用户界面设计"])
                scroll_layout.addWidget(features_card)
                scroll_layout.addStretch(1)
                scroll_area = QScrollArea()
                scroll_area.setWidget(scroll_widget)
                scroll_area.setWidgetResizable(True)
                scroll_area.setFrameShape(QScrollArea.NoFrame)
                scroll_area.setStyleSheet("\n            QScrollArea {\n                background-color: transparent;\n                border: none;\n            }\n        ")
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
            __doc__ = "美观简约的关于页面 - 显示应用信息和开发者信息"

            def __init__(self, parent=None):
                super().__init__(parent)
                self.setObjectName("aboutPage")
                main_layout = QVBoxLayout(self)
                main_layout.setContentsMargins(0, 0, 0, 0)
                main_layout.setSpacing(0)
                scroll_widget = QWidget()
                scroll_layout = QVBoxLayout(scroll_widget)
                scroll_layout.setContentsMargins(32, 32, 32, 32)
                scroll_layout.setSpacing(24)
                app_card = QWidget()
                app_card.setObjectName("appInfoCard")
                app_layout = QVBoxLayout(app_card)
                app_layout.setContentsMargins(40, 40, 40, 40)
                app_layout.setSpacing(16)
                app_layout.setAlignment(Qt.AlignCenter)
                app_name_label = QLabel(APP_NAME)
                app_name_label.setObjectName("appNameLabel")
                app_layout.addWidget(app_name_label, alignment=(Qt.AlignCenter))
                version_label = QLabel(f"版本 {APP_VERSION}")
                version_label.setObjectName("versionLabel")
                app_layout.addWidget(version_label, alignment=(Qt.AlignCenter))
                desc_label = QLabel("电子系统课程设计项目\n实时监控与可视化电脑鼠迷宫探索")
                desc_label.setObjectName("appDescLabel")
                desc_label.setAlignment(Qt.AlignCenter)
                desc_label.setWordWrap(True)
                app_layout.addWidget(desc_label, alignment=(Qt.AlignCenter))
                scroll_layout.addWidget(app_card)
                dev_card = self._create_info_card("👨\u200d💻 开发者信息", [
                 (
                  "开发者", APP_DEVELOPER),
                 (
                  "学校", APP_SCHOOL),
                 (
                  "项目", APP_PROJECT),
                 (
                  "邮箱", APP_EMAIL),
                 (
                  "网址", APP_URL if APP_URL else "暂无")])
                scroll_layout.addWidget(dev_card)
                tech_card = self._create_info_card("🔧 技术栈", [
                 (
                  "GUI框架", f"PyQt5 {PYQT_VERSION_STR}"),
                 (
                  "Qt版本", QT_VERSION_STR),
                 (
                  "Python版本", sys.version.split(" ")[0]),
                 ('绘图库', 'Matplotlib'),
                 ('通信协议', '串口通信 (QSerialPort)')])
                scroll_layout.addWidget(tech_card)
                copyright_card = QWidget()
                copyright_card.setObjectName("sectionCard")
                copyright_layout = QVBoxLayout(copyright_card)
                copyright_layout.setContentsMargins(24, 20, 24, 20)
                copyright_layout.setSpacing(12)
                copyright_title = QLabel("📄 版权信息")
                copyright_title.setObjectName("sectionTitle")
                copyright_layout.addWidget(copyright_title)
                copyright_text = QLabel(f"{APP_COPYRIGHT} {APP_DEVELOPER}\n\n本软件为电子系统设计课程项目，仅供学习交流使用。\n所有权利保留。")
                copyright_text.setObjectName("sectionContent")
                copyright_text.setWordWrap(True)
                copyright_layout.addWidget(copyright_text)
                scroll_layout.addWidget(copyright_card)
                buttons_card = QWidget()
                buttons_card.setObjectName("sectionCard")
                buttons_layout = QVBoxLayout(buttons_card)
                buttons_layout.setContentsMargins(24, 20, 24, 20)
                buttons_layout.setSpacing(12)
                buttons_title = QLabel("🔗 快速操作")
                buttons_title.setObjectName("sectionTitle")
                buttons_layout.addWidget(buttons_title)
                btn_row = QHBoxLayout()
                btn_row.setSpacing(12)
                copy_email_btn = QfwPushButton("📧 复制邮箱", self) if QFW_AVAILABLE else QPushButton("📧 复制邮箱", self)
                copy_email_btn.clicked.connect(lambda: self._copy_to_clipboard(APP_EMAIL, "邮箱"))
                btn_row.addWidget(copy_email_btn)
                copy_info_btn = QfwPushButton("📋 复制应用信息", self) if QFW_AVAILABLE else QPushButton("📋 复制应用信息", self)
                copy_info_btn.clicked.connect(self._copy_app_info)
                btn_row.addWidget(copy_info_btn)
                check_update_btn = QfwPushButton("🔄 检查更新", self) if QFW_AVAILABLE else QPushButton("🔄 检查更新", self)
                check_update_btn.clicked.connect(self._check_for_updates)
                btn_row.addWidget(check_update_btn)
                btn_row.addStretch(1)
                buttons_layout.addLayout(btn_row)
                scroll_layout.addWidget(buttons_card)
                scroll_layout.addStretch(1)
                scroll_area = QScrollArea()
                scroll_area.setWidget(scroll_widget)
                scroll_area.setWidgetResizable(True)
                scroll_area.setFrameShape(QScrollArea.NoFrame)
                scroll_area.setStyleSheet("\n            QScrollArea {\n                background-color: transparent;\n                border: none;\n            }\n        ")
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
                for (key, value) in items:
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
                info = f'应用名称：{APP_NAME}\n版本：{APP_VERSION}\n开发者：{APP_DEVELOPER}\n学校：{APP_SCHOOL}\n项目：{APP_PROJECT}\n邮箱：{APP_EMAIL}\n网址：{APP_URL}\nPython：{sys.version.split(" ")[0]}\nQt：{QT_VERSION_STR}\nPyQt5：{PYQT_VERSION_STR}\n'
                QGuiApplication.clipboard().setText(info)
                QMessageBox.information(self, "复制成功", "应用信息已复制到剪贴板")

            def _check_for_updates(self):
                """检查更新功能 - 从服务器或本地版本文件检查"""
                checking_msg = QMessageBox(self)
                checking_msg.setWindowTitle("检查更新")
                checking_msg.setText("正在检查更新...")
                checking_msg.setStandardButtons(QMessageBox.NoButton)
                checking_msg.setModal(False)
                checking_msg.show()
                QApplication.processEvents()
                version_url_json = "http://154.219.114.232/version.json"
                version_url_txt = "http://154.219.114.232/version.txt"

                def check_update_in_thread():
                    """在后台线程中执行更新检查"""
                    import urllib.request, urllib.error, json, re, traceback
                    latest_version = None
                    download_url = None
                    release_notes = ""
                    error_msg = ""
                    try:
                        user_agent = f"MicromouseApp/{APP_VERSION}"
                        req = urllib.request.Request(version_url_json,
                          headers={"User-Agent": user_agent})
                        with urllib.request.urlopen(req, timeout=10) as response:
                            content = response.read().decode("utf-8")
                            data = json.loads(content)
                            latest_version = data.get("version")
                            download_url = data.get("download_url", "")
                            release_notes = data.get("release_notes", "")
                            print(f"[更新检查] 成功获取版本信息: {latest_version}")
                    except urllib.error.HTTPError as e:
                        try:
                            error_msg = f"HTTP错误 {e.code}: {e.reason}"
                            print(f"[更新检查] JSON请求失败: {error_msg}")
                            try:
                                user_agent = f"MicromouseApp/{APP_VERSION}"
                                req = urllib.request.Request(version_url_txt,
                                  headers={"User-Agent": user_agent})
                                with urllib.request.urlopen(req, timeout=10) as response:
                                    content = response.read().decode("utf-8")
                                    match = re.search("version[:\\s]+([\\d.]+)", content, re.IGNORECASE)
                                    if not match:
                                        match = re.search("(\\d+\\.\\d+\\.\\d+)", content)
                                    if match:
                                        latest_version = match.group(1)
                                        print(f"[更新检查] 文本格式获取版本: {latest_version}")
                            except Exception as e2:
                                try:
                                    error_msg = f"文本格式也失败: {str(e2)}"
                                    print(f"[更新检查] {error_msg}")
                                finally:
                                    e2 = None
                                    del e2

                        finally:
                            e = None
                            del e

                    except urllib.error.URLError as e:
                        try:
                            error_msg = f"网络连接错误: {str(e.reason)}"
                            print(f"[更新检查] {error_msg}")
                        finally:
                            e = None
                            del e

                    except json.JSONDecodeError as e:
                        try:
                            error_msg = f"JSON解析错误: {str(e)}"
                            print(f"[更新检查] {error_msg}")
                        finally:
                            e = None
                            del e

                    except Exception as e:
                        try:
                            error_msg = f"未知错误: {str(e)}"
                            print(f"[更新检查] {error_msg}")
                            traceback.print_exc()
                        finally:
                            e = None
                            del e

                    else:
                        if latest_version is None:
                            try:
                                import os
                                app_dir = QApplication.instance().applicationDirPath() if QApplication.instance() else os.getcwd()
                                version_file = os.path.join(app_dir, "version_info.json")
                                if os.path.exists(version_file):
                                    with open(version_file, "r", encoding="utf-8") as f:
                                        data = json.load(f)
                                        latest_version = data.get("version", APP_VERSION)
                                        download_url = data.get("download_url", APP_URL)
                                        release_notes = data.get("release_notes", "")
                                        print(f"[更新检查] 使用本地版本文件: {latest_version}")
                            except Exception as e:
                                try:
                                    print(f"[更新检查] 本地版本文件读取失败: {str(e)}")
                                finally:
                                    e = None
                                    del e

                        print(f"[更新检查] 准备显示结果: latest_version={latest_version}, download_url={download_url}")
                        result_queue.put((
                         latest_version, download_url, release_notes, error_msg))

                result_queue = queue.Queue()
                thread = threading.Thread(target=check_update_in_thread, daemon=True)
                thread.start()

                def check_result():
                    try:
                        (latest_version, download_url, release_notes, error_msg) = result_queue.get_nowait()
                        timer.stop()
                        checking_msg.hide()
                        checking_msg.close()
                        checking_msg.deleteLater()
                        QApplication.processEvents()
                        QTimer.singleShot(50, lambda: self._show_update_result(latest_version, download_url, release_notes, error_msg))
                    except queue.Empty:
                        pass

                timer = QTimer(self)
                timer.timeout.connect(check_result)
                timer.start(100)

            def _show_update_result(self, latest_version, download_url, release_notes, error_msg):
                """在主线程中显示更新检查结果"""
                if latest_version:
                    if self._compare_versions(APP_VERSION, latest_version) < 0:
                        msg_text = f"发现新版本！\n\n当前版本：{APP_VERSION}\n最新版本：{latest_version}\n\n"
                        if release_notes:
                            notes = release_notes.replace("\\n", "\n")
                            msg_text += f"{notes}\n\n"
                        msg_text += "是否访问下载页面？"
                        msg = QMessageBox(self)
                        msg.setWindowTitle("发现新版本")
                        msg.setIcon(QMessageBox.Information)
                        msg.setText(msg_text)
                        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        msg.setDefaultButton(QMessageBox.Yes)
                        if msg.exec_() == QMessageBox.Yes:
                            import webbrowser
                            target_url = download_url if download_url else APP_URL
                            webbrowser.open(target_url)
                    else:
                        QMessageBox.information(self, "检查更新", f"当前版本：{APP_VERSION}\n\n您使用的是最新版本！")
                else:
                    error_info = f"\n\n错误信息：{error_msg}" if error_msg else ""
                    QMessageBox.warning(self, "检查更新", f"当前版本：{APP_VERSION}\n\n无法连接到更新服务器。" + error_info + "\n\n请检查网络连接或稍后重试。\n\n更新服务器地址：http://154.219.114.232/version.json")

            def _compare_versions(self, v1: str, v2: str) -> int:
                """比较版本号
        返回: -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2
        """

                def normalize_version(v):
                    parts = []
                    for part in v.split("."):
                        try:
                            parts.append(int(part))
                        except ValueError:
                            parts.append(0)

                    while len(parts) < 3:
                        parts.append(0)

                    return tuple(parts)

                n1 = normalize_version(v1)
                n2 = normalize_version(v2)
                if n1 < n2:
                    return -1
                if n1 > n2:
                    return 1
                return 0


class SupportPage(QWidget):

            def __init__(self, parent=None, app_page=None):
                super().__init__(parent)
                self.setObjectName("supportPage")
                self.app_page = app_page
                outer = QVBoxLayout(self)
                form = QFormLayout()
                form.setContentsMargins(12, 12, 12, 12)
                form.setSpacing(8)
                self.lbl_py = QLabel(sys.version.split(" ")[0])
                self.lbl_qt = QLabel(QT_VERSION_STR)
                self.lbl_pyqt = QLabel(PYQT_VERSION_STR)
                self.lbl_ports = QLabel("点击刷新…")
                form.addRow(QLabel("Python:"), self.lbl_py)
                form.addRow(QLabel("Qt 版本:"), self.lbl_qt)
                form.addRow(QLabel("GUI 框架:"), self.lbl_pyqt)
                form.addRow(QLabel("可用串口:"), self.lbl_ports)
                btn_row = QHBoxLayout()
                self.refresh_btn = QfwPushButton("刷新串口", self) if QFW_AVAILABLE else QPushButton("刷新串口", self)
                self.copy_btn = QfwPrimaryPushButton("复制诊断", self) if QFW_AVAILABLE else QPushButton("复制诊断", self)
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
                    try:
                        self.lbl_ports.setText(f"错误: {e}")
                    finally:
                        e = None
                        del e

            def build_diagnostics(self) -> str:
                from datetime import datetime
                lines = []
                lines.append(f'时间: {datetime.now().isoformat(timespec="seconds")}')
                lines.append(f"Python: {sys.version}")
                lines.append(f"Qt: {QT_VERSION_STR}")
                lines.append(f"PyQt: {PYQT_VERSION_STR}")
                try:
                    screen = QGuiApplication.primaryScreen()
                    if screen is not None:
                        size = screen.size()
                        lines.append(f"屏幕: {size.width()}x{size.height()}")
                except Exception:
                    pass
                else:
                    try:
                        ports = [p.portName() for p in QSerialPortInfo.availablePorts()]
                        lines.append("串口: " + (", ".join(ports) if ports else "(无)"))
                    except Exception as e:
                        try:
                            lines.append(f"串口查询错误: {e}")
                        finally:
                            e = None
                            del e

                    else:
                        return "\n".join(lines)

            def copy_diagnostics(self):
                text = self.build_diagnostics()
                QGuiApplication.clipboard().setText(text)
                QMessageBox.information(self, "诊断", "诊断信息已复制到剪贴板")


class RealtimeLogPage(QWidget):

            def __init__(self, parent=None, app_page=None):
                super().__init__(parent)
                self.setObjectName("realtimeLogPage")
                self.app_page = app_page
                root = QVBoxLayout(self)
                tools = QHBoxLayout()
                self.filter_edit = QLineEdit(self)
                self.filter_edit.setPlaceholderText("过滤关键字（留空不过滤）")
                self.pause_chk = QCheckBox("暂停滚动", self)
                self.show_rx_chk = QCheckBox("显示接收", self)
                self.show_rx_chk.setChecked(True)
                self.show_tx_chk = QCheckBox("显示发送", self)
                self.show_tx_chk.setChecked(True)
                self.export_btn = QfwPushButton("导出日志", self) if QFW_AVAILABLE else QPushButton("导出日志", self)
                tools.addWidget(QLabel("筛选:"))
                tools.addWidget(self.filter_edit, 1)
                tools.addWidget(self.show_rx_chk)
                tools.addWidget(self.show_tx_chk)
                tools.addWidget(self.pause_chk)
                tools.addWidget(self.export_btn)
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
                if self.app_page is not None:
                    self.app_page.log_subscribers.append(self.on_log)
                self.export_btn.clicked.connect(self.export_logs)
                self._stats_timer = QTimer(self)
                self._stats_timer.setInterval(500)
                self._stats_timer.timeout.connect(self.update_stats)
                self._stats_timer.start()
                self._rx_buffer = []
                self._tx_buffer = []

            def on_log(self, timestamp: str, direction: str, text: str):
                key = self.filter_edit.text().strip()
                if key and key not in text:
                    if key not in direction:
                        return
                    if direction == "RX":
                        if not self.show_rx_chk.isChecked():
                            return
                        if direction == "TX" and not self.show_tx_chk.isChecked():
                            return
                    line = f"[{timestamp}] {direction} {text}"
                if direction == "RX":
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
                (rx_bps, tx_bps) = self.app_page.get_throughput_bps()
                self.lbl_rx_bps.setText(f"RX: {rx_bps} bps")
                self.lbl_tx_bps.setText(f"TX: {tx_bps} bps")
                self.lbl_err.setText(f"错误帧: {self.app_page.error_frame_count}")

            def export_logs(self):
                all_text = "\n".join(["--- RX ---"] + self._rx_buffer + ["", "--- TX ---"] + self._tx_buffer)
                (path, _) = QFileDialog.getSaveFileName(self, "导出日志", "logs.txt", "Text Files (*.txt)")
                if path:
                    try:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(all_text)
                        QMessageBox.information(self, "导出日志", "日志已保存")
                    except Exception as e:
                        try:
                            QMessageBox.critical(self, "导出失败", str(e))
                        finally:
                            e = None
                            del e


class ReplayPage(QWidget):
            __doc__ = "轨迹回放页：列表查看、播放/暂停/倍速、叠加对比、导出"

            def __init__(self, parent=None, app_page=None):
                super().__init__(parent)
                self.setObjectName("replayPage")
                self.app_page = app_page
                self.current_run = None
                root = QVBoxLayout(self)
                top = QHBoxLayout()
                root.addLayout(top)
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
                self.replay_fig = Figure(figsize=(5, 5), dpi=100, facecolor="#fafbfc")
                self.replay_ax = self.replay_fig.add_subplot(111)
                self._init_plot_style()
                self.replay_canvas = FigureCanvas(self.replay_fig)
                top.addWidget(self.replay_canvas, 2)
                self.btn_refresh.clicked.connect(self.refresh_list)
                self.btn_save.clicked.connect(self.save_current_run)
                self.btn_export_csv.clicked.connect(self.export_csv)
                self.btn_export_png.clicked.connect(self.export_png)
                self.refresh_list()
                self.draw_selected()

            def _init_plot_style(self):
                ax = self.replay_ax
                ax.clear()
                ax.set_facecolor("#ffffff")
                ax.set_xlim(-0.5, 8.5)
                ax.set_ylim(-0.5, 8.5)
                ax.set_xticks(range(9))
                ax.set_yticks(range(9))
                ax.grid(True, color="#e5e7eb", linewidth=0.9, alpha=0.8)
                for spine in ax.spines.values():
                    spine.set_color("#e5e7eb")
                    spine.set_linewidth(1.0)

                ax.set_title("轨迹回放", color="#111827", fontsize=14, fontweight="600", pad=12)

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
                name = f"run_{len(self.app_page.replay_runs) + 1}"
                self.app_page.snapshot_current_run(name=name)
                self.refresh_list()
                QMessageBox.information(self, "保存轨迹", f"已保存为 {name}")

            def draw_selected(self):
                self._init_plot_style()
                if not self.app_page:
                    self.replay_canvas.draw_idle()
                    return
                selected = [i.row() for i in self.list.selectedIndexes()]
                if not selected:
                    if self.app_page.replay_runs:
                        selected = [
                         len(self.app_page.replay_runs) - 1]
                        self.list.setCurrentRow(selected[0])
                palette = [
                 "#6366f1","#10b981","#f59e0b","#ef4444","#0ea5e9","#a855f7"]
                draw_all = self.overlay_chk.isChecked()
                targets = selected if draw_all else selected[:1]
                for (k, idx) in enumerate(targets):
                    if idx >= len(self.app_page.replay_runs):
                        pass
                    else:
                        run = self.app_page.replay_runs[idx]
                        xs = run.get("path_x", [])
                        ys = run.get("path_y", [])
                        color = palette[k % len(palette)]
                        self.replay_ax.plot(xs, ys, color=color, linewidth=2.5, alpha=0.9)
                        if xs:
                            if ys:
                                self.replay_ax.plot((xs[0]), (ys[0]), "o", color="#22c55e", markersize=8, markeredgecolor="#fff", markeredgewidth=2)
                                self.replay_ax.plot((xs[-1]), (ys[-1]), "o", color="#ef4444", markersize=9, markeredgecolor="#fff", markeredgewidth=2)
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
                (path, _) = QFileDialog.getSaveFileName(self, "导出轨迹 CSV", f'{run.get("name", "run")}.csv', "CSV Files (*.csv)")
                if not path:
                    return
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write("x,y\n")
                        for (x, y) in zip(run.get("path_x", []), run.get("path_y", [])):
                            f.write(f"{x},{y}\n")

                    QMessageBox.information(self, "导出", "CSV 导出成功")
                except Exception as e:
                    try:
                        QMessageBox.critical(self, "导出失败", str(e))
                    finally:
                        e = None
                        del e

            def export_png(self):
                idxs = self.list.selectedIndexes()
                if not idxs:
                    QMessageBox.warning(self, "导出", "请选择要导出的轨迹")
                    return
                self.draw_overlay()
                (path, _) = QFileDialog.getSaveFileName(self, "导出轨迹 PNG", "replay.png", "PNG Files (*.png)")
                if not path:
                    return
                try:
                    self.replay_fig.savefig(path, dpi=180, bbox_inches="tight")
                    QMessageBox.information(self, "导出", "PNG 导出成功")
                except Exception as e:
                    try:
                        QMessageBox.critical(self, "导出失败", str(e))
                    finally:
                        e = None
                        del e


class StartupSplash(QWidget):

            def __init__(self, theme='light', mode='progress', duration_ms=1800, gif_path=''):
                super().__init__(None, Qt.SplashScreen | Qt.FramelessWindowHint)
                self.setAttribute(Qt.WA_TranslucentBackground, True)
                self.setObjectName("startupSplash")
                self._mode = mode
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
                    card.setStyleSheet("#splashCard{background:#111827; border:1px solid #374151; border-radius:12px;}")
                else:
                    title.setStyleSheet(title_style_light)
                    subtitle.setStyleSheet(sub_style_light)
                    card.setStyleSheet("#splashCard{background:#ffffff; border:1px solid #e5e7eb; border-radius:12px;}")
                layout.addWidget(title)
                layout.addWidget(subtitle)
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
                    else:
                        content_layout.addWidget(self._gif_label)
                    if self._mode != "gif":
                        self._progress = QProgressBar(self._content_wrap)
                        self._progress.setRange(0, 0)
                        self._progress.setTextVisible(False)
                        self._progress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                        self._progress.setMinimumWidth(360)
                        self._progress.setFixedHeight(12)
                        if is_dark:
                            self._progress.setStyleSheet("QProgressBar{background-color:#1f2937; border:1px solid #374151; border-radius:6px;}QProgressBar::chunk{background-color:#3b82f6; border-radius:6px;}")
                        else:
                            self._progress.setStyleSheet("QProgressBar{background-color:#f3f4f6; border:1px solid #e5e7eb; border-radius:6px;}QProgressBar::chunk{background-color:#3b82f6; border-radius:6px;}")
                        content_layout.addWidget(self._progress)
                    layout.addWidget(self._content_wrap)
                    outer.addWidget(card)
                    self.resize(460, 240)
                try:
                    screen = QGuiApplication.primaryScreen()
                    if screen is not None:
                        geo = screen.geometry()
                        self.move(geo.center().x() - self.width() // 2, geo.center().y() - self.height() // 2)
                except Exception:
                    pass
                else:
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
                else:
                    self.close()


def run_fluent_window():
    win = FluentWindow()
    win.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
    try:
        win.setMicaEffectEnabled(True)
    except Exception:
        pass
    
    run_page_container = QWidget()
    run_page_container.setObjectName("runPage")
    run_layout = QVBoxLayout(run_page_container)
    app_page = MicroMouseApp(as_page=True)
    run_layout.addWidget(app_page.central_widget)
    win.addSubInterface(run_page_container, FIF.HOME, "运行", NavigationItemPosition.TOP)
    settings_page = SettingsPage(parent=win, app_page=app_page)
    win.addSubInterface(settings_page, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM)
    docs_page = DocsPage(parent=win)
    win.addSubInterface(docs_page, FIF.BOOK_SHELF, "使用说明", NavigationItemPosition.BOTTOM)
    about_page = AboutPage(parent=win)
    try:
        about_icon = getattr(FIF, "INFO", FIF.HELP) if QFW_AVAILABLE else None
    except Exception:
        about_icon = FIF.HELP if QFW_AVAILABLE else None
    
    win.addSubInterface(about_page, about_icon, "关于", NavigationItemPosition.BOTTOM)
    support_page = SupportPage(parent=win, app_page=app_page)
    win.addSubInterface(support_page, FIF.SETTING, "支持/诊断", NavigationItemPosition.BOTTOM)
    rtlog_page = RealtimeLogPage(parent=win, app_page=app_page)
    win.addSubInterface(rtlog_page, FIF.SEND, "实时日志", NavigationItemPosition.TOP)
    replay_page = ReplayPage(parent=win, app_page=app_page)
    win.addSubInterface(replay_page, FIF.INFO, "轨迹回放", NavigationItemPosition.TOP)
    win.resize(1200, 760)
    win.show()
    return win


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings = QSettings("MicromouseLab", "MicromouseApp")
    try:
        settings.sync()
    except Exception:
        # 如果设置读取失败，不影响程序继续运行
        pass
    
    # 读取启动画面设置
    try:
        show_splash = settings.value("general/showSplashOnStart", True, type=bool)
    except Exception:
        show_splash = True
    
    try:
        splash_style = str(settings.value("general/splashStyle", "progress"))
    except Exception:
        splash_style = "progress"
    
    try:
        splash_duration = int(settings.value("general/splashDurationMs", 3000, type=int))
    except Exception:
        splash_duration = 3000
    
    try:
        splash_gif = str(settings.value("general/splashGifPath", ""))
    except Exception:
        splash_gif = ""
    
    try:
        theme_pref = str(settings.value("general/theme", "light"))
    except Exception:
        theme_pref = "light"
    
    splash = None
    if show_splash:
        try:
            splash = StartupSplash(theme=theme_pref, mode=splash_style, duration_ms=splash_duration, gif_path=splash_gif)
            splash.show()
            app.processEvents()
        except Exception:
            splash = None

    if QFW_AVAILABLE:
        _w = run_fluent_window()
        sys.exit(app.exec_())
    else:
        window = MicroMouseApp()
        window.show()
        sys.exit(app.exec_())