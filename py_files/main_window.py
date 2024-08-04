import sys
import os
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QScrollArea, QPushButton, QDialog, QCheckBox, QDialogButtonBox, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEvent, QEasingCurve, pyqtSlot, QTimer, QUrl, QTime, QSize
from PyQt5.QtGui import QFontDatabase, QFont, QIcon, QColor, QScreen
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from py_files.shop import Shop
from py_files.info import InfoPanel
from py_files.settings import ConfigDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        QFontDatabase.addApplicationFont(os.path.join("resources", "fonts", "Karla", "static", "Karla-Regular.ttf"))
        QFontDatabase.addApplicationFont(os.path.join("resources", "fonts", "Karla-Bold", "static", "Karla-Bold.ttf"))

        self.setWindowIcon(QIcon(os.path.join("resources", "icons", "coin.svg")))
        self.sound = True
        self.audio_players = []
        self.gift_icon = None

        self.info_panel = InfoPanel(self)
        self.shop = Shop(self.metodo_exemplo, self)

        self.init_ui()

        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_gift_icon)
        self.spawn_timer.start(60000)

        self.elapsed_timer = QTimer(self)
        self.elapsed_timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_time = QTime(0, 0, 0)
        self.elapsed_timer.start(1000)

    def init_ui(self):
        self.setWindowTitle("[ALPHA] Pirate Coin Plunder")
        self.setFixedSize(1024, 768)

        layout_principal = QHBoxLayout(self)

        layout_principal.addWidget(self.shop, 1)

        divisoria_direita_loja = QFrame(self)
        divisoria_direita_loja.setFrameShape(QFrame.VLine)
        divisoria_direita_loja.setFrameShadow(QFrame.Sunken)
        divisoria_direita_loja.setStyleSheet("color: #d9d9d9;")
        layout_principal.addWidget(divisoria_direita_loja)

        layout_principal.addWidget(self.info_panel, 2)

        divisoria_esquerda_icones = QFrame(self)
        divisoria_esquerda_icones.setFrameShape(QFrame.VLine)
        divisoria_esquerda_icones.setFrameShadow(QFrame.Sunken)
        divisoria_esquerda_icones.setStyleSheet("color: #d9d9d9;")
        layout_principal.addWidget(divisoria_esquerda_icones)

        self.botao_som = QPushButton(self)
        self.botao_som.setIcon(QIcon(os.path.join("resources", "icons", "sound.svg")))
        self.botao_som.setIconSize(self.botao_som.size())
        self.botao_som.setStyleSheet("border: none;")
        self.botao_som.setFixedSize(30, 30)
        self.botao_som.clicked.connect(self.toggle_som)

        layout_icones = QVBoxLayout()
        layout_icones.addWidget(self.botao_som, alignment=Qt.AlignTop)
        layout_icones.addStretch()

        layout_principal.addLayout(layout_icones, 0)

        self.setLayout(layout_principal)

        self.installEventFilter(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_ouros)
        self.timer.start(1000)

        self.ouros_por_segundo = 0

    def center_window(self):
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize:
            self.atualizar_tamanho_fonte(self.size())
        return super().eventFilter(source, event)

    def atualizar_tamanho_fonte(self, size):
        tamanho_fonte = max(size.width() // 60, 12)
        self.info_panel.label_ouros.setFont(QFont('Karla-Bold', int(tamanho_fonte * 1.5), QFont.Bold))

    def atualizar_ouros(self):
        valor_atual = int(self.info_panel.label_ouros.text().split(": ")[1])
        novo_valor = valor_atual + self.ouros_por_segundo
        self.info_panel.label_ouros.setText(f"Ouro atual: {novo_valor}")
        self.shop.atualizar_estado_botoes()

    def atualizar_estado_botoes(self):
        self.shop.atualizar_estado_botoes()

    def toggle_som(self):
        self.sound = not self.sound
        if self.sound:
            self.botao_som.setIcon(QIcon(os.path.join("resources", "icons", "sound.svg")))
        else:
            self.botao_som.setIcon(QIcon(os.path.join("resources", "icons", "no_sound.svg")))

    def tocar_som(self, tipo):
        player = QMediaPlayer()
        if tipo == 'farm':
            player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join("resources", "sounds", "farm.mp3"))))
        elif tipo == 'buy':
            player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join("resources", "sounds", "buy.mp3"))))
        player.play()
        player.mediaStatusChanged.connect(lambda status, p=player: self.limpar_audio_player(status, p))
        self.audio_players.append(player)

    def limpar_audio_player(self, status, player):
        if status == QMediaPlayer.EndOfMedia:
            self.audio_players.remove(player)
            player.deleteLater()

    def metodo_exemplo(self):
        pass

    def spawn_gift_icon(self):
        if self.gift_icon is not None:
            return

        self.gift_icon = QPushButton(self)
        self.gift_icon.setIcon(QIcon(os.path.join("resources", "icons", "gift.svg")))
        self.gift_icon.setIconSize(self.gift_icon.size())
        self.gift_icon.setStyleSheet("border: none; background: transparent;")
        self.gift_icon.setFixedSize(64, 64)

        x = random.randint(0, self.width() - self.gift_icon.width())
        y = random.randint(0, self.height() - self.gift_icon.height())
        self.gift_icon.move(x, y)
        self.gift_icon.show()
        self.gift_icon.clicked.connect(self.collect_gift)

        QTimer.singleShot(4000, self.remove_gift_icon)

    def remove_gift_icon(self):
        if self.gift_icon is not None:
            self.gift_icon.deleteLater()
            self.gift_icon = None

    def collect_gift(self):
        valor_atual = int(self.info_panel.label_ouros.text().split(": ")[1])
        novo_valor = int(valor_atual * 1.20)
        if valor_atual == 0:
            novo_valor = 100
        self.info_panel.label_ouros.setText(f"Ouro atual: {novo_valor}")
        self.shop.atualizar_estado_botoes()
        self.remove_gift_icon()
        if self.sound:
            self.tocar_som('farm')

    def update_elapsed_time(self):
        self.info_panel.update_elapsed_time()
