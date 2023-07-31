from PyQt5.QtWidgets import QApplication

from lib.py.ui.mapselect import GridViewWindow

column_order = ['Lump', 'Stats']

# TODO: refactor statistics class so it can be used display demo stats in the picker
def OpenDemoSelection(demos):
    
    rows = []
    for demo in demos:
        rows.append(demo.Dictify())

    app = QApplication([])
    window = GridViewWindow(rows, column_order)
    selected = None

    def handle_index_selected(index):
        nonlocal selected
        selected = demos[index]

    window.index_selected.connect(handle_index_selected)

    window.show()
    app.exec_()

    return selected
