
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QObject, pyqtSignal

class BaseModel:
    pass

class BaseAbstraction(QObject):
    property_changed = pyqtSignal(str, object)
    def __init__(self):
        super().__init__()

class BasePresentation(QMainWindow):
    pass

class BaseView(QObject):
    pass

class BaseControl(QObject):
    def __init__(self, presentation, abstraction):
        super().__init__()
        self.presentation = presentation
        self.abstraction = abstraction

class BaseAgent:
    def __init__(self, presentation=None, abstraction=None, control_cls=None, model=None):
        self.presentation = presentation
        self.abstraction = abstraction
        self.model = model
        self.control = None
        if presentation and abstraction and control_cls:
            self.control = control_cls(presentation, abstraction)
    def show(self):
        if self.presentation:
            self.presentation.show()
