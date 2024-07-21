import sys
import os
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QScrollArea, QPushButton, QDialog, QCheckBox, QDialogButtonBox, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEvent, QEasingCurve, pyqtSlot, QTimer, QUrl, QTime, QSize
from PyQt5.QtGui import QFontDatabase, QFont, QIcon, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Configurações')
        self.setWindowIcon(QIcon(os.path.join("resources", "icons", "settings.svg")))
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint)
        self.init_ui()
        self.adjustSize()

    def init_ui(self):
        layout = QVBoxLayout(self)

        options_layout = QVBoxLayout()
        options_layout.setAlignment(Qt.AlignCenter)
        self.opcao1 = QCheckBox("Opção 1", self)
        self.opcao1.setLayoutDirection(Qt.RightToLeft)
        self.opcao2 = QCheckBox("Opção 2", self)
        self.opcao2.setLayoutDirection(Qt.RightToLeft)
        self.opcao3 = QCheckBox("Opção 3", self)
        self.opcao3.setLayoutDirection(Qt.RightToLeft)

        options_layout.addWidget(self.opcao1)
        options_layout.addWidget(self.opcao2)
        options_layout.addWidget(self.opcao3)

        layout.addLayout(options_layout)

        botoes_layout = QHBoxLayout()
        botoes_dialogo = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        botoes_dialogo.accepted.connect(self.apply)
        botoes_dialogo.rejected.connect(self.reject)

        botoes_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        botoes_layout.addWidget(botoes_dialogo)
        botoes_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(botoes_layout)

        self.setLayout(layout)

    def apply(self):
        self.accept()
