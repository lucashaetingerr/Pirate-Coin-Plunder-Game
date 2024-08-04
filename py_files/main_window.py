import sys
import os
import random
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect, QMessageBox, QDialogButtonBox, QDialog, QHBoxLayout, QScrollArea, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEvent, QEasingCurve, pyqtSlot, QTimer, QTime, QUrl
from PyQt5.QtGui import QFontDatabase, QFont, QIcon, QColor, QScreen
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication

from py_files.shop import Shop
from py_files.info import InfoPanel
from py_files.settings import ConfigDialog
from py_files.game_data import GameData

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

        # Inicializar o tempo decorrido
        self.elapsed_time = QTime(0, 0, 0)
        self.session_start_time = QTime.currentTime()  # Guardar o tempo de início da sessão

        self.elapsed_timer = QTimer(self)
        self.elapsed_timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_timer.start(1000)

        self.init_ui()

        # Carregar progresso do jogo
        self.load_game_data()

    def init_ui(self):
        self.setWindowTitle("[ALPHA] Pirate Coin Plunder")
        self.setFixedSize(1024, 768)

        layout_principal = QHBoxLayout(self)

        # Criação da área de rolagem para a loja
        scroll_area_shop = QScrollArea(self)
        scroll_area_shop.setWidgetResizable(True)
        scroll_area_shop.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.shop = Shop(self, self.metodo_exemplo)
        scroll_area_shop.setWidget(self.shop)
        layout_principal.addWidget(scroll_area_shop, 1)

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

        # Botão de salvar jogo
        self.botao_salvar = QPushButton(self)
        self.botao_salvar.setIcon(QIcon(os.path.join("resources", "icons", "savegame_icon.svg")))
        self.botao_salvar.setIconSize(self.botao_salvar.size())
        self.botao_salvar.setStyleSheet("border: none;")
        self.botao_salvar.setFixedSize(30, 30)
        self.botao_salvar.clicked.connect(self.salvar_progresso)

        layout_icones = QVBoxLayout()
        layout_icones.addWidget(self.botao_som, alignment=Qt.AlignTop)
        layout_icones.addWidget(self.botao_salvar, alignment=Qt.AlignTop)
        layout_icones.addStretch()

        layout_principal.addLayout(layout_icones, 0)

        self.setLayout(layout_principal)

        self.installEventFilter(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_ouros)
        self.timer.start(1000)

        self.ouros_por_segundo = 0

    def load_game_data(self):
        self.game_data = GameData()
        self.game_data.load('game_save.json')
        self.info_panel.label_ouros.setText(f"Ouro atual: {self.game_data.ouro}")
        self.ouros_por_segundo = self.game_data.ouros_por_segundo
        self.info_panel.label_ouros_por_segundo.setText(f"Rendimento: {self.ouros_por_segundo} ouro/s")
        for botao in self.shop.botoes:
            botao.quantidade_comprada = self.game_data.items.get(botao.nome, 0)
            botao.atualizar_texto()
        self.shop.atualizar_estado_botoes()

        # Carregar e ajustar o tempo decorrido com base no valor salvo
        self.elapsed_time = QTime(0, 0, 0).addSecs(self.game_data.tempo_decorrido)

        # Reiniciar o temporizador para contar a partir do tempo salvo
        self.elapsed_timer.stop()
        self.elapsed_timer.start(1000)

    def update_elapsed_time(self):
        # Calcular o tempo decorrido desde o início da sessão
        session_elapsed_seconds = self.session_start_time.secsTo(QTime.currentTime())

        # Tempo decorrido total é o tempo salvo mais o tempo da sessão atual
        total_elapsed_seconds = self.game_data.tempo_decorrido + session_elapsed_seconds

        # Atualizar o tempo de sessão e o tempo total
        self.info_panel.label_session_time.setText(f"Tempo da Sessão: {QTime(0, 0, 0).addSecs(session_elapsed_seconds).toString('hh:mm:ss')}")
        self.info_panel.label_total_time.setText(f"Tempo Total: {QTime(0, 0, 0).addSecs(total_elapsed_seconds).toString('hh:mm:ss')}")

    def salvar_progresso(self):
        game_data = GameData()
        game_data.ouro = int(self.info_panel.label_ouros.text().split(": ")[1])
        game_data.ouros_por_segundo = self.ouros_por_segundo
        game_data.items = {botao.nome: botao.quantidade_comprada for botao in self.shop.botoes}

        # Calcular o tempo decorrido total para salvar
        session_elapsed_seconds = self.session_start_time.secsTo(QTime.currentTime())
        game_data.tempo_decorrido = self.game_data.tempo_decorrido + session_elapsed_seconds
        game_data.save('game_save.json')

        # Mostrar mensagem de confirmação de salvamento
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Jogo Salvo")
        msg_box.setText("Seu progresso foi salvo com sucesso.")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

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

    def closeEvent(self, event):
        # Diálogo de confirmação ao tentar fechar a janela
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirmação de saída")
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        label = QLabel("Deseja salvar o jogo antes de sair?", dialog)
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Discard | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.salvar_e_sair)
        button_box.button(QDialogButtonBox.Discard).clicked.connect(self.sair_sem_salvar)
        button_box.rejected.connect(dialog.reject)

        dialog.exec_()

        if dialog.result() == QDialog.Accepted:
            event.accept()
        else:
            event.ignore()

    def salvar_e_sair(self):
        self.salvar_progresso()
        QApplication.quit()

    def sair_sem_salvar(self):
        QApplication.quit()
