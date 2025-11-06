import sys, os
import builtins
import json
from rich import print

from core.context.global_context import GlobalContextClass

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
    app.setWindowIcon(QIcon("source/icon.png"))
    db = DatabaseManager(os.path.join(root, "db/base_app.db"))
    eventbus = EventBus()
    agents = load_agents('agents')
    print(f"Загружено компонентов: {len(agents)}")
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
def jq(obj):
    """Гибкий вывод для отладки (аналог jq/print_r)"""
    # Если это Qt объект — пытаемся извлечь полезное
    qt_type = type(obj).__name__
    qt_module = type(obj).__module__
    if qt_module.startswith("PyQt"):
        if hasattr(obj, "text"):
            print(f"<{qt_type} text='{obj.text()}' data={obj.data(256) if hasattr(obj, 'data') else None}>")
        elif hasattr(obj, "objectName"):
            print(f"<{qt_type} objectName='{obj.objectName()}'>")
        else:
            print(f"<{qt_type}>")
        return

    # Списки и словари — красиво форматируем
    if isinstance(obj, (dict, list, tuple, set)):
        try:
            print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))
            return
        except Exception:
            pass

    # Классы / инстансы — выводим их атрибуты
    if hasattr(obj, "__dict__"):
        attrs = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        print(f"[bold cyan]{obj.__class__.__name__}[/bold cyan]:")
        print(json.dumps(attrs, indent=2, ensure_ascii=False, default=str))
        return

    # Фоллбэк
    print(obj)

builtins.jq = jq

if __name__ == '__main__':
    main()
