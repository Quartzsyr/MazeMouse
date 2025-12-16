"""基于 Fluent UI 外壳的 Micromouse 上位机入口。

该文件在不改动现有 `main.py` 业务逻辑的前提下，提供
一套 FluentWindow 容器，将原有 `MicroMouseApp` 以及
设置/文档/关于/实时日志/轨迹回放等页面封装到 Fluent
导航界面中。保持原有窗口的所有功能与信号处理。

注意：为避免 “QWidget: Must construct a QApplication before a QWidget”
错误，qfluentwidgets 与 qframelesswindow 的导入和窗口定义均在
创建 QApplication 之后进行。
"""

import sys
from typing import Optional

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

# 引入现有业务类与常量（仅定义，不创建 QWidget 实例）
from main import (
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


def build_fluent_window_classes():
    """延迟导入 Fluent 依赖，确保 QApplication 已存在。"""
    try:
        from qfluentwidgets import (
            FluentWindow,
            NavigationItemPosition,
            setTheme,
            setThemeColor,
            Theme,
            FluentIcon as FIF,
        )
    except Exception as exc:  # pragma: no cover - 依赖缺失时回退
        raise RuntimeError("缺少 qfluentwidgets，请先安装：pip install qfluentwidgets") from exc

    try:
        from qframelesswindow import StandardTitleBar
        FRAM_READY = True
    except Exception:
        StandardTitleBar = None  # type: ignore
        FRAM_READY = False

    class MicromouseFluentWindow(FluentWindow):
        """将原有页面包装到 FluentWindow 的导航结构中。"""

        def __init__(self, settings: Optional[QSettings] = None):
            super().__init__()

            self.settings = settings or QSettings("MicromouseLab", "MicromouseApp")

            self._init_theme(Theme, setTheme, setThemeColor)
            self._init_title_bar(StandardTitleBar, FRAM_READY)
            self._init_pages(FIF, NavigationItemPosition)

            self.resize(1200, 760)
            self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")

        def _init_theme(self, Theme, setTheme, setThemeColor):
            """读取设置并应用 Fluent 主题与主题色。"""
            theme_pref = str(self.settings.value("general/theme", "light"))
            theme_color = str(self.settings.value("general/themeColor", "#0078d4"))

            theme_map = {"dark": Theme.DARK, "light": Theme.LIGHT, "auto": Theme.AUTO}
            setTheme(theme_map.get(theme_pref.lower(), Theme.AUTO))
            setThemeColor(theme_color)

        def _init_title_bar(self, StandardTitleBar, FRAM_READY: bool):
            """可选使用无边框标题栏。"""
            if FRAM_READY and StandardTitleBar is not None:
                title_bar = StandardTitleBar(self)
                title_bar.setTitle(f"{APP_NAME} v{APP_VERSION}")
                self.setTitleBar(title_bar)

        def _init_pages(self, FIF, NavigationItemPosition):
            """创建并注册所有子页面。"""
            # 运行主界面：使用 as_page 以嵌入 central_widget
            app_page = MicroMouseApp(as_page=True)
            run_container = QWidget()
            run_container.setObjectName("runPage")
            run_layout = QVBoxLayout(run_container)
            run_layout.setContentsMargins(0, 0, 0, 0)
            run_layout.setSpacing(0)
            run_layout.addWidget(app_page.central_widget)

            self.addSubInterface(run_container, FIF.HOME, "运行", NavigationItemPosition.TOP)

            # 实时日志、轨迹回放
            rtlog_page = RealtimeLogPage(parent=self, app_page=app_page)
            self.addSubInterface(rtlog_page, FIF.SEND, "实时日志", NavigationItemPosition.TOP)

            replay_page = ReplayPage(parent=self, app_page=app_page)
            self.addSubInterface(replay_page, FIF.INFO, "轨迹回放", NavigationItemPosition.TOP)

            # 设置、文档、关于、支持
            settings_page = SettingsPage(parent=self, app_page=app_page)
            self.addSubInterface(settings_page, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM)

            docs_page = DocsPage(parent=self)
            self.addSubInterface(docs_page, FIF.BOOK_SHELF, "使用说明", NavigationItemPosition.BOTTOM)

            about_icon = getattr(FIF, "INFO", FIF.HELP)
            about_page = AboutPage(parent=self)
            self.addSubInterface(about_page, about_icon, "关于", NavigationItemPosition.BOTTOM)

            support_page = SupportPage(parent=self, app_page=app_page)
            self.addSubInterface(support_page, FIF.SETTING, "支持/诊断", NavigationItemPosition.BOTTOM)

    return MicromouseFluentWindow


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    settings = QSettings("MicromouseLab", "MicromouseApp")

    # 可选启动动画沿用原有逻辑
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

    MicromouseFluentWindow = build_fluent_window_classes()
    window = MicromouseFluentWindow(settings=settings)
    window.show()

    exit_code = app.exec_()
    if splash is not None:
        splash.finish()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

