import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

class ItemTask(QWidget):
    def __init__(self, title, priority, deadline, list_item=None, complite_event=None, delete_event=None, data=None):
        super().__init__()
        self.is_complited_task = None
        self._list_item = list_item
        self._complite_event = complite_event
        self._delete_event = delete_event
        self.setupUi(title, priority, deadline, data)
        self.setStyleSheet(f"""QWidget {{color: #ddd;background-color: transparent !important;}}""")

    def setupUi(self, title, priority, deadline, data):

        self.box_item_layout = QHBoxLayout(self)
        self.box_item_layout.setContentsMargins(10, 10, 10, 10)  # Увеличили отступы
        self.box_item_layout.setSpacing(2)

        """ Область Drag&Drop === start """
        drag_label = QLabel()
        drag_label.setStyleSheet("border:1px solid red;")
        # === Кнопка перетаскивания ===
        icon = qta.icon("ei.check", color="#aaa")
        btn_check = QPushButton()
        btn_check.setIcon(icon)
        btn_check.setIconSize(QSize(24, 24))
        btn_check.setFixedSize(25, 25)
        btn_check.setToolTip('Выполнить')  # подсказка при наведении
        # Привязка клика к callback (если он передан)
        if self._complite_event is not None and self._list_item is not None:
            # передаем QListWidgetItem в контроллер
            btn_check.clicked.connect(lambda: self._complite_event(self._list_item))
        self.box_item_layout.addWidget(drag_label, stretch=1)
        """ Область Drag&Drop === end """

        header_label = QLabel()
        header_label.setStyleSheet("border:1px solid white;")
        self.box_item_layout.addWidget(header_label, stretch=25)

        action_label = QLabel()
        action_label.setStyleSheet("border:1px solid blue;")
        self.box_item_layout.addWidget(action_label, stretch=4)

