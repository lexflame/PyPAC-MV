# style DarkTheme
from config.theme.ui_style import UiStyle
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation
import qtawesome as qta
from views.window.title_bar import TitleBar
from views.window.resources import (APP_TITLE)

class Dashboard(QWidget):
    """Главное окно PyPAC-MV — отображает всех агентов как вкладки."""

    def __init__(self, agents: dict, AgentRegistry):
        super().__init__()
        style = UiStyle(self)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Боковая панель (всегда видна)
        self.side_menu = QFrame(self)
        self.side_menu.setStyleSheet(f"border: 0.5px solid black;")
        self.side_menu.setFixedWidth(45)

        # Контент боковой панели
        layout_menu = QVBoxLayout()
        layout_menu.setContentsMargins(0, 0, 0, 0)
        layout_menu.setSpacing(0)

        # Кнопки с иконками
        self.home_btn = self._make_icon_button("fa5s.tasks", "Задачи")
        self.tasks_btn = self._make_icon_button("ri.treasure-map-line", "Карты")
        self.notes_btn = self._make_icon_button("fa5s.sticky-note", "Заметки")
        self.stats_btn = self._make_icon_button("msc.file-media", "Статистика")
        self.settings_btn = self._make_icon_button("fa5s.cog", "Настройки")

        for btn in [self.home_btn, self.tasks_btn, self.notes_btn, self.stats_btn, self.settings_btn]:
            layout_menu.addWidget(btn)

        layout_menu.addStretch()
        self.side_menu.setLayout(layout_menu)

        # Заголовок
        self.title_bar = TitleBar(self)

        # Контент справа
        self.content = QLabel("Привет! Это окно с **боковой панелью**, которая всегда видна.")
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Объединяем боковую панель и контент
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.side_menu)
        content_layout.addWidget(self.content)

        # Общий layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.title_bar)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        # Разворачиваем окно на весь экран
        screen_geometry = self.screen().availableGeometry()
        self.setGeometry(screen_geometry)

        # добавляем вкладки для всех агентов
        # for name, agent in self.agents.items():
        #    tab = self._create_agent_tab(agent, name)
        #    self.tabs.addTab(tab, name.capitalize())
        # self.setCentralWidget(self.tabs)


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
