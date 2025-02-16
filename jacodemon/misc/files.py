from PySide6.QtWidgets import QFileDialog

from jacodemon.config import GetConfig, JacodemonConfig

def FindIwad() -> str:

    config: JacodemonConfig = GetConfig()

    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

    title = "Select an IWAD"

    fileName, _ = dialog.getOpenFileName(None, title, config.iwad_dir,
        "WAD files (*.wad)")

    return fileName

def FindDoomFiles(start_dir: str = "") -> str:
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

    title = "Select a map set"

    fileNames, _ = dialog.getOpenFileNames(None, title, start_dir,
        "Doom mod files (*.pk3 *.wad *.deh);;Other (*)")

    return fileNames