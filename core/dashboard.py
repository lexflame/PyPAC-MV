from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QSizePolicy, QStackedWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap

from config.theme.ui_style import UiStyle
from core.loader import AgentRegistry

from views.window.title_bar import TitleBar
from views.window.resources import (APP_TITLE)

class Dashboard(QWidget):
    def __init__(self, agents: dict, AgentRegistry):

        """
        Dashboard принимает agents и опционально registry.
        - agents может быть dict {name: agent} или list of agent instances.
        - registry может иметь attribute 'metadata' (dict) или метод get_metadata().
        """

        super().__init__()
        style = UiStyle(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


        self.registry = AgentRegistry
        # normalize agents to ordered list of (name, agent)
        self.agents_map = {}
        if isinstance(agents, dict):
            for k, v in agents.items():
                self.agents_map[k] = v
        elif isinstance(agents, (list, tuple)):
            for a in agents:
                # try to determine name
                name = getattr(a, 'name', None) or (getattr(a, 'presentation', None) and getattr(a.presentation, 'windowTitle', None) and a.presentation.windowTitle()) or str(id(a))
                self.agents_map[name] = a
        else:
            raise ValueError("Unsupported agents type")

        # get metadata mapping
        self.meta = {}
        if AgentRegistry is not None:
            if hasattr(AgentRegistry, 'metadata'):
                self.meta = AgentRegistry.metadata
            elif hasattr(AgentRegistry, 'get_metadata'):
                try:
                    self.meta = AgentRegistry.get_metadata()
                except Exception:
                    self.meta = {}
        # build UI
        self.setWindowTitle("MindNavigator")
        #self.resize(1000, 700)

        main_layout = QHBoxLayout(self)
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)

        # side menu
        self.side_menu = QFrame()

        self.side_menu.setFixedWidth(72)
        self.side_menu.setObjectName("side_menu")
        side_layout = QVBoxLayout(self.side_menu)
        side_layout.setContentsMargins(6, 6, 6, 6)
        side_layout.setSpacing(8)
        # central area with tabs (stacked)
        self.stack = QStackedWidget()
        # determine order
        ordered = self._ordered_agents()
        self.btn_map = {}
        for idx, (name, agent) in enumerate(ordered):
            meta = self.meta.get(name, {})
            title = meta.get('title', name)
            icon_text = meta.get('icon', None)
            # create tab content
            content = QWidget()
            content_layout = QVBoxLayout(content)
            # prefer agent.presentation.widget or centralWidget()
            w = None
            if hasattr(agent, 'presentation') and hasattr(agent.presentation, 'widget'):
                w = agent.presentation.widget
            else:
                # try centralWidget() if available
                try:
                    cw = agent.presentation.centralWidget() if hasattr(agent.presentation, 'centralWidget') else None
                    w = cw
                except Exception:
                    w = None
            if w is not None:
                content_layout.addWidget(w)
            else:
                content_layout.addWidget(QLabel(f"Agent {title} has no view"))
            self.stack.addWidget(content)
            # create side button
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setToolTip(title)
            btn.setFixedSize(56, 56)
            if icon_text:
                btn.setText(icon_text)
            btn.clicked.connect(lambda _, i=idx: self.switch_to_index(i))
            side_layout.addWidget(btn)
            self.btn_map[name] = btn
        side_layout.addStretch()
        main_layout.addWidget(self.side_menu)
        main_layout.addWidget(self.stack, 1)

        # default select first
        if self.stack.count() > 0:
            self.switch_to_index(0)

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
