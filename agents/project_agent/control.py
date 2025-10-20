
from core.base import BaseControl
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox
from PyQt6.QtCore import QDate
from datetime import datetime

class ProjectControl(BaseControl):
    def __init__(self, presentation, abstraction):
        super().__init__(presentation, abstraction)
        # wire up UI actions
        self.presentation.new_btn.clicked.connect(self.toggle_new_area)
        self.presentation.save_btn.clicked.connect(self.save_project)
        self.presentation.search_input.textChanged.connect(self.on_search)
        self.presentation.filter_combo.currentTextChanged.connect(self.refresh_list)
        self.presentation.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        # initial load
        self.refresh_list()
        self.toggle_new_area()

    def toggle_new_area(self):
        # show/hide creation widgets
        widgets = [self.presentation.title_input, self.presentation.due_date, self.presentation.priority, self.presentation.save_btn]
        visible = self.presentation.title_input.isVisible()
        for w in widgets:
            w.setVisible(not visible)

    def save_project(self):
        title = self.presentation.title_input.text().strip()
        if not title:
            QMessageBox.warning(None, "Error", "Title is required")
            return
        due = self.presentation.due_date.date().toString("yyyy-MM-dd")
        priority = self.presentation.priority.currentText()
        self.abstraction.add_project(title, '', due_date=due, priority=priority)
        self.presentation.title_input.clear()
        self.refresh_list()

    def on_search(self, text):
        self.refresh_list()

    def on_item_double_clicked(self, item):
        project_id = item.data(256)
        # toggle done status
        rows = self.abstraction.get_projects()
        for r in rows:
            if r['id'] == project_id:
                new_status = 'done' if r['status'] != 'done' else 'pending'
                self.abstraction.update_project(project_id, status=new_status)
                break
        self.refresh_list()

    def refresh_list(self):
        filter_type = self.presentation.filter_combo.currentText()
        search = self.presentation.search_input.text().strip() or None
        rows = self.abstraction.get_projects(filter_type=filter_type, search=search)
        self.presentation.list_widget.clear()
        last_date = None
        for r in rows:
            due = r['due_date']
            date_label = due if due else "No due date"
            # Add separator when date changes
            if date_label != last_date:
                sep = QListWidgetItem(f"--- {date_label} ---")
                sep.setFlags(sep.flags() & ~ (sep.flags()))  # non-selectable
                self.presentation.list_widget.addItem(sep)
                last_date = date_label
            text = f"[{r['priority']}] {r['title']}"
            item = QListWidgetItem(text)
            item.setData(256, r['id'])
            self.presentation.list_widget.addItem(item)
