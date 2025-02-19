from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget

from jacodemon.view.components.sets.select import MapSetList

class SetsTab(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Set")

        self.layout = QVBoxLayout()

        self.new_button = QPushButton("New map set")
        self.setLayout(self.layout)

        self.mapSetList = MapSetList()
        self.layout.addWidget(self.new_button)
        self.layout.addWidget(self.mapSetList)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = SetsTab()
    widget.show()
    sys.exit(app.exec())
