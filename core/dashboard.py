import qtawesome as qta

from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QSizePolicy, QStackedWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap

from config.theme.ui_style import UiStyle
from core.loader import AgentRegistry

from views.window.title_bar import TitleBar
from views.window.resources import (APP_TITLE)

class Dashboard(QWidget):
    def __init__(self, agents, AgentRegistry):
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
            """todo добавить переход на tab соответствующий агенту """
            item_btn = self._make_icon_button(meta.get('icon', 'fa5s.cog'), name)
            layout_menu.addWidget(item_btn)

        """Добавляем область работы для проектов и ЧТО_ТО ЕЩЕ"""
        self.nav_project = QTabWidget()
        self.nav_project.setFixedWidth(250)
        self.nav_project.setDocumentMode(True)

        self.nav_project.widget = QWidget()
        layout = QVBoxLayout(self.nav_project.widget)
        project = self._create_agent_tab(self.nav_project.widget, 'project')
        label = 'Проекты'
        self.nav_project.addTab(project, label)

        """Получаем табы для агентов"""
        self.registry = AgentRegistry
        """ normalize agents to ordered list of (name, agent) """
        self.agents_map = {}
        if isinstance(agents, dict):
            for k, v in agents.items():
                self.agents_map[k] = v
        elif isinstance(agents, (list, tuple)):
            for a in agents:
                # try to determine name
                name = (getattr(a, 'name', None)
                        or (getattr(a, 'presentation', None)
                            and getattr(a.presentation, 'windowTitle', None)
                            and a.presentation.windowTitle()) or str(id(a)))
                self.agents_map[name] = a
        else:
            raise ValueError("Unsupported agents type")

        """ get metadata mapping """
        self.meta = {}
        if AgentRegistry is not None:
            if hasattr(AgentRegistry, 'metadata'):
                self.meta = AgentRegistry.metadata
            elif hasattr(AgentRegistry, 'get_metadata'):
                try:
                    self.meta = AgentRegistry.get_metadata()
                except Exception:
                    self.meta = {}

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

        """Выводим табы агентов"""
        """BEGIN"""

        """END"""

        content_layout.addWidget(self.side_menu)
        content_layout.addWidget(self.nav_project)
        #content_layout.addWidget(self.tabs)

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

    def _ordered_agents(self):
        # return list of tuples (name, agent) ordered by meta 'order' if present
        items = list(self.agents_map.items())
        def order_key(item):
            name, agent = item
            meta = self.meta.get(name, {})
            return meta.get('order', 1000)
        items.sort(key=order_key)
        return items

    def switch_to_agent(self, agent_name):
        # switch to tab corresponding to agent_name
        ordered = self._ordered_agents()
        for idx, (name, _) in enumerate(ordered):
            if name == agent_name:
                self.switch_to_index(idx)
                return True
        return False

    def switch_to_index(self, index):
        # update buttons checked state
        for btn in self.btn_map.values():
            btn.setChecked(False)
        # find name for index
        ordered = self._ordered_agents()
        if 0 <= index < len(ordered):
            name = ordered[index][0]
            btn = self.btn_map.get(name)
            if btn:
                btn.setChecked(True)
        self.stack.setCurrentIndex(index)

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
