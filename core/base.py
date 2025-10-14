from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMainWindow

class BaseModel:
    pass

class BaseAbstraction(QObject):
    property_changed = pyqtSignal(str, object)
    def __init__(self, parent=None):
        super().__init__(parent)

class BasePresentation(QMainWindow):
    """Base presentation: expects a .widget attribute for embedding in Dashboard."""
    def __init__(self, parent=None):
        super().__init__(parent)

class BaseControl(QObject):
    def __init__(self, presentation, abstraction, parent=None):
        super().__init__(parent)
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
            try:
                self.presentation.show()
            except Exception:
                pass
