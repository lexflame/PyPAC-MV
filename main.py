import importlib
import sys, os, builtins
from pathlib import Path

from rich import print, inspect

from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from core.context.global_context import GLC
from core.dashboard import Dashboard
from core.database import DatabaseManager
from core.eventbus import EventBus
from core.resolver import DependencyResolver
from core.loader import load_agents, AgentRegistry

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
        print('[PyPAC-MV IN] Инициализация базы данных')
        db = DatabaseManager(os.path.join(root, "db/base_app.db"))

        splash.showMessage("PyPAC-MV :: Запуск EventBus...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        print('[PyPAC-MV ST] Запуск EventBus')
        eventbus = EventBus()

        splash.showMessage("PyPAC-MV :: Загрузка агентов...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        print('[PyPAC-MV ST] Запуск агентов')
        agents = load_agents('agents')
        print(f"[PyPAC-MV OK] ✅ Загружено компонентов: {len(agents)}")

        splash.showMessage("PyPAC-MV :: Регистрация агентов в БД...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        print('[PyPAC-MV IN] Регистрация агентов')
        for name, meta in AgentRegistry.metadata.items():
            db.register_agent(name, meta.get('version', '1.0'))

        splash.showMessage("PyPAC-MV :: Настройка eventbus для агентов...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        print('[PyPAC-MV IN] Настройка eventbus')
        for name, agent in agents.items():
            if hasattr(agent, 'presentation'):
                setattr(agent.presentation, 'eventbus', eventbus)
            if hasattr(agent, 'abstraction'):
                setattr(agent.abstraction, 'eventbus', eventbus)

        splash.showMessage("PyPAC-MV :: Проверка зависимостей...",
                           Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                           Qt.GlobalColor.white)
        print('[PyPAC-MV ST] Проверка зависимостей')
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
        print(f"[PyPAC-MV ERROR] ❌ Ошибка при загрузке: {e}")
        splash.close()
        sys.exit(1)

    sys.exit(app.exec())

def scan_folder(path, recursive=True):
    path = Path(path)
    result = []

    if recursive:
        files = path.rglob("*")
    else:
        files = path.iterdir()

    for p in files:
        if p.is_file() and p.suffix != '.pyc':
            fclass = p.name.split('.')[0]
            inc = False
            if len(p.name.split('_')) > 2:
                inc = (f"_{p.name.split('_')[2].split('.')[0]}")
            arrName = fclass.split('_')
            NamecodeClass = '';
            arrPath = str(p.resolve()).split("\\")
            resolve = False
            import_path= '';
            for name in arrPath:
                if name == 'agents':
                    resolve = True
                if resolve:
                    valid_file = name.split('.')
                    if len(valid_file) == 1:
                        import_path += name + '.'
            for NameCode in arrName:
                NamecodeClass += NameCode.capitalize() + ''
            result.append({
                'name_class': NamecodeClass,
                'import_path': import_path + fclass,
                'include': inc,
                'file_class': fclass,
                'file_name': p.name,  # имя файла с расширением
                'file_path': str(p.resolve()), # полный путь к файлу
                'module': importlib.import_module(import_path + fclass),
            })

    return result


builtins.scan_folder = scan_folder

if __name__ == '__main__':
    main()