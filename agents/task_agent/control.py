
from rich import print
from rich.pretty import pprint
from core.base import BaseControl
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox, QStyledItemDelegate
from PyQt6.QtCore import Qt, QDate, QRect
from PyQt6.QtGui import QPainter, QBrush, QColor, QFont
from datetime import datetime

class TaskControl(BaseControl):
    def __init__(self, presentation, abstraction):
        super().__init__(presentation, abstraction)
        # wire up UI actions
        self.presentation.new_btn.clicked.connect(self.toggle_new_area)
        self.presentation.save_btn.clicked.connect(self.save_task)
        self.presentation.search_input.textChanged.connect(self.on_search)
        self.presentation.filter_combo.currentTextChanged.connect(self.refresh_list)
        self.presentation.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        # initial load
        self.presentation.list_widget.setItemDelegate(ViewDelegate())
        self.refresh_list()
        self.toggle_new_area()


    def toggle_new_area(self):
        # show/hide creation widgets
        widgets = [self.presentation.title_input, self.presentation.due_date, self.presentation.priority, self.presentation.save_btn]
        visible = self.presentation.title_input.isVisible()
        for w in widgets:
            w.setVisible(not visible)

    def save_task(self):
        title = self.presentation.title_input.text().strip()
        if not title:
            QMessageBox.warning(None, "Error", "Title is required")
            return
        due = self.presentation.due_date.date().toString("yyyy-MM-dd")
        priority = self.presentation.priority.currentText()
        self.abstraction.add_task(title, '', due_date=due, priority=priority)
        self.presentation.title_input.clear()
        self.refresh_list()

    def on_search(self, text):
        self.refresh_list()

    def on_item_double_clicked(self, item):
        task_id = item.data(256)
        # toggle done status
        rows = self.abstraction.get_tasks()
        for r in rows:
            if r['id'] == task_id:
                new_status = 'done' if r['status'] != 'done' else 'pending'
                self.abstraction.update_task(task_id, status=new_status)
                break
        self.refresh_list()

    def refresh_list(self, list_widget=None):
        filter_type = self.presentation.filter_combo.currentText()
        search = self.presentation.search_input.text().strip() or None
        rows = self.abstraction.get_tasks(filter_type=filter_type, search=search)
        self.presentation.list_widget.clear()
        last_date = None
        for r in rows:
            due = r['due_date']
            date_label = due if due else "No due date"
            # Add separator when date changes
            if date_label != last_date:
                sep = QListWidgetItem(f"{date_label}")
                sep.setFlags(Qt.ItemFlag.ItemIsEnabled)
                sep.setData(Qt.ItemDataRole.UserRole, "separator_date")
                self.presentation.list_widget.addItem(sep)
                last_date = date_label
            priority = r['priority']
            title = r['title']
            self.setViewTask( self,title=title, priority=priority)

    def setViewTask(self,*args, **kwargs):
        # task['priority']
        # priority = f"{task['priority']}"
        # title = f"{task['title']}"
        # print(kwargs['title'])
        self.title_box = QListWidgetItem(f"{kwargs['title']}");
        # self.priority_box = QListWidgetItem();
        # self.box_task = QListWidget()
        # self.box_task.addItem(title_box)
        # self.presentation.list_widget.addItem(box_task)

class ViewDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        item_class = index.data(Qt.ItemDataRole.UserRole)
        if item_class == "separator_date":
            painter.save()
            painter.fillRect(option.rect, QColor(45, 45, 45))
            #painter.setPen(QColor("white"))
            font = QFont()
            font.setBold(True)
            painter.setFont(font)
            text = index.data(Qt.ItemDataRole.DisplayRole)
            padding = 10
            text_rect = QRect(option.rect)
            text_rect.adjust(padding, 0, -padding, 0)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)
            painter.restore()
        else:
            super().paint(painter, option, index)

