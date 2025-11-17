# main.py
import sys, os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from core.launcher.loading_screen import LoadingScreen
from core.launcher.loading_worker import LoadingWorker
from core.loader import AgentRegistry
from core.dashboard import Dashboard

from PyQt6.QtCore import QThread

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("source/icon.png"))

    # ---- Экран загрузки ----
    loading = LoadingScreen()
    loading.show()

    # ---- Запуск потока загрузки ----
    thread = QThread()
    worker = LoadingWorker()
    worker.moveToThread(thread)

    worker.progress.connect(loading.set_progress)
    worker.status.connect(loading.set_status)

    def finished(data):
        loading.close()

        # создаём Dashboard после загрузки
        dashboard = Dashboard(data["agents"], AgentRegistry)
        dashboard.show()

    worker.finished.connect(finished)

    thread.started.connect(worker.run)
    thread.start()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
