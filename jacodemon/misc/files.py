import os
import re

from PySide6.QtWidgets import QFileDialog

from jacodemon.model.config import GetConfig, JacodemonConfig


def ParseTimestampFromPath(path):
    basename = os.path.basename(path)

    match = re.search(r"\d{4}-\d{2}-\d{2}T\d{6}", basename)
    timestamp = match.group(0) if match else None

    return timestamp

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
