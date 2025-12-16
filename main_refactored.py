"""Micromouse 上位机 - 重构版入口

说明：
    - 保留原有 main.py 中的全部业务逻辑与页面类；
    - 在本文件中通过“子类 + 新外壳窗口”的方式对界面和布局进行重构；
    - 主控制页面采用「上：左侧控制 / 右侧迷宫，下：实时日志」的三分布局；
    - 依然提供 Fluent UI 外壳导航，并保留独立的“实时日志 / 轨迹回放 / 设置 / 文档 / 关于 / 支持”页面。

依赖：
    pip install PyQt5
"""

import sys
from typing import Optional

from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QApplication, QSplitter

# 复用现有业务常量与页面类（不改动 main.py）
from main import (  # type: ignore
    APP_NAME,
    APP_VERSION,
    APP_PROJECT,
    APP_SCHOOL,
    MicroMouseApp,
    SettingsPage,
    DocsPage,
    AboutPage,
    SupportPage,
    RealtimeLogPage,
    ReplayPage,
    StartupSplash,
)


def create_refactored_app_page(as_page: bool = True) -> MicroMouseApp:
    """创建一个带有“底部内嵌实时日志”的重构版主页面实例。

    注意：
        - 不通过继承，而是在实例构造完成后重排其内部布局；
        - 该函数必须在 QApplication 创建之后再调用（由 Fluent 外壳负责保证）。
    """

    app_page = MicroMouseApp(as_page=as_page)

    # 防御性判断：如果父类结构有变更，不做重排以避免崩溃
    if not hasattr(app_page, "content_stack"):
        return app_page
    try:
        main_page = app_page.content_stack.widget(0)
    except Exception:
        return app_page
    if main_page is None:
        return app_page

    # 原 main.py 中 create_main_control_page() 会挂一个 self.h_splitter
    h_splitter = getattr(app_page, "h_splitter", None)
    if h_splitter is None:
        return app_page

    layout = main_page.layout()
    if layout is None:
        return app_page

    # 创建新的垂直 splitter：上半部分放原有水平布局，下半部分放实时日志
    v_splitter = QSplitter(Qt.Vertical, main_page)
    v_splitter.setObjectName("mainVerticalSplitter")

    # 从原 layout 中移除旧的水平 splitter，放入新的垂直 splitter 顶部
    try:
        layout.removeWidget(h_splitter)
    except Exception:
        pass
    h_splitter.setParent(v_splitter)
    v_splitter.addWidget(h_splitter)

    # 底部嵌入一个精简版实时日志页面，复用 RealtimeLogPage 的逻辑
    # 注意：这里单独实例化一个页面，不影响导航栏中的“实时日志”完整页面
    inline_log_page = RealtimeLogPage(parent=app_page, app_page=app_page)
    inline_log_page.setObjectName("inlineRealtimeLog")

    # 将下方日志页放入 splitter
    v_splitter.addWidget(inline_log_page)

    # 调整拉伸比例：上面主控制区域更大，下面日志区域略小
    v_splitter.setStretchFactor(0, 3)
    v_splitter.setStretchFactor(1, 2)

    # 将新的垂直 splitter 放回主控制页的根布局中
    layout.addWidget(v_splitter)

    # 在实例上挂一个引用，方便未来扩展（例如访问 inline_log_page）
    app_page.inline_log_page = inline_log_page  # type: ignore[attr-defined]

    return app_page


def main():
    """应用入口：使用重构版主控制页面布局（左控右图 + 底部日志）。"""
    app = QApplication.instance() or QApplication(sys.argv)
    settings = QSettings("MicromouseLab", "MicromouseApp")

    # 启动画面：沿用原有逻辑与设置项
    show_splash = settings.value("general/showSplashOnStart", True, type=bool)
    splash_style = str(settings.value("general/splashStyle", "progress"))
    splash_gif = str(settings.value("general/splashGifPath", ""))
    try:
        splash_duration = int(settings.value("general/splashDurationMs", 3000, type=int))
    except Exception:
        splash_duration = 3000

    splash = None
    if show_splash:
        try:
            splash = StartupSplash(
                theme=str(settings.value("general/theme", "light")),
                mode=splash_style,
                duration_ms=splash_duration,
                gif_path=splash_gif,
            )
            splash.show()
            app.processEvents()
        except Exception:
            splash = None

    # 使用重构后的主控制页面（普通 QMainWindow，而非 FluentWindow）
    window = create_refactored_app_page(as_page=False)
    window.show()

    exit_code = app.exec_()
    if splash is not None:
        splash.finish()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()


