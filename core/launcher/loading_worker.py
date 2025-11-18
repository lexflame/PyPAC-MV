from PyQt6.QtCore import QObject, QThread, pyqtSignal
import time, os, sys

from core.dashboard import Dashboard

class LoadingWorker(QObject):
    progress = pyqtSignal(int)          # 0–100 %
    status = pyqtSignal(str)            # текст шага
    finished = pyqtSignal(dict)         # результат загрузки

    def run(self):
        """Выполняет реальные шаги загрузки приложения."""

        self.result = {}
        # ---------- Шаг 1 ----------
        self.status.emit("=== Handler PyPAC-MV v0.5 starting ===")
        self.status.emit("Инициализация базы данных...")
        QThread.msleep(200)
        self.progress.emit(10)

        from core.database import DatabaseManager
        self.result["db"] = DatabaseManager(os.path.join(os.getcwd(), "db/base_app.db"))
        self.progress.emit(20)

        # ---------- Шаг 2 ----------
        self.status.emit("Запуск EventBus...")
        from core.eventbus import EventBus
        self.result["eventbus"] = EventBus()
        QThread.msleep(200)
        self.progress.emit(35)

        # ---------- Шаг 3 ----------
        self.status.emit("Загрузка агентов...")
        from core.loader import load_agents, AgentRegistry
        self.result["agents"] = load_agents("agents")
        print(f"Загружено компонентов: {len(self.result["agents"])}")
        self.status.emit(f"Загружено компонентов: {len(self.result["agents"])}")
        QThread.msleep(200)
        self.progress.emit(55)

        # ---------- Шаг 4 ----------
        self.status.emit("Регистрация метаданных агентов...")
        for name, meta in AgentRegistry.metadata.items():
            self.result["db"].register_agent(name, meta.get("version", "1.0"))
        for name, agent in self.result["agents"].items():
            if hasattr(agent, 'presentation'):
                setattr(agent.presentation, 'eventbus', self.result["eventbus"])
            if hasattr(agent, 'abstraction'):
                setattr(agent.abstraction, 'eventbus', self.result["eventbus"])
        QThread.msleep(200)
        self.progress.emit(70)

        # ---------- Шаг 5 ----------
        self.status.emit("Настройка зависимостей...")
        from core.resolver import DependencyResolver
        resolver = DependencyResolver(AgentRegistry.metadata)
        resolver.detect_cycles()
        QThread.msleep(200)
        self.progress.emit(85)

        # ---------- Шаг 6 ----------
        self.status.emit("Подготовка интерфейса...")
        self.progress.emit(95)
        self.status.emit("Вход...")
        QThread.msleep(200)
        self.progress.emit(100)



        self.finished.emit(self.result)
