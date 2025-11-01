from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
import qtawesome as qta

class ItemTask(QWidget):
    def __init__(self, title, priority, deadline, list_item=None, complite_event=None, delete_event=None, data=None):
        super().__init__()
        self._list_item = list_item
        self._complite_event = complite_event
        self._delete_event = delete_event
        self.anim = None
        self.setupUi(title, priority, deadline, data)
        self.setStyleSheet("QWidget { color: #ddd; background-color: transparent !important; }")

    def setupUi(self, title, priority, deadline, data):
        # Основной вертикальный макет
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 8, 20, 8)
        self.main_layout.setSpacing(5)

        # Горизонтальная верхняя строка с основной информацией и кнопками
        top_layout = QHBoxLayout()
        top_layout.setSpacing(5)

        # Левая часть: текст задачи
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        priority_label = "<span style='background-color: #ddd; color: white;></span>"
        # if(priority == 'low'):
            #priority_label = ""
        # if (priority == 'normal'):
            #priority_label = ""
        # if (priority == 'high'):
            #priority_label = ""
        # priority_label = f"'/>{priority_label}</span>"

        box_label = QLabel(f"{priority_label} {title}")
        box_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        text_layout.addWidget(box_label)

        # Кнопка 'Подробности'
        btn_more = QPushButton()
        btn_more.setIcon(qta.icon("msc.more", color="#aaa"))
        btn_more.setIconSize(QSize(24, 24))
        btn_more.setFixedSize(25, 25)
        btn_more.setToolTip('Подробности')
        btn_more.clicked.connect(self.toggle_content)
        text_layout.addWidget(btn_more, alignment=Qt.AlignmentFlag.AlignLeft)

        top_layout.addLayout(text_layout, stretch=1)

        # Кнопки справа
        btn_check = QPushButton()
        btn_check.setIcon(qta.icon("ei.check", color="#aaa"))
        btn_check.setFixedSize(25, 25)
        if self._complite_event and self._list_item:
            btn_check.clicked.connect(lambda: self._complite_event(self._list_item))

        btn_edit = QPushButton()
        btn_edit.setIcon(qta.icon("fa5s.edit", color="#aaa"))
        btn_edit.setFixedSize(25, 25)

        btn_delete = QPushButton()
        btn_delete.setIcon(qta.icon("mdi.delete", color="#aaa"))
        btn_delete.setFixedSize(25, 25)
        if self._delete_event and self._list_item:
            btn_delete.clicked.connect(lambda: self._delete_event(self._list_item))

        for btn in [btn_edit, btn_check, btn_delete]:
            top_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(top_layout)

        # Раскрывающаяся область
        self.content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(5,5,5,5)
        content_label = QLabel(f"Подробности: {priority_label} {deadline} {title}")
        content_label.setWordWrap(True)
        content_layout.addWidget(content_label)
        self.content_widget.setLayout(content_layout)
        self.content_widget.setVisible(False)
        self.content_widget.setMaximumHeight(0)
        self.content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Ширина 80% от родителя
        self.content_widget.setMinimumWidth(int(self.width()*0.8))
        self.content_widget.setMaximumWidth(int(self.width()*0.8))

        self.main_layout.addWidget(self.content_widget)

        # Сделаем ItemTask адаптивным по высоте
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    def toggle_content(self):
        if self.content_widget.isVisible():
            # скрытие
            self.anim = QPropertyAnimation(self.content_widget, b"maximumHeight")
            self.anim.setDuration(200)
            self.anim.setStartValue(self.content_widget.height())
            self.anim.setEndValue(0)
            self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            self.anim.finished.connect(lambda: self.content_widget.setVisible(False))
            self.anim.finished.connect(self.updateGeometry)  # перерасчет родителя
            self.anim.start()
        else:
            # раскрытие
            self.content_widget.setVisible(True)
            self.anim = QPropertyAnimation(self.content_widget, b"maximumHeight")
            self.anim.setDuration(200)
            self.anim.setStartValue(0)
            self.anim.setEndValue(self.content_widget.sizeHint().height())
            self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            self.anim.finished.connect(self.updateGeometry)  # перерасчет родителя
            self.anim.start()
