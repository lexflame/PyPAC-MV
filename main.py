import sys, os
import tkinter as tk

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from core.loader import load_agents, AgentRegistry
from core.dashboard import Dashboard
from core.database import DatabaseManager
from core.eventbus import EventBus
from core.resolver import DependencyResolver

def main():
    print("=== Handler PyPAC-MV v0.5 starting ===")
    root = os.path.dirname(__file__)
    if root not in sys.path:
        sys.path.insert(0, root)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))
    db = DatabaseManager(os.path.join(root, "pypac.db"))
    eventbus = EventBus()
    agents = load_agents('agents')
    print(f"Загружено агентов: {len(agents)}")
    for name, meta in AgentRegistry.metadata.items():
        db.register_agent(name, meta.get('version', '1.0'))
    for name, agent in agents.items():
        if hasattr(agent, 'presentation'):
            setattr(agent.presentation, 'eventbus', eventbus)
        if hasattr(agent, 'abstraction'):
            setattr(agent.abstraction, 'eventbus', eventbus)
    resolver = DependencyResolver(AgentRegistry.metadata)
    cycles = resolver.detect_cycles()
    if cycles:
        print("[PyPAC-MV] ⚠ Dependency cycles detected:", cycles)
    dashboard = Dashboard(agents,AgentRegistry)
    dashboard.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
