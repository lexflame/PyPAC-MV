from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QFrame


class TaskItemBehavior:
    """Отвечает за поведение и анимацию ItemTask."""

    def __init__(self, parent):
        self.parent = parent  # ссылка на ItemTask
        self._anim = None

    # ----------------------------
    # Обработчики кликов
    # ----------------------------

    def on_edit_clicked(self):
        """Скрыть другие, переключить режим редактирования."""
        if self.parent._collapse_all:
            self.parent._collapse_all()
        self.toggle_edit()

    def on_desc_clicked(self):
        """Скрыть другие, переключить описание."""
        if self.parent._collapse_all:
            self.parent._collapse_all()
        self.toggle_desc()

    # ----------------------------
    # Переключатели секций
    # ----------------------------

    def toggle_edit(self):
        """Показать/скрыть секцию редактирования."""
        if self.parent.desc.isVisible():
            self.parent.desc.hide()

        visible = self.parent.edit.isVisible()
        self.parent.edit.setVisible(not visible)
        self.animate_size_change(expanding=not visible)

    def toggle_desc(self):
        """Показать/скрыть описание."""
        if self.parent.edit.isVisible():
            self.parent.edit.hide()

        visible = self.parent.desc.isVisible()
        self.parent.desc.setVisible(not visible)
        self.animate_size_change(expanding=not visible)

    # ----------------------------
    # Визуальные эффекты
    # ----------------------------

    def create_priority_circle(self):
        """Создаёт цветной кружок для приоритета."""
        color_map = {
            "high": "#e74c3c",  # красный
            "normal": "#f1c40f",  # желтый
            "low": "#2ecc71",  # зеленый
        }
        color = color_map.get(self.parent._priority, "#95a5a6")

        circle = QFrame()
        circle.setFixedSize(16, 16)
        circle.setStyleSheet(f"border-radius: 8px; background-color: {color};")
        return circle

    def animate_size_change(self, expanding=True):
        start_height = self.parent.height()
        end_height = self.parent.sizeHint().height()

        anim = QPropertyAnimation(self.parent, b"maximumHeight")
        anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        anim.setStartValue(start_height)
        anim.setEndValue(end_height)
        anim.setDuration(400)
        anim.start()
        self._anim = anim

        def on_finished():
            if self.parent._list_item:
                self.parent._list_item.setSizeHint(self.parent.sizeHint())

        anim.finished.connect(on_finished)

    def save_task_edit(self):
        set_title       = self.parent.title_edit_input.text().strip()
        set_date        = self.parent.due_date_edit.date().toString("yyyy-MM-dd")
        set_priority    = self.parent.priority_edit.currentText()
        jq(self.parent.id_task)
        # self.parent.abstraction.update_task(task_id, status=new_status)


