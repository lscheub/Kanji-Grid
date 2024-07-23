# -*- coding: utf-8 -*-

import os

from aqt import mw
from aqt.qt import *

from ..version import VERSION


class Dialog(QDialog):

    FONT_HEADER = QFont()
    FONT_HEADER.setPointSize(12)
    FONT_HEADER.setBold(True)

    FONT_INFO = QFont()
    FONT_INFO.setItalic(True)

    FONT_LABEL = QFont()
    FONT_LABEL.setBold(True)

    FONT_TITLE = QFont()
    FONT_TITLE.setPointSize(16)
    FONT_TITLE.setBold(True)

    SPACING = 10


    def __init__(self, title, parent):
        super(Dialog, self).__init__(parent)

        self.title = title
        self.setModal(True)
        self.setLayout(self.ui())
        self.setWindowTitle(
            self.title if "Kanji Grid Advanced" in self.title else "Kanji Grid Advanced: %s" % self.title
        )
        self.setMinimumSize(600,100)


    def ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self.ui_banner())
        layout.addWidget(self.ui_divider(QFrame.Shape.HLine))

        return layout


    def ui_banner(self):
        title = QLabel(self.title)
        title.setFont(self.FONT_TITLE)

        version = QLabel("Kanji Grid Advanced\nv%s" % VERSION)
        version.setFont(self.FONT_INFO)

        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(self.SPACING)
        layout.addStretch()
        layout.addWidget(version)

        return layout


    def ui_divider(self, orientation_style=QFrame.Shape.VLine):
        frame = QFrame()
        frame.setFrameStyle(orientation_style | QFrame.Shadow.Sunken)

        return frame


    def ui_buttons(self):
        self.buttons = QDialogButtonBox()
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.buttons.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        return self.buttons
