import os
import re
import hashlib

from PySide6.QtWidgets import QFileDialog
from jacodemon.model.config import GetConfig, JacodemonConfig

def ParseTimestampFromPath(path):
    basename = os.path.basename(path)

    match = re.search(r"\d{4}-\d{2}-\d{2}T\d{6}", basename)
    timestamp = match.group(0) if match else None

    return timestamp

def OpenSingleFileDialog(parent, types, line):
    file, _ = QFileDialog.getOpenFileName(parent, "Open File", "", types)

    if file:
        line.setText(file)

# TODO: move this also
def OpenDirectoryDialog(parent, what, line):
    options = QFileDialog.Option.ShowDirsOnly
    directory = QFileDialog.getExistingDirectory(parent, f"Select {what} directory", "", options=options)

    if directory:
        line.setText(directory)

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

def GetFileHash(filepath: str) -> str:
    """Compute a fast MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    buffer_size = 1048576  # 1MB chunks for better performance on large files

    with open(filepath, "rb") as f:
        while chunk := f.read(buffer_size):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()

def ToPathHashTupleList(filepaths: list[str]) -> list[tuple[str, str]]:
    """Convert a list of filepaths to a list of tuples of (filepath, hash)."""
    return [(filepath, GetFileHash(filepath)) for filepath in filepaths]
