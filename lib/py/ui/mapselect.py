from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSignal

from lib.py.common import *
from lib.py.mod import *

column_order = ['ModName', 'MapId', 'MapName', 'Author', 'CompLevel', 'Files', 'Merge', 'Port', 'Notes']

class GridViewWindow(QMainWindow):
    index_selected = pyqtSignal(int)

    def __init__(self, data, column_order):
        super().__init__()
        self.model = QStandardItemModel()
        self.table_view = QTableView(self)
        self.table_view.setModel(self.model)
        self.setCentralWidget(self.table_view)
        self.resize(1920,1080)

        # Create table headers based on keys in the first dictionary
        self.model.setHorizontalHeaderLabels(column_order)

        for row_dict in data:
            row_items = [QStandardItem(str(row_dict[key])) for key in column_order]
            for item in row_items:
                item.setEditable(False)  # Set the item as uneditable
            self.model.appendRow(row_items)

        self.table_view.doubleClicked.connect(self.handle_double_click)
        self.table_view.resizeColumnsToContents()

    def handle_double_click(self, index):
        self.index_selected.emit(index.row())
        self.close()  # Close the window

def OpenMapSelection(maps):

    rows = []
    for map in maps:
        rows.append(map.Dictify())

    app = QApplication([])
    window = GridViewWindow(rows, column_order)
    selected = None

    def handle_index_selected(index):
        nonlocal selected
        selected = maps[index]

    window.index_selected.connect(handle_index_selected)

    window.show()
    app.exec_()

    return selected
