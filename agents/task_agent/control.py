from core.base import BaseControl
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect

from agents.task_agent.classes.item_separator import ItemSeparator
from agents.task_agent.classes.item_task import ItemTask

class TaskControl(BaseControl):
    def __init__(self, presentation, abstraction):
        super().__init__(presentation, abstraction)
        # wire up UI actions
        self.presentation.save_btn.clicked.connect(self.save_task)
        self.presentation.search_input.textChanged.connect(self.on_search)
        self.presentation.filter_combo.currentTextChanged.connect(self.refresh_list)
        self.presentation.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        # initial load
        self.presentation.list_widget.setItemDelegate(ItemSeparator())
        self.refresh_list()

    def save_task(self):
        title = self.presentation.title_input.text().strip()

        if len(title) < 2:
            QMessageBox.warning(None, "Error", "Title task is required")
            return

        due = self.presentation.due_date.date().toString("yyyy-MM-dd")
        priority = self.presentation.priority.currentText()
        self.abstraction.add_task(title, '', due_date=due, priority=priority)
        self.refresh_list()
        self.presentation.title_input.clear()

    def on_search(self, text):
        self.refresh_list()

    def complite_task(self, item):
        task_id = item.data(256)
        task_id = int(task_id)
        self.abstraction.complite_task(task_id)
        self.refresh_list()

    def delete_task(self, item):
        task_id = item.data(256)
        task_id = int(task_id)
        self.abstraction.delete_task(task_id)
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
        filter_type = self.presentation.filter_combo.currentData()
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

            # Создаём элемент списка
            self.ListItem = QListWidgetItem()

            self.ListItem.setData(256, int(r['id']))
            self.position = self.presentation.list_widget.count() - 1;
            task_widget = ItemTask(
                title=title,
                priority=priority,
                deadline=due,
                list_item=self.ListItem,
                complite_event=self.complite_task,
                delete_event=self.delete_task,
                collapse_all=self.collapse_all,
                data=r,
                position=self.position
            )
            # item.setSizeHint(QSize(0, 180))
            self.ListItem.setSizeHint(task_widget.sizeHint())
            # task_widget.setMinimumHeight(40)


            # Привязываем виджет к элементу
            self.presentation.list_widget.addItem(self.ListItem)
            self.presentation.list_widget.setItemWidget(self.ListItem, task_widget)
            # self.presentation.list_widget.setUniformItemSizes(False)

    def scroll_to_item_smooth(self, item):
        """Плавно прокручивает к элементу item."""
        target_value = self.row(item) * self.sizeHintForRow(0)  # высота строки * номер
        anim = QPropertyAnimation(self.verticalScrollBar(), b"value")
        anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        anim.setStartValue(self.verticalScrollBar().value())
        anim.setEndValue(target_value)
        anim.setDuration(300)
        anim.start()
        self._anim = anim

    def scroll(self):
        item = self.presentation.list_widget.item(30)
        self.presentation.list_widget.scroll_to_item_smooth(item)

    def collapse_all(self):
        list_widget = self.presentation.list_widget
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            widget = list_widget.itemWidget(item)
            if not widget:
                continue

            # Скрываем раскрытые элементы
            for part_name in ("edit", "desc"):
                part = getattr(widget, part_name, None)
                if part and part.isVisible():
                    part.hide()

            # Обновляем лейаут и высоту
            widget.layout().activate()
            widget.adjustSize()
            item.setSizeHint(QSize(widget.width(), 85))
            self.animate_collapse(widget)

    def animate_collapse(self,widget):
        l_item = self.ListItem
        start_height = l_item.sizeHint().height()
        end_height = 85

        if start_height == end_height:
            return  # уже свернут

        anim = QPropertyAnimation(widget, b"geometry")
        anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        anim.setStartValue(QRect(0, widget.y(), widget.width(), start_height))
        anim.setEndValue(QRect(0, widget.y(), widget.width(), end_height))
        anim.setDuration(250)


        # Чтобы не "улетала" геометрия
        def update_height():
            item.setSizeHint(widget.sizeHint())

        anim.valueChanged.connect(update_height)
        anim.finished.connect(update_height)

        # Хранить ссылку, чтобы не уничтожалась сборщиком
        widget._collapse_anim = anim
        anim.start()