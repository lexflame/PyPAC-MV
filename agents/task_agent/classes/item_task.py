import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QListWidgetItem, QFrame, QLineEdit, QDateEdit, QComboBox
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QDate


class ItemTask(QWidget):
    def __init__(self, title, priority, deadline, list_item=None, complite_event=None, delete_event=None, data=None):
        super().__init__()
        self.is_complited_task = None
        self._list_item = list_item
        self._priority = priority
        self._complite_event = complite_event
        self._delete_event = delete_event
        self.setupUi(title, priority, deadline, list_item, data)
        self.setStyleSheet(f"""QWidget {{color: #ddd;background-color: transparent !important;}}""")

    def setupUi(self, title, priority, deadline, list_item, data):
        # --- ВЕРТИКАЛЬНЫЙ layout (весь контейнер) ---
        debug = False;
        header = QWidget(self)
        if debug:
            header.setStyleSheet("""QWidget {border: 2px solid red;background-color: rgba(0, 120, 212, 0.05);}""")
        vbox = QVBoxLayout(header)
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.setSpacing(2)

        # --- 1 горизонтальный блок ---
        item = QWidget()
        if debug:
            item.setStyleSheet("""QWidget {border: 2px solid orange;background-color: rgba(255, 69, 0, 0.05);}""")
        item_box = QHBoxLayout(item)
        priority_circle = self.create_priority_circle()
        item_box.setContentsMargins(5, 5, 5, 5)

        title_label = QLabel(f"{deadline} <b>{title}</b>")

         # отступ между кружком и текстом
        item_box.addWidget(title_label)
        item_box.addWidget(priority_circle)
        item_box.addSpacing(5)

        # Кнопка действия 'Подробности'
        icon = qta.icon("msc.more", color="#aaa")
        btn_more = QPushButton()
        btn_more.setIcon(icon)
        btn_more.setIconSize(QSize(24, 24))
        btn_more.setFixedSize(25, 25)
        btn_more.setFixedSize(25, 25)
        # btn_more.setStyleSheet("border:1px solid red;")
        btn_more.setToolTip('Подробности')
        btn_more.setMinimumSize(25, 25)
        btn_more.clicked.connect(self.toggle_desc)

        title_box = QHBoxLayout()
        title_box.setContentsMargins(0, 0, 0, 0)
        title_box.setSpacing(2)
        title_box.addWidget(title_label)
        title_box.addWidget(btn_more, alignment=Qt.AlignmentFlag.AlignVCenter)
        title_box.addStretch()

        title_widget = QWidget()
        title_widget.setLayout(title_box)

        action_bar = QWidget()
        btn_box = QHBoxLayout(action_bar)

        # Кнопка действия 'Редактировать'
        icon = qta.icon("fa5s.edit", color="#aaa")
        btn_edit = QPushButton()
        btn_edit.setIcon(icon)
        btn_edit.setIconSize(QSize(24, 24))
        btn_edit.setFixedSize(25, 25)
        btn_edit.setToolTip('Редактировать')
        btn_edit.clicked.connect(self.toggle_edit)

        # Кнопка действия 'Выполнить'
        icon = qta.icon("ei.check", color="#aaa")
        btn_check = QPushButton()
        btn_check.setIcon(icon)
        btn_check.setIconSize(QSize(24, 24))
        btn_check.setFixedSize(25, 25)
        btn_check.setToolTip('Выполнить')
        if self._complite_event is not None and self._list_item is not None:
            btn_check.clicked.connect(lambda: self._complite_event(self._list_item))

        # Кнопка действия 'Удалить'
        icon = qta.icon("mdi.delete", color="#aaa")
        btn_delete = QPushButton()
        btn_delete.setIcon(icon)
        btn_delete.setIconSize(QSize(24, 24))
        btn_delete.setFixedSize(25, 25)
        btn_delete.setToolTip('Удалить')
        if self._delete_event is not None and self._list_item is not None:
            btn_delete.clicked.connect(lambda: self._delete_event(self._list_item))

        btn_box.addWidget(btn_edit, stretch=1)
        btn_box.addWidget(btn_check, stretch=1)
        btn_box.addWidget(btn_delete, stretch=1)

        # Кнопка действия 'Драг'
        icon = qta.icon("fa6s.up-down", color="#aaa")
        btn_drag = QPushButton()
        btn_drag.setIcon(icon)
        btn_drag.setIconSize(QSize(24, 24))
        btn_drag.setFixedSize(25, 25)
        # btn_drag.setStyleSheet("border:1px solid red;")
        btn_drag.setToolTip('Перенести')
        btn_drag.setMinimumSize(25, 25)
        # btn_drag.clicked.connect(self.toggle_content)

        item_box.addWidget(btn_drag, stretch=1)
        item_box.addWidget(title_widget, stretch=25)
        item_box.addWidget(action_bar, stretch=4)

        # --- 2 горизонтальный блок ---
        self.desc = QWidget()
        self.desc.hide()
        if debug:
            desc.setStyleSheet("""QWidget {border: 2px solid #32CD32;background-color: rgba(50, 205, 50, 0.05);}""")
        desc_box = QVBoxLayout(self.desc)
        desc_box.setContentsMargins(5, 5, 5, 5)
        lang_map = {
            "high": "Высокий",
            "normal": "Нормальный",
            "low": "Низкий",
        }
        priority_desc = lang_map.get(priority, "Не указан")
        desc_box.addWidget(QLabel(f"<b>Название: {title}</b>"), stretch=4)
        desc_box.addWidget(QLabel(f"<b>Срок: {deadline}</b>"), stretch=4)
        desc_box.addWidget(QLabel(f"<b>Приоритет: {priority} {priority_desc}</b>"), stretch=4)

        # --- 3 горизонтальный блок ---
        self.edit = QWidget()
        self.edit.hide()
        if debug:
            self.edit.setStyleSheet("""QWidget {border: 2px solid blue;background-color: rgba(50, 205, 50, 0.05);}""")
        edit_box = QHBoxLayout(self.edit)
        edit_box.setContentsMargins(5, 5, 5, 5)
        self.edit.setStyleSheet("""QWidget {background-color: #3a3a3a;border-radius:5px;}""")


        self.title_edit_input = QLineEdit(title)
        self.title_edit_input.setPlaceholderText("Название задачи")
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        year, month, day = map(int, deadline.split("-"))
        self.due_date_edit.setDate(QDate(year, month, day))
        self.priority_edit = QComboBox()
        level_map = {
            "low": 0,
            "normal": 1,
            "high": 2,
        }
        level_index = int(level_map.get(priority, 1))
        self.priority_edit.addItems(["low", "normal", "high"])
        self.priority_edit.setCurrentIndex(level_index)

        edit_box.addWidget(self.title_edit_input, stretch=15)
        edit_box.addWidget(self.due_date_edit, stretch=4)
        edit_box.addWidget(self.priority_edit, stretch=4)


        # --- Добавляем горизонтальные блоки в вертикальный ---
        vbox.addWidget(item)
        vbox.addWidget(self.desc)
        vbox.addWidget(self.edit)

        # --- Основной layout окна ---
        root_layout = QVBoxLayout(self)
        root_layout.addWidget(header)

    def create_priority_circle(self):
        """Создаёт виджет-кружок для приоритета."""
        color_map = {
            "high": "#e74c3c",  # красный
            "normal": "#f1c40f",  # желтый
            "low": "#2ecc71",  # зеленый
        }
        color = color_map.get(self._priority, "#95a5a6")  # серый по умолчанию

        circle = QFrame()
        circle.setFixedSize(16, 16)  # размер кружка
        circle.setStyleSheet(f"border-radius: 8px; background-color: {color};")
        return circle

    def toggle_edit(self):

        if self.desc.isVisible():
            self.desc.hide()

        visible = self.edit.isVisible()
        self.edit.setVisible(not visible)
        self.animate_size_change_edit(expanding=not visible)

    def toggle_desc(self):

        if self.edit.isVisible():
            self.edit.hide()

        visible = self.desc.isVisible()
        self.desc.setVisible(not visible)
        self.animate_size_change_desc(expanding=not visible)

    def animate_size_change_desc(self, expanding=True):
        """Плавно изменяет высоту ItemTask при раскрытии/сворачивании."""
        start_height = self.height()
        # Получаем новую целевую высоту
        end_height = self.sizeHint().height()

        anim = QPropertyAnimation(self, b"maximumHeight")
        anim.setDuration(250)
        anim.setStartValue(start_height)
        anim.setEndValue(end_height)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.start()
        # Сохраняем, чтобы GC не уничтожил
        self._anim = anim
        # После завершения обновляем item в QListWidget
        def on_finished():
            if self._list_item:
                self._list_item.setSizeHint(self.sizeHint())
            # self.setMaximumHeight(16777215)  # сбросить ограничение высоты
        anim.finished.connect(on_finished)
        anim.finished.connect(on_finished)

    def animate_size_change_edit(self, expanding=True):
        """Плавно изменяет высоту ItemTask при раскрытии/сворачивании."""
        start_height = self.height()
        # Получаем новую целевую высоту
        end_height = self.sizeHint().height()

        anim = QPropertyAnimation(self, b"maximumHeight")
        anim.setDuration(250)
        anim.setStartValue(start_height)
        anim.setEndValue(end_height)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.start()
        # Сохраняем, чтобы GC не уничтожил
        self._anim = anim
        # После завершения обновляем item в QListWidget
        def on_finished():
            if self._list_item:
                self._list_item.setSizeHint(self.sizeHint())
            # self.setMaximumHeight(16777215)  # сбросить ограничение высоты
        anim.finished.connect(on_finished)
        anim.finished.connect(on_finished)





