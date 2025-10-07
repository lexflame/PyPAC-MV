import sys
from PyQt6.QtWidgets import QApplication
from core.loader import load_agents, AgentRegistry
from core.dashboard import Dashboard
from core.database import DatabaseManager

def main():
    print("=== PyPAC-MV starting ===")

    # Логика
    app = QApplication(sys.argv)

    # 🗃 инициализация базы данных
    db = DatabaseManager("pypac.db")

    # 🔍 загрузка агентов
    agents = load_agents('agents')

    print(f"Загружено агентов: {len(agents)}")
    for name, meta in AgentRegistry.metadata.items():
        print(f" - {name} ({meta.get('version', '1.0')}) (icon: {meta.get('icon', '1.0')})")
        db.register_agent(name, meta.get('version', '1.0'))

    # 🧭 создаём Dashboard
    dashboard = Dashboard(agents, AgentRegistry)
    dashboard.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
