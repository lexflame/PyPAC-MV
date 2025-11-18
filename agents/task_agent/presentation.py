import qtawesome as qta
import re

from core.base import BasePresentation
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QHBoxLayout, QComboBox, \
    QDateEdit, QAbstractItemView
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtCore import QSize

from agents.task_agent.abstraction import TaskAbstraction
from agents.task_agent.control import TaskControl

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
        self.abstraction = TaskAbstraction()
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

        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(True)
        # self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.list_widget.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.list_widget.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.list_widget.model().rowsMoved.connect(self.on_rows_moved)

        # self.list_widget.setFixedWidth(250) # Ширина столбца вывода задач

        self.list_widget.setStyleSheet("""
            QListWidget {
                color: #ecf0f1;
                border: none;
            }
            QListWidget::item[data-role="separator_date"] {
                background-color: #FFF !important;
                color: white;
                w1idth: 50%;
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
        # self.title_input.hide()
        # self.due_date.hide()
        # self.priority.hide()
        # self.save_btn.hide()

        # self.control = TaskControl(self, self.abstraction)

    def on_rows_moved(self, parent, start, end, destination, row):

        def check_date_separator(s):
            pattern = r'^\d{4}-\d{2}-\d{2}$'
            return re.fullmatch(pattern, s) is not None

        separator_item_start = self.list_widget.item(start)
        date_to = separator_item_start.text()
        jq(f"DATE FROM START :: {date_to}")

        separator_item_end = self.list_widget.item(end)
        date_to_end = separator_item_end.text()
        jq(f"DATE FROM END :: {date_to_end}")

        if check_date_separator(date_to) != True:
            for i in range(row, 0, -1):
                find_separ = self.list_widget.item(i)
                if check_date_separator(find_separ.text()):
                    date_to = find_separ.text()
                    break

        if check_date_separator(date_to):
            moved_item = self.list_widget.item(row)
            if moved_item is None:
                return

            task_id = moved_item.data(256)
            # print("Перемещен элемент с ID:", task_id)

            # Можно получить виджет задачи
            task_widget = self.list_widget.itemWidget(moved_item)
            if task_widget:
                ins_possition = int(task_widget.item_position.text())
                moved_curr_item = self.list_widget.item(ins_possition)
                task_id = moved_curr_item.data(256)
                # task_curr_widget = self.list_widget.itemWidget(moved_curr_item)
                # print("Название:", task_curr_widget.title_edit_input.text())
            jq(f'Новая дата:: {date_to}')
            self.abstraction.update_task(task_id, due_date=date_to)
            self.control.refresh_list()
        else:
            jq('ОШИБКА ДАТА НЕ ЗАДАННА')
            # jq(self)
            # jq(self.list_widget.item(start).text) # separator_data
            # jq(self.list_widget.item(row)) # separator_data
            # print(f"Элементы {start}-{end} перемещены на позицию {row}")
