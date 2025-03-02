from abc import ABCMeta

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class Meta(ABCMeta, type(QWidget)):
    pass

class ConfigWidget(QWidget, metaclass=Meta):
    def __init__(self, parent=None):
        super().__init__(parent)

    def AddButtons(self, layout):
        button_layout = QHBoxLayout()
        self.save_button = self.FixedQPushButton("Save")
        self.save_button.setDefault(True)
        self.revert_button = self.FixedQPushButton("Revert")

        self.save_button.setEnabled(False)
        self.revert_button.setEnabled(False)

        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.revert_button)
        
        layout.addLayout(button_layout)

    def FixedQPushButton(self, text: str) -> QPushButton:
        button = QPushButton(text, self)
        button.setFixedWidth(64)
        return button
