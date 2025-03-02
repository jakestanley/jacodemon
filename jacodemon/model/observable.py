from PySide6.QtCore import QObject, Signal

class ObservableModel(QObject):
    changed = Signal()

    def notify_change(self):
        self.changed.emit()
