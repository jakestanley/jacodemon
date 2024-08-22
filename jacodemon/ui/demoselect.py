from PySide6.QtWidgets import QApplication

from jacodemon.ui.mapselect import GridViewWindow

column_order = ['Lump', 'Time', 'Kills', 'Items', 'Secrets']

def OpenDemoSelection(demos):
    
    rows = []
    for demo in demos:
        rows.append(demo.Dictify())

    app = QApplication.instance()
    window = GridViewWindow(rows, column_order)
    selected = None

    def handle_index_selected(index):
        nonlocal selected
        selected = demos[index]

    window.index_selected.connect(handle_index_selected)

    window.show()
    app.exec()

    return selected
