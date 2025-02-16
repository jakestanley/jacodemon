from jacodemon.view.components.config.config import ConfigWidget

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QLineEdit

class ObsTab(ConfigWidget):
    def __init__(self, parent=None):
        super(ObsTab, self).__init__(parent)

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

    def save(self):
        pass
        # TODO: get data or similar
        # cfg: JacodemonConfig = GetConfig()
        # cfg.play_scene = self.play_scene.text()
        # cfg.wait_scene = self.wait_scene.text()
        # cfg.browser_scene = self.browser_scene.text()
        # cfg.title_source = self.title_source.text()
        # cfg.Save()

    def revert(self):
        self.LoadValuesFromConfig()
