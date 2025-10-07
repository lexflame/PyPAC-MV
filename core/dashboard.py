from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class Dashboard(QMainWindow):
    """Главное окно PyPAC-MV — отображает всех агентов как вкладки."""

    def __init__(self, agents: dict):
        super().__init__()
        self.agents = agents
        self.setWindowTitle("PyPAC-MV Dashboard")
        self.setGeometry(200, 100, 800, 600)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setDocumentMode(True)

        # добавляем вкладки для всех агентов
        for name, agent in self.agents.items():
            tab = self._create_agent_tab(agent, name)
            self.tabs.addTab(tab, name.capitalize())

        self.setCentralWidget(self.tabs)

    def _create_agent_tab(self, agent, name):
        """Создаёт вкладку для агента."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        if hasattr(agent, 'presentation') and hasattr(agent.presentation, 'widget'):
            layout.addWidget(agent.presentation.widget)
        else:
            layout.addWidget(QLabel(f"⚠️ Агент {name} не имеет представления", alignment=Qt.AlignmentFlag.AlignCenter))

        return widget
