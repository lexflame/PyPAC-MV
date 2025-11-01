import qtawesome as qta
from core.base import BasePresentation
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QHBoxLayout, QComboBox, QDateEdit
from PyQt6.QtCore import QDate
from PyQt6.QtCore import QSize

class TaskPresentation(BasePresentation):
    def __init__(self):
        super().__init__()
        # We'll expose .widget for embedding into Dashboard
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        # Toolbar: create and search
        toolbar = QHBoxLayout()
        # self.new_btn = QPushButton("add")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("План", "plan")
        self.filter_combo.addItem("Просроченые", "overdue")
        self.filter_combo.addItem("Все", "all")
        self.filter_combo.addItem("Выполненые", "done")

        # toolbar.addWidget(self.new_btn)
        # toolbar.addStretch()
        toolbar.addWidget(self.search_input, stretch=1)
        toolbar.addWidget(QLabel("Режим отображения:"))
        toolbar.addWidget(self.filter_combo)

        # Creation area (hidden by default)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название задачи")
        self.due_date = QDateEdit()
        self.due_date.setCalendarPopup(True)
        self.due_date.setDate(QDate.currentDate())
        self.priority = QComboBox()
        self.priority.addItems(["low", "normal", "high"])
        icon = qta.icon("mdi.chevron-double-down", color="#aaa")
        self.save_btn = QPushButton()
        self.save_btn.setIcon(icon)
        self.save_btn.setIconSize(QSize(24, 24))
        self.save_btn.setFixedSize(25, 25)
        self.save_btn.setToolTip('Добавить задачу')
        create_layout = QHBoxLayout()
        create_layout.addWidget(self.title_input)
        create_layout.addWidget(self.due_date)
        create_layout.addWidget(self.priority)
        create_layout.addWidget(self.save_btn)

        # Filter
        filter_layout = QHBoxLayout()
        filter_layout.addStretch()

        # List of tasks
        self.list_widget = QListWidget()
        # self.list_widget.setFixedWidth(250) # Ширина столбца вывода задач

        self.list_widget.setStyleSheet("""
            QListWidget {
                color: #ecf0f1;
                border: none;
            }
            QListWidget::item[data-role="separator_date"] {
                background-color: #FFF !important;
                color: white;
                width: 50%;
            }
            QListWidget::item {
                background-color: #2c3e50;
                border-radius: 4px;
                margin: 5px;
            }
            QListWidget::item:hover {
                background-color: #3498db;
                animation: hover-effect 0.3s ease;
            }
            QListWidget::item:selected {
                background-color: #34495e;  /* Цвет выделения */
                color: white;
            }
        """)

        # Assemble
        self.layout.addLayout(create_layout)
        self.layout.addLayout(toolbar)
        # self.layout.addLayout(filter_layout)
        self.layout.addWidget(self.list_widget)

        # Hide creation inputs initially
        self.title_input.hide()
        self.due_date.hide()
        self.priority.hide()
        self.save_btn.hide()
