# style DarkTheme
from config.theme.ui_style import UiStyle
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation
import qtawesome as qta
from views.window.title_bar import TitleBar
from views.window.resources import (APP_TITLE)

class Dashboard(QMainWindow):
    """Главное окно PyPAC-MV — отображает всех агентов как вкладки."""

    def __init__(self, agents: dict, AgentRegistry):
        super().__init__()
        style = UiStyle(self)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Боковая панель (всегда видна)
        self.side_menu = QFrame(self)
        self.side_menu.setFixedWidth(45)

        # Контент боковой панели
        layout_menu = QVBoxLayout()
        layout_menu.setContentsMargins(0, 0, 0, 0)
        layout_menu.setSpacing(0)

        self.agents = agents
        self.setWindowTitle(f"{APP_TITLE}")
        self.setGeometry(200, 100, 800, 600)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setDocumentMode(True)

        # Добавляем кнопки для перехода
        for name, meta in AgentRegistry.metadata.items():
           btn_item = self._make_icon_button(meta.get('icon', 'fa5s.cog'), name)


        # добавляем вкладки для всех агентов
        # for name, agent in self.agents.items():
        #    tab = self._create_agent_tab(agent, name)
        #    self.tabs.addTab(tab, name.capitalize())
        # self.setCentralWidget(self.tabs)

        self.title_bar = TitleBar(self)

        # Заголовок


    def _create_agent_tab(self, agent, name):
        """Создаёт вкладку для агента."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        if hasattr(agent, 'presentation') and hasattr(agent.presentation, 'widget'):
            layout.addWidget(agent.presentation.widget)
        else:
            layout.addWidget(QLabel(f"⚠️ Агент {name} не имеет представления", alignment=Qt.AlignmentFlag.AlignCenter))

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
