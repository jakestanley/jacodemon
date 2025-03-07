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

def FindAndVerify(filepaths: list[tuple[str, str]], additionalSearchDirectories: list[str]) -> list[tuple[str, str]]:
    """Verify that the files in the list exist, search for them in additional search 
    directories recursively if not, and ensure the files have not been modified. 
    If no hash is present, skip verification"""
    verified = []

    # TODO: make this recursive, and verify hash (if present) before 
    #   returning a result in the filepaths loop
    for filepath, hash in filepaths:
        if not os.path.exists(filepath):
            for directory in additionalSearchDirectories:
                if os.path.exists(os.path.join(directory, os.path.basename(filepath))):
                    filepath = os.path.join(directory, os.path.basename(filepath))
                    break
            else:
                raise FileNotFoundError(f"File not found: {filepath}")

        if hash and hash != "nohash":
            if hash != GetFileHash(filepath):
                raise ValueError(f"File has been modified: {filepath}")
        else:
            print(f"Skipping hash verification for {filepath} as no hash was present")

        verified.append((filepath, hash))

    return verified
