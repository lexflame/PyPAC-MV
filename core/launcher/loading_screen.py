from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt6.QtGui import QPixmap, QLinearGradient, QPalette, QColor, QBrush
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtSignal

class LoadingScreen(QWidget):
    closed = pyqtSignal()  # событие "экран завершил работу"

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(640, 320)
        self._build_ui()
        self._apply_gradient_background()

    def _apply_gradient_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#3a3a3a"))
        gradient.setColorAt(1, QColor("#1e1e1e"))

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # ЛОГО СЛЕВА
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("source/icon.png").scaled(160, 160, Qt.KeepAspectRatio))
        layout.addWidget(self.logo)

        # Справа — прогресс и статус
        side = QVBoxLayout()
        layout.addLayout(side)

        self.status_label = QLabel("Запуск...")
        self.status_label.setAlignment(Qt.AlignRight)
        self.status_label.setStyleSheet("font-size: 16px; color: #ccc;")
        side.addWidget(self.status_label)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                background: #ccc;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #fff;
            }
        """)
        side.addWidget(self.progress)

    def set_status(self, text):
        self.status_label.setText(text)

    def set_progress(self, value):
        # плавная анимация прогресса
        anim = QPropertyAnimation(self.progress, b"value")
        anim.setDuration(250)
        anim.setStartValue(self.progress.value())
        anim.setEndValue(value)
        anim.start()
        self._anim = anim  # не дать GC удалить

    def closeEvent(self, event):
        self.closed.emit()
        return super().closeEvent(event)
