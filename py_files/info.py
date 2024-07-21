import sys
import os
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QScrollArea, QPushButton, QDialog, QCheckBox, QDialogButtonBox, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEvent, QEasingCurve, pyqtSlot, QTimer, QUrl, QTime, QSize
from PyQt5.QtGui import QFontDatabase, QFont, QIcon, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class InfoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.elapsed_time = QTime(0, 0, 0)
        self.init_ui()

        self.elapsed_timer = QTimer(self)
        self.elapsed_timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_timer.start(1000)

    def init_ui(self):
        layout_jogo = QVBoxLayout(self)
        layout_jogo.setContentsMargins(10, 10, 10, 10)

        self.frame_informacoes = QFrame(self)
        self.frame_informacoes.setFrameShape(QFrame.StyledPanel)
        self.frame_informacoes.setFrameShadow(QFrame.Raised)
        layout_frame_informacoes = QVBoxLayout(self.frame_informacoes)

        self.label_informacoes = QLabel("Informações", self.frame_informacoes)
        self.label_informacoes.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.label_informacoes.setFont(QFont('Karla-Bold', 24, QFont.Bold))
        self.label_informacoes.setStyleSheet("color: black;")
        layout_frame_informacoes.addWidget(self.label_informacoes)

        self.label_tempo = QLabel("Tempo: 00:00:00", self.frame_informacoes)
        self.label_tempo.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.label_tempo.setFont(QFont('Karla', 16))
        self.label_tempo.setStyleSheet("color: black;")
        layout_frame_informacoes.addWidget(self.label_tempo)

        layout_jogo.addWidget(self.frame_informacoes)

        self.label_ouros = QLabel("Ouro atual: 0", self)
        self.label_ouros.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        self.label_ouros.setFont(QFont('Karla-Bold', 18, QFont.Bold))
        self.label_ouros.setStyleSheet("""
            QLabel {
                background: #134B70;
                color: white;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 20px;
                border: 1px solid #d9d9d9;
            }
        """)

        sombra_ouros = QGraphicsDropShadowEffect()
        sombra_ouros.setBlurRadius(10)
        sombra_ouros.setOffset(2, 2)
        sombra_ouros.setColor(QColor(0, 0, 0, 75))
        self.label_ouros.setGraphicsEffect(sombra_ouros)

        layout_jogo.addWidget(self.label_ouros)

        self.frame_ouros_por_segundo = QFrame(self)
        self.frame_ouros_por_segundo.setFrameShape(QFrame.StyledPanel)
        self.frame_ouros_por_segundo.setFrameShadow(QFrame.Raised)
        layout_frame_ouros = QVBoxLayout(self.frame_ouros_por_segundo)

        self.label_ouros_por_segundo = QLabel("Rendimento: 0 ouro/s", self.frame_ouros_por_segundo)
        self.label_ouros_por_segundo.setAlignment(Qt.AlignCenter)
        self.label_ouros_por_segundo.setFont(QFont('Karla-Bold', 18, QFont.Bold))
        self.label_ouros_por_segundo.setStyleSheet("""
            QLabel {
                background: #134B70;
                color: white;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #d9d9d9;
            }
        """)

        sombra_rendimento = QGraphicsDropShadowEffect()
        sombra_rendimento.setBlurRadius(10)
        sombra_rendimento.setOffset(2, 2)
        sombra_rendimento.setColor(QColor(0, 0, 0, 75))
        self.frame_ouros_por_segundo.setGraphicsEffect(sombra_rendimento)

        layout_frame_ouros.addWidget(self.label_ouros_por_segundo)
        layout_jogo.addWidget(self.frame_ouros_por_segundo)

        self.botao_incrementar = QPushButton(self)
        self.botao_incrementar.setIcon(QIcon(os.path.join("resources", "icons", "coin.svg")))
        self.botao_incrementar.setIconSize(QSize(80, 80))
        self.botao_incrementar.setStyleSheet("border: none; background: transparent;")
        self.botao_incrementar.clicked.connect(self.incrementar_ouros)
        layout_jogo.addWidget(self.botao_incrementar, alignment=Qt.AlignCenter)

        layout_jogo.addStretch()

        self.label_autor = QLabel("Developed by @lucashaetingerr", self)
        self.label_autor.setAlignment(Qt.AlignCenter)
        self.label_autor.setFont(QFont('Karla-Bold', 10, QFont.Bold))
        self.label_autor.setStyleSheet("color: black; margin-top: 15px; margin-bottom: 7px;")
        layout_jogo.addWidget(self.label_autor, alignment=Qt.AlignBottom)

        sombra_autor = QGraphicsDropShadowEffect()
        sombra_autor.setBlurRadius(10)
        sombra_autor.setOffset(2, 2)
        sombra_autor.setColor(QColor(0, 0, 0, 75))
        self.label_autor.setGraphicsEffect(sombra_autor)

    def update_elapsed_time(self):
        self.elapsed_time = self.elapsed_time.addSecs(1)
        self.label_tempo.setText(f"Tempo: {self.elapsed_time.toString('hh:mm:ss')}")

    @pyqtSlot()
    def incrementar_ouros(self):
        valor_atual = int(self.label_ouros.text().split(": ")[1])
        novo_valor = valor_atual + 1
        self.label_ouros.setText(f"Ouro atual: {novo_valor}")
        self.parent().atualizar_estado_botoes()
        if self.parent().sound:
            self.parent().tocar_som('farm')
