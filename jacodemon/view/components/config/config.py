from abc import ABCMeta, abstractmethod

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class Meta(ABCMeta, type(QWidget)):
    pass

class ConfigWidget(QWidget, metaclass=Meta):
    def __init__(self, parent=None):
        super().__init__(parent)

    def AddButtons(self, layout):
        button_layout = QHBoxLayout()
        save_button = self.FixedQPushButton("Save")
        save_button.setDefault(True)
        revert_button = self.FixedQPushButton("Revert")

        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(revert_button)
        
        layout.addLayout(button_layout)

    def FixedQPushButton(self, text: str) -> QPushButton:
        button = QPushButton(text, self)
        button.setFixedWidth(64)
        return button
