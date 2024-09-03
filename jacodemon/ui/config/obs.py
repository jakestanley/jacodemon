from jacodemon.ui.config.config import ConfigWidget
from jacodemon.config import JacodemonConfig, GetConfig

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit

class ObsTab(ConfigWidget):
    def __init__(self, parent=None):
        super(ObsTab, self).__init__(parent)

        cfg: JacodemonConfig = GetConfig()
        layout: QVBoxLayout = QVBoxLayout(self)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("play_scene"))
        self.play_scene = QLineEdit(self)
        hbox.addWidget(self.play_scene)
        self.btn_test_play_scene = QPushButton("Test", self)
        hbox.addWidget(self.btn_test_play_scene)

        layout.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("wait_scene"))
        self.wait_scene = QLineEdit(self)
        hbox.addWidget(self.wait_scene)
        self.btn_test_wait_scene = QPushButton("Test", self)
        hbox.addWidget(self.btn_test_wait_scene)
        layout.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("browser_scene"))
        self.browser_scene = QLineEdit(self)
        hbox.addWidget(self.browser_scene)
        self.btn_test_browser_scene = QPushButton("Test", self)
        hbox.addWidget(self.btn_test_browser_scene)
        layout.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("title_source"))
        self.title_source = QLineEdit(self)
        hbox.addWidget(self.title_source)
        self.btn_test_title_source = QPushButton("Test", self)
        hbox.addWidget(self.btn_test_title_source)
        layout.addLayout(hbox)
        layout.addStretch()

        self.AddButtons(layout)
        self.LoadValuesFromConfig()

    def LoadValuesFromConfig(self):
        cfg: JacodemonConfig = GetConfig()
        self.play_scene.setText(cfg.play_scene)
        self.wait_scene.setText(cfg.wait_scene)
        self.browser_scene.setText(cfg.browser_scene)
        self.title_source.setText(cfg.title_source)

    def save(self):
        cfg: JacodemonConfig = GetConfig()
        cfg.play_scene = self.play_scene.text()
        cfg.wait_scene = self.wait_scene.text()
        cfg.browser_scene = self.browser_scene.text()
        cfg.title_source = self.title_source.text()
        cfg.Save()

    def revert(self):
        self.LoadValuesFromConfig()
