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
        self.setMinimumHeight(70)
        self.setMaximumHeight(80)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # Основной горизонтальный макет
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)  # Увеличили отступы
        layout.setSpacing(2)  # Расстояние между элементами
        # Левая часть: текст задачи
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(2, 2, 2, 2)  # Убираем отступы
        text_layout.setSpacing(2)
        # --- цвет квадратика в зависимости от приоритета ---
        color_map = {
            "low": "#4CAF50",  # зелёный
            "normal": "#FFC107",  # жёлтый
            "high": "#F44336"  # красный
        }
        color = color_map.get(priority, "#9E9E9E")  # серый по умолчанию
        # --- QLabel-квадратик ---
        priority_label = QLabel()
        priority_label.setWordWrap(False)  # отключаем перенос
        priority_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        priority_label.setFixedSize(12, 12)  # квадрат 12x12 px
        priority_label.setStyleSheet(f"background-color: {color}; border-radius: 3px;")
        # --- заголовок задачи ---
        title_label = QLabel(title)
        title_label.setWordWrap(False)
        title_label.setFixedSize(400, 20)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        title_label.setStyleSheet("float:left;font-weight: bold;border:1px solid #ddd;")
        # Область 'Подробности'
        desc_title_input = QLabel(f"Подробности: {priority_label} {deadline} {title}")
        content_layout = QVBoxLayout()
        content_layout.addWidget(desc_title_input)
        self.content_widget = QWidget()
        self.content_widget.setLayout(content_layout)
        self.content_widget.setVisible(False)
        self.content_widget.setMaximumHeight(0)
        self.content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.content_widget.setFixedWidth(int(self.width() * 0.8))
        # Кнопка действия 'Подробности'
        icon = qta.icon("msc.more", color="#aaa")
        btn_more = QPushButton()
        btn_more.setIcon(icon)
        btn_more.setIconSize(QSize(24, 24))
        btn_more.setFixedSize(25, 25)
        btn_more.setFixedSize(25, 25)
        btn_more.setStyleSheet("border:1px solid red;")
        btn_more.setToolTip('Подробности')  # подсказка при наведении
        btn_more.setMinimumSize(25, 25)
        btn_more.clicked.connect(self.toggle_content)
        # встроим виджеты в text_layout
        text_layout.addWidget(priority_label)
        text_layout.addWidget(title_label)
        text_layout.addWidget(btn_more)
        # Добавляем в основной макет
        layout.addLayout(text_layout, 0)  # Вес 1 (растягивается)
        # Кнопка действия 'Редактировать'
        icon = qta.icon("fa5s.edit", color="#aaa")
        btn_edit = QPushButton()
        btn_edit.setIcon(icon)
        btn_edit.setIconSize(QSize(24, 24))
        btn_edit.setFixedSize(25, 25)
        btn_edit.setToolTip('Редактировать')  # подсказка при наведении
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
        layout.addWidget(self.content_widget, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(btn_edit, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignRight)  # Вес 0 (фиксированный размер)
        layout.addWidget(btn_check, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignRight)  # Вес 0 (фиксированный размер)
        layout.addWidget(btn_delete, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignRight)  # Вес 0 (фиксированный размер)
        layout.addWidget(self.content_widget)

    def toggle_content(content_widget=None):
        if content_widget.isVisible():
            # Скрыть
            anim = QPropertyAnimation(content_widget, b"maximumHeight")
            anim.setDuration(200)
            anim.setStartValue(content_widget.height())
            anim.setEndValue(0)
            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            anim.start()
            content_widget.setVisible(False)
        else:
            # Показать
            content_widget.setVisible(True)
            content_widget.setMaximumHeight(0)
            anim = QPropertyAnimation(content_widget, b"maximumHeight")
            anim.setDuration(200)
            anim.setStartValue(0)
            anim.setEndValue(content_widget.sizeHint().height())
            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            anim.start()