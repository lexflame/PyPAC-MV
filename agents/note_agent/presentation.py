
from core.base import BasePresentation
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QTextEdit, QPushButton

class NotePresentation(BasePresentation):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note Agent")
        self.resize(400,300)
        self.view = QWidget()
        layout = QVBoxLayout()
        self.text = QTextEdit()
        self.save = QPushButton("Сохранить")
        layout.addWidget(QLabel("Заметка:"))
        layout.addWidget(self.text)
        layout.addWidget(self.save)
        self.view.setLayout(layout)
        self.setCentralWidget(self.view)
