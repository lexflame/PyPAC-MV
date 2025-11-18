import sys, os
import builtins
import json
from rich import print

from core.context.global_context import GlobalContextClass
from PyQt6.QtWidgets import QApplication, QSplashScreen, QGraphicsColorizeEffect, QGraphicsDropShadowEffect
from PyQt6.QtGui import QIcon, QPixmap, QColor
from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation

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

    # 1. Создаём splash screen
    splash_pix = QPixmap(QPixmap("source/splash.png").scaled(642, 295, Qt.KeepAspectRatio))  # укажите путь к вашему изображению
    splash = QSplashScreen(splash_pix)

    # Настройка внешнего вида заставки
    splash.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    splash.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # Показываем заставку
    splash.show()
    app.processEvents()  # обрабатываем события, чтобы заставка отобразилась

    try:
        # 2. Пошаговая загрузка с обновлением статуса
        splash.showMessage("Handler PyPAC-MV v0.5 starting - Инициализация базы данных...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        db = DatabaseManager(os.path.join(root, "db/base_app.db"))

        splash.showMessage("PyPAC-MV :: Запуск EventBus...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        eventbus = EventBus()

        splash.showMessage("PyPAC-MV :: Загрузка агентов...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        agents = load_agents('agents')
        print(f"PyPAC-MV :: Загружено компонентов: {len(agents)}")

        splash.showMessage("PyPAC-MV :: Регистрация агентов в БД...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        for name, meta in AgentRegistry.metadata.items():
            db.register_agent(name, meta.get('version', '1.0'))

        splash.showMessage("PyPAC-MV :: Настройка eventbus для агентов...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        for name, agent in agents.items():
            if hasattr(agent, 'presentation'):
                setattr(agent.presentation, 'eventbus', eventbus)
            if hasattr(agent, 'abstraction'):
                setattr(agent.abstraction, 'eventbus', eventbus)

        splash.showMessage("PyPAC-MV :: Проверка зависимостей...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        resolver = DependencyResolver(AgentRegistry.metadata)
        cycles = resolver.detect_cycles()
        if cycles:
            print("[PyPAC-MV] ⚠ Dependency cycles detected:", cycles)

        # 3. Показываем главное окно и скрываем splash
        dashboard = Dashboard(agents, AgentRegistry)

        # Плавное скрытие splash (опционально)
        splash.finish(dashboard)
        dashboard.show()

    except Exception as e:
        print(f"[ERROR] Ошибка при загрузке: {e}")
        splash.close()
        sys.exit(1)

    sys.exit(app.exec())


def jq(obj):
    """Гибкий вывод для отладки (аналог jq/print_r)"""
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

    if isinstance(obj, (dict, list, tuple, set)):
        try:
            print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))
            return
        except Exception:
            pass

    if hasattr(obj, "__dict__"):
        attrs = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        print(f"[bold cyan]{obj.__class__.__name__}[/bold cyan]:")
        print(json.dumps(attrs, indent=2, ensure_ascii=False, default=str))
        return

    print(obj)


builtins.jq = jq

if __name__ == '__main__':
    main()
