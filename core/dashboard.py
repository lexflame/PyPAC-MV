import qtawesome as qta

from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation

from config.theme.ui_style import UiStyle
from core.loader import AgentRegistry

from views.window.title_bar import TitleBar
from views.window.resources import (APP_TITLE)

class Dashboard(QWidget):
    def __init__(self, agents: dict, AgentRegistry):
        super().__init__()
        style = UiStyle(self)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        """Боковая панель (всегда видна)"""
        self.side_menu = QFrame(self)
        self.side_menu.setStyleSheet(f"border: 0.5px solid black;")
        self.side_menu.setFixedWidth(45)

        """Контент боковой панели"""
        layout_menu = QVBoxLayout()
        layout_menu.setContentsMargins(0, 0, 0, 0)
        layout_menu.setSpacing(0)

        """Добавляем кнопки с иконками для перехода между табами"""
        for name, meta in AgentRegistry.metadata.items():
            item_btn = self._make_icon_button(meta.get('icon', 'fa5s.cog'), name)
            layout_menu.addWidget(item_btn)

        """Добавляем область работы для проектов и ЧТО_ТО ЕЩЕ"""
        self.nav_project = QTabWidget()
        self.nav_project.setFixedWidth(250)
        self.nav_project.setDocumentMode(True)

        self.nav_project.widget = QWidget()
        layout = QVBoxLayout(self.nav_project.widget)
        project = self._create_agent_tab(self.nav_project.widget, name)
        label = 'Проекты'
        self.nav_project.addTab(project, label)

        """Добавляем табы для агентов"""
        self.agents = agents
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setDocumentMode(True)

        self.main_widget = QMainWindow(self)
        self.main_widget.setFocus()

        for name, agent in self.agents.items():
            tab = self._create_agent_tab(agent, name)
            label = agent.presentation.windowTitle() if hasattr(agent.presentation, 'windowTitle') else name
            self.tabs.addTab(tab, label)
        # self.main_widget.setCentralWidget(self.tabs)

        layout_menu.addStretch()
        self.side_menu.setLayout(layout_menu)

        """Заголовок"""
        self.title_bar = TitleBar(self)

        """Контент справа"""
        self.content = QLabel("Привет! Это окно с **боковой панелью**, которая всегда видна.")
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        """Объединяем боковую панель и контент"""
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.side_menu)
        content_layout.addWidget(self.nav_project)
        content_layout.addWidget(self.tabs)

        """Общий layout"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.title_bar)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        """Разворачиваем окно на весь экран"""
        screen_geometry = self.screen().availableGeometry()
        self.setGeometry(screen_geometry)

    def _create_agent_tab(self, agent, name):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        try:
            if hasattr(agent.presentation, 'widget'):
                layout.addWidget(agent.presentation.widget)
            else:
                cw = getattr(agent.presentation, 'centralWidget', lambda: None)()
                if cw is not None:
                    layout.addWidget(cw)
                else:
                    layout.addWidget(QLabel(f"⚠️ Агент {name} не имеет представления", alignment=Qt.AlignmentFlag.AlignCenter))
        except Exception:
            layout.addWidget(QLabel(f"⚠️ Ошибка отображения агента {name}", alignment=Qt.AlignmentFlag.AlignCenter))
        return widget

    def _make_icon_button(self, icon_name, tooltip):
        """Создание кнопки с иконкой"""
        icon = qta.icon(icon_name, color="white")
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(24, 24))
        btn.setFixedSize(45, 45)  # квадратные кнопки
        btn.setToolTip(tooltip)  # подсказка при наведении
        btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #3d3d3d;
                        border-radius: 8px;
                    }
                """)
        return btn