from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from views.window.resources import TITLE_BAR_BG, BUTTON_BG, BUTTON_HOVER, CLOSE_BUTTON_BG, CLOSE_BUTTON_HOVER, FONT_COLOR, APP_TITLE

class TitleBar(QWidget):
    def __init__(self, parent, toggle_menu_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.toggle_menu_callback = toggle_menu_callback
        self.setFixedHeight(40)
        self.setStyleSheet(f"background-color: {TITLE_BAR_BG}; color: {FONT_COLOR}; ")
        self.old_pos = None

        # Гамбургер
        self.btn_menu = QPushButton("☰")
        self.btn_menu.setFixedSize(45, 45)
        self.btn_menu.setStyleSheet(f"""
            QPushButton {{
                background-color: {BUTTON_BG};
                border: 0.5px solid black;
                font-weight: bold;
                color: {FONT_COLOR};
            }}
            QPushButton:hover {{
                background-color: {BUTTON_HOVER};
            }}
        """)
        self.btn_menu.clicked.connect(self.toggle_menu)

        # Название окна
        self.title = QLabel(f"{APP_TITLE}")
        self.title.setStyleSheet("padding-left: 5px;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        # Кнопки управления окном
        self.btn_min = QPushButton("—")
        self.btn_max = QPushButton("▢")
        self.btn_close = QPushButton("✕")
        self.setup_buttons()

        # Лэйаут заголовка
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.btn_menu)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_close)
        self.setLayout(layout)

        self.is_maximized = False

    def setup_buttons(self):
        for btn in (self.btn_min, self.btn_max):
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {BUTTON_BG};
                    border: none;
                    font-weight: bold;
                    color: {FONT_COLOR};
                }}
                QPushButton:hover {{
                    background-color: {BUTTON_HOVER};
                }}
            """)
        self.btn_close.setFixedSize(40, 40)
        self.btn_close.setStyleSheet(f"""
            QPushButton {{
                background-color: {CLOSE_BUTTON_BG};
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {CLOSE_BUTTON_HOVER};
            }}
        """)

        self.btn_min.clicked.connect(self.parent.showMinimized)
        self.btn_max.clicked.connect(self.toggle_max_restore)
        self.btn_close.clicked.connect(self.parent.close)

    def toggle_max_restore(self):
        if self.is_maximized:
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
        self.is_maximized = not self.is_maximized

    def toggle_menu(self):
        if self.toggle_menu_callback:
            self.toggle_menu_callback()

    # Перетаскивание окна
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            new_x = max(0, self.parent.x() + delta.x())
            new_y = max(0, self.parent.y() + delta.y())
            self.parent.move(new_x, new_y)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
