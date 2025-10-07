
from PyQt6.QtWidgets import QApplication
from core.loader import load_agents
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    agents = load_agents('agents')
    for a in agents.values():
        a.show()
    sys.exit(app.exec())
