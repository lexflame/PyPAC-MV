import sys, os, builtins, json, traceback, inspect, importlib
from pathlib import Path
from rich import print

from core.context.global_context import GlobalContextClass
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

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

def scan_folder_inc(path, recursive=True):
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
                'import_path': import_path,
                'include': inc,
                'file_class': fclass,
                'file_name': p.name,  # имя файла с расширением
                'file_path': str(p.resolve()), # полный путь к файлу
            })

    return result


def initedClasses(classes):

    trace = traceback.extract_stack()
    stack_func = inspect.stack()
    path = {}

    caller_frame = trace[-2]
    stack_frame = stack_func[1]

    script_name = os.path.basename(caller_frame.filename).split('.')[0]
    module = inspect.getmodule(inspect.stack()[1].frame)
    module_path_import = module.__name__ if module else "unknown"
    path['import_from'] = {}
    path['import_from']['classes'] = (f"{module_path_import}.{script_name}_classes")
    path['import_from']['file'] = (f"{stack_func[1].filename.replace((f"{script_name}.py"), "")}{script_name}_classes")
    files = scan_folder_inc(path['import_from']['file'], recursive=True)
    for file_item in files:
        full_import_class = (f"{file_item['import_path']}{file_item['file_class']}")
        if file_item['include'] != False:
            param_name = file_item['include']
            value_name = file_item['name_class']
            try:
                module_path = (f"{file_item['import_path']}{file_item['file_class']}")
                module = importlib.import_module(module_path)
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    """"""""""""""
                    """ TODOOO """
                    """"""""""""""
            except ImportError as e:
                raise ImportError(f"Не удалось импортировать модуль {module_path}: {e}")
            try:
                class_name = file_item['name_class']
                class_obj = getattr(module, class_name)
            except AttributeError:
                raise AttributeError(f"Класс {class_name} не найден в модуле {module_path}")
            instance = class_obj(classes)
            setattr(classes, param_name, instance)
        print(file_item)

builtins.jq = jq
builtins.initedClasses = initedClasses
builtins.scan_folder_inc = scan_folder_inc

if __name__ == '__main__':
    main()
