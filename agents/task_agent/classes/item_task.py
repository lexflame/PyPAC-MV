import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal

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
        self.setMinimumHeight(70)
        self.setMaximumHeight(80)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # Основной горизонтальный макет
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 20, 8)  # Увеличили отступы

        layout.setSpacing(2)  # Расстояние между элементами

        # Левая часть: текст задачи
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)  # Убираем внешние отступы
        text_layout.setSpacing(0) # Маленький зазор между элементами

        text_layout = QVBoxLayout()

        priority_label = ""
        if(priority == 'low'):
            priority_label = "low"
        if (priority == 'normal'):
            priority_label = "normal"
        if (priority == 'high'):
            priority_label = "high"

        box_label = QLabel(f" {priority_label} {deadline} {title}")
        box_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        box_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        text_layout.addWidget(box_label)

        title_label = QLabel(f"<b></b>")
        title_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Кнопка действия 'Подробности'
        icon = qta.icon("msc.more", color="#aaa")
        btn_more = QPushButton()
        btn_more.setIcon(icon)
        btn_more.setIconSize(QSize(24, 24))
        btn_more.setFixedSize(25, 25)
        btn_more.setToolTip('Подробности')  # подсказка при наведении
        btn_more.setMinimumSize(25, 25)

        text_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        text_layout.setSpacing(0)
        text_layout.addWidget(title_label)
        text_layout.addWidget(btn_more, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignLeft)

        # Добавляем в основной макет
        layout.addLayout(text_layout, 1)  # Вес 1 (растягивается)

        # Кнопка действия 'Выполнить'
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

        # Кнопка действия 'Редактировать'
        icon = qta.icon("fa5s.edit", color="#aaa")
        btn_edit = QPushButton()
        btn_edit.setIcon(icon)
        btn_edit.setIconSize(QSize(24, 24))
        btn_edit.setFixedSize(25, 25)
        btn_edit.setToolTip('Редактировать')  # подсказка при наведении

        # Кнопка действия 'Удалить'
        icon = qta.icon("mdi.delete", color="#aaa")
        btn_delete = QPushButton()
        btn_delete.setIcon(icon)
        btn_delete.setIconSize(QSize(24, 24))
        btn_delete.setFixedSize(25, 25)
        btn_delete.setToolTip('Удалить')  # подсказка при наведении

        # Привязка клика к callback (если он передан)

        if self._delete_event is not None and self._list_item is not None:
            # передаем QListWidgetItem в контроллер
            btn_delete.clicked.connect(lambda: self._delete_event(self._list_item))

        # Устанавливаем минимальный размер для виджета
        self.setMinimumHeight(60)
        layout.addWidget(btn_edit, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignRight)  # Вес 0 (фиксированный размер)
        layout.addWidget(btn_check, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignRight)  # Вес 0 (фиксированный размер)
        layout.addWidget(btn_delete, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignRight)  # Вес 0 (фиксированный размер)