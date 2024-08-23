from PySide6.QtWidgets import QFileDialog

def FindDoomFiles(start_dir: str = "") -> str:
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

    title = "Select a map set"

    fileNames, _ = dialog.getOpenFileNames(None, title, start_dir,
        "Doom mod files (*.pk3 *.wad *.deh);;Other (*)")

    return fileNames