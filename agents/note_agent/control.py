
from core.base import BaseControl

class NoteControl(BaseControl):
    def __init__(self, presentation, abstraction):
        super().__init__(presentation, abstraction)
        # простая логика
        self.presentation.save.clicked.connect(self.on_save)

    def on_save(self):
        print("Сохраняем текст:", self.presentation.text.toPlainText())
