# core/launcher/loading_worker.py
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import time
import os

class LoadingWorker(QObject):
    progress = pyqtSignal(int)          # 0–100 %
    status = pyqtSignal(str)            # текст шага
    finished = pyqtSignal(dict)         # результат загрузки

    def run(self):
        """Выполняет реальные шаги загрузки приложения."""

        result = {}

        # ---------- Шаг 1 ----------
        self.status.emit("Инициализация базы данных...")
        time.sleep(0.4)
        self.progress.emit(10)

        from core.database import DatabaseManager
        result["db"] = DatabaseManager(os.path.join(os.getcwd(), "db/base_app.db"))
        self.progress.emit(20)

        # ---------- Шаг 2 ----------
        self.status.emit("Запуск EventBus...")
        from core.eventbus import EventBus
        result["eventbus"] = EventBus()
        time.sleep(0.3)
        self.progress.emit(35)

        # ---------- Шаг 3 ----------
        self.status.emit("Загрузка агентов...")
        from core.loader import load_agents, AgentRegistry
        result["agents"] = load_agents("agents")
        time.sleep(0.4)
        self.progress.emit(55)

        # ---------- Шаг 4 ----------
        self.status.emit("Регистрация метаданных агентов...")
        for name, meta in AgentRegistry.metadata.items():
            result["db"].register_agent(name, meta.get("version", "1.0"))
        time.sleep(0.3)
        self.progress.emit(70)

        # ---------- Шаг 5 ----------
        self.status.emit("Настройка зависимостей...")
        from core.resolver import DependencyResolver
        resolver = DependencyResolver(AgentRegistry.metadata)
        resolver.detect_cycles()
        time.sleep(0.3)
        self.progress.emit(85)

        # ---------- Шаг 6 ----------
        self.status.emit("Подготовка интерфейса...")
        time.sleep(0.3)
        self.progress.emit(100)

        self.finished.emit(result)
