from enum import Enum
from PySide6.QtWidgets import QStackedWidget, QWidget

class UIState(Enum):
    SELECT_SET = 0
    SELECT_MAP = 1
    PRE_LAUNCH = 2
    SUBPROCESS = 3

class UIManager(QStackedWidget):

    def __init__(self):
        super().__init__()
        self.views = {}

    def register_view(self, state, view: QWidget):
        self.views[state] = view
        self.addWidget(view)

    def set_state(self, state: UIState):
        if state in self.views:
            self.setCurrentWidget(self.views[state])
