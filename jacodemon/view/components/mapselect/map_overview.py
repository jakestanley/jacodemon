from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from jacodemon.view.components.mapselect.demo import DemoTableView

class MapOverviewWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self._selected_demo = None
        layout = QVBoxLayout(self)

        self.play_button = QPushButton("Play")
        

        self.demo_table = DemoTableView(self)
        # TODO signal instead
        
        self.play_demo_button = QPushButton("Play Demo")
        
        

        layout.addWidget(self.play_button)
        layout.addWidget(self.demo_table)
        layout.addWidget(self.play_demo_button)

        layout.addStretch()
        self.setLayout(layout)

if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication([])

    window = MapOverviewWidget(None)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
