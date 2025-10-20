from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QStyleFactory
import qtawesome as qta


class UiStyle:
    """Применяет ночной стиль и подключает qtawesome-иконки."""

    def __init__(self, app: QApplication, font_family="Segoe UI", font_size=10):
        self.app = app
        self.font_family = font_family
        self.font_size = font_size

        self.apply_dark_theme()
        self.apply_font()
        self.icons = self.load_icons()

    def apply_dark_theme(self):
        """Создаёт и применяет тёмную палитру."""
        dark_palette = QPalette()

        dark_color = QColor(45, 45, 45)
        disabled_color = QColor(127, 127, 127)
        text_color = QColor(220, 220, 220)
        accent_color = QColor(0, 122, 204)

        dark_palette.setColor(QPalette.ColorRole.Window, dark_color)
        dark_palette.setColor(QPalette.ColorRole.WindowText, text_color)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, dark_color)
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, text_color)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, text_color)
        dark_palette.setColor(QPalette.ColorRole.Text, text_color)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(55, 55, 55))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, text_color)
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, accent_color)

        dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled_color)
        dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, disabled_color)

        self.app.setPalette(dark_palette)
        self.app.setStyle(QStyleFactory.create("Fusion"))

    def apply_font(self):
        """Устанавливает системный шрифт."""
        self.app.setStyleSheet(f"""
            QWidget {{
                font-family: '{self.font_family}';
                font-size: {self.font_size}pt;
                color: #ddd;
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                                 stop:0 #1a1a1a, stop:1 #2a2a2a);
            }}
            QPushButton {{
                background-color: #3a3a3a;
                border: 1px solid #555;
                padding: 6px 12px;
                border-radius: 0px;
            }}
            QPushButton:hover {{
                background-color: #4a4a4a;
            }}
            QLineEdit, QTextEdit {{
                background-color: #1e1e1e;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 4px;
            }}
        """)

    def load_icons(self):
        """Создаёт словарь qtawesome-иконок для быстрого доступа."""
        return {
            "add": qta.icon("fa5s.plus-circle", color="#4caf50"),
            "edit": qta.icon("ei.edit", color="#ffc107"),
            "delete": qta.icon("fa5.trash-alt", color="#f44336"),
            "save": qta.icon("fa5.save", color="#00bcd4"),
            "settings": qta.icon("mdi.cog-box", color="#9e9e9e"),
            "sync": qta.icon("mdi6.refresh-circle", color="#03a9f4"),
            "task": qta.icon("fa5.check-square", color="#8bc34a"),
        }

