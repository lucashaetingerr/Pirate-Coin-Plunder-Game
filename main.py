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
        # Layout da janela de configurações
        layout = QVBoxLayout(self)

        # Layout para centralizar as opções
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

        # Layout para os botões de dialogo centralizados horizontalmente
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
        # Lógica para aplicar as configurações pode ser adicionada aqui
        self.accept()

class BotaoAnimado(QPushButton):
    def __init__(self, nome, preco, incremento, metodo, icone, parent=None):
        super().__init__(parent)
        self.nome = nome
        self.preco = preco
        self.incremento = incremento
        self.quantidade_comprada = 0
        self.metodo = metodo
        self.icone = icone
        self.font_bold = QFont('Karla-Bold', 16, QFont.Bold)
        self.font_regular = QFont('Karla', 16)
        self.setIcon(QIcon(icone))
        self.setIconSize(QSize(32, 32))
        self.atualizar_texto()
        self.setStyleSheet("""
            QPushButton {
                background-color: #134B70;
                color: white;
                padding: 10px;
                text-align: left;
                margin: 7px 0;
                border: 1px solid #d9d9d9;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #508C9B;
            }
            QPushButton:pressed {
                background-color: #201E43;
            }
        """)

        # Adicionar sombra ao botão
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(10)
        sombra.setOffset(2, 2)
        sombra.setColor(QColor(0, 0, 0, 75))
        self.setGraphicsEffect(sombra)

    def atualizar_texto(self):
        self.setText(f"({self.quantidade_comprada}) {self.nome}\nPreço: {self.preco} ouros\n+{self.incremento} ouro(s)/s")

    def animar(self):
        # Animação para o botão quando clicado
        animacao = QPropertyAnimation(self, b"geometry")
        animacao.setDuration(300)
        animacao.setStartValue(self.geometry())
        animacao.setEndValue(QRect(self.x(), self.y() + 10, self.width(), self.height()))
        animacao.setEasingCurve(QEasingCurve.OutBounce)
        animacao.finished.connect(self.resetar_posicao)
        animacao.start()

    def resetar_posicao(self):
        self.move(self.x(), self.y() - 10)

    def set_bloqueado(self, bloqueado):
        if bloqueado:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #A9A9A9;
                    color: white;
                    padding: 10px;
                    text-align: left;
                    margin: 7px 0;
                    border: 1px solid #d9d9d9;
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background-color: #A9A9A9;
                }
                QPushButton:pressed {
                    background-color: #A9A9A9;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #134B70;
                    color: white;
                    padding: 10px;
                    text-align: left;
                    margin: 7px 0;
                    border: 1px solid #d9d9d9;
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background-color: #508C9B;
                }
                QPushButton:pressed {
                    background-color: #201E43;
                }
            """)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Carregar fontes Karla
        QFontDatabase.addApplicationFont(os.path.join("resources", "fonts", "Karla", "static", "Karla-Regular.ttf"))
        QFontDatabase.addApplicationFont(os.path.join("resources", "fonts", "Karla-Bold", "static", "Karla-Bold.ttf"))

        self.setWindowIcon(QIcon(os.path.join("resources", "icons", "coin.svg")))  # Definir ícone da janela
        self.sound = True  # Variável de controle para o ícone de som
        self.audio_players = []  # Lista para gerenciar players de áudio
        self.gift_icon = None  # Variável para armazenar o ícone de presente
        self.init_ui()

        # Timer para spawnar o ícone de presente
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_gift_icon)
        self.spawn_timer.start(60000)  # 1 minuto

        # Timer para o tempo decorrido
        self.elapsed_timer = QTimer(self)
        self.elapsed_timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_time = QTime(0, 0, 0)  # Inicia o tempo em 0
        self.elapsed_timer.start(1000)

    def init_ui(self):
        self.setWindowTitle("Pirate Coin Plunder")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)

        # Layout principal
        layout_principal = QHBoxLayout(self)

        # Layout da loja (esquerda)
        layout_loja = QVBoxLayout()
        layout_loja.setContentsMargins(10, 10, 10, 10)

        # Título "Loja"
        self.titulo_loja = QLabel("Loja", self)
        self.titulo_loja.setAlignment(Qt.AlignCenter)
        self.titulo_loja.setFont(QFont('Karla-Bold', 24, QFont.Bold))
        self.titulo_loja.setStyleSheet("""
            QLabel {
                color: black;
                margin-bottom: 10px;
            }
        """)
        layout_loja.addWidget(self.titulo_loja)

        # Área de rolagem para a lista de botões
        area_rolagem = QScrollArea(self)
        area_rolagem.setWidgetResizable(True)
        area_rolagem.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin-left: 10px;
            }
            QScrollBar:vertical:hover {
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #134B70;
                border-radius: 6px;
            }
            QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
                height: 0;
                background: none;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none.
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none.
            }
        """)
        conteudo_area_rolagem = QWidget()
        area_rolagem.setWidget(conteudo_area_rolagem)
        layout_area_rolagem = QVBoxLayout(conteudo_area_rolagem)
        layout_area_rolagem.setContentsMargins(0, 0, 0, 0)

        # Dados dos botões
        self.botoes_dados = [
            {"nome": "Navio Pirata", "preco": 10, "incremento": 1, "icone": os.path.join("resources", "icons", "store_icons", "pirate-ship.svg")},
            {"nome": "Baú de Tesouro", "preco": 25, "incremento": 3, "icone": os.path.join("resources", "icons", "store_icons", "treasure-chest.svg")},
            {"nome": "Tripulação de Bucaneiros", "preco": 50, "incremento": 5, "icone": os.path.join("resources", "icons", "store_icons", "pirate-buccaneer.svg")},
            {"nome": "Chapéu do Capitão", "preco": 100, "incremento": 10, "icone": os.path.join("resources", "icons", "store_icons", "pirate-hat.svg")},
            {"nome": "Papagaio", "preco": 200, "incremento": 20, "icone": os.path.join("resources", "icons", "store_icons", "parrot.svg")},
            {"nome": "Canhão", "preco": 400, "incremento": 40, "icone": os.path.join("resources", "icons", "store_icons", "cannon.svg")},
            {"nome": "Mapa do Pirata", "preco": 800, "incremento": 80, "icone": os.path.join("resources", "icons", "store_icons", "pirate-map.svg")},
            {"nome": "Sabre", "preco": 1600, "incremento": 160, "icone": os.path.join("resources", "icons", "store_icons", "saber.svg")},
            {"nome": "Pérola Negra", "preco": 3200, "incremento": 320, "icone": os.path.join("resources", "icons", "store_icons", "pearl.svg")},
            {"nome": "Tesouro Lendário", "preco": 6400, "incremento": 640, "icone": os.path.join("resources", "icons", "store_icons", "legendary-treasure.svg")}
        ]

        # Adicionar botões à lista
        self.botoes = []
        for dados in self.botoes_dados:
            botao = BotaoAnimado(dados['nome'], dados['preco'], dados['incremento'], self.metodo_exemplo, dados['icone'])
            botao.clicked.connect(lambda _, b=botao: self.botao_lista_clicado(b))
            self.botoes.append(botao)
            layout_area_rolagem.addWidget(botao)

        layout_area_rolagem.addStretch()
        layout_loja.addWidget(area_rolagem)

        # Divisória à direita do layout da loja
        divisoria_direita_loja = QFrame(self)
        divisoria_direita_loja.setFrameShape(QFrame.VLine)
        divisoria_direita_loja.setFrameShadow(QFrame.Sunken)
        divisoria_direita_loja.setStyleSheet("color: #d9d9d9;")
        
        layout_principal.addLayout(layout_loja, 1)
        layout_principal.addWidget(divisoria_direita_loja)

        # Layout do jogo (centro)
        layout_jogo = QVBoxLayout()
        layout_jogo.setContentsMargins(10, 10, 10, 10)

        # Frame para informações
        self.frame_informacoes = QFrame(self)
        self.frame_informacoes.setFrameShape(QFrame.StyledPanel)
        self.frame_informacoes.setFrameShadow(QFrame.Raised)
        layout_frame_informacoes = QVBoxLayout(self.frame_informacoes)

        self.label_informacoes = QLabel("Informações", self.frame_informacoes)
        self.label_informacoes.setAlignment(Qt.AlignTop | Qt.AlignCenter)  # Alinhar ao topo
        self.label_informacoes.setFont(QFont('Karla-Bold', 24, QFont.Bold))  # Ajuste o tamanho da fonte aqui
        self.label_informacoes.setStyleSheet("color: black;")
        layout_frame_informacoes.addWidget(self.label_informacoes)
        
        # Label para mostrar o tempo decorrido
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

        # Adicionar sombra ao label "ouros"
        sombra_ouros = QGraphicsDropShadowEffect()
        sombra_ouros.setBlurRadius(10)
        sombra_ouros.setOffset(2, 2)
        sombra_ouros.setColor(QColor(0, 0, 0, 75))
        self.label_ouros.setGraphicsEffect(sombra_ouros)

        layout_jogo.addWidget(self.label_ouros)

        # Frame para ouros por segundo
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
        
        # Adicionar sombra ao frame "Rendimento"
        sombra_rendimento = QGraphicsDropShadowEffect()
        sombra_rendimento.setBlurRadius(10)
        sombra_rendimento.setOffset(2, 2)
        sombra_rendimento.setColor(QColor(0, 0, 0, 75))
        self.frame_ouros_por_segundo.setGraphicsEffect(sombra_rendimento)

        layout_frame_ouros.addWidget(self.label_ouros_por_segundo)
        layout_jogo.addWidget(self.frame_ouros_por_segundo)

        # Botão para incrementar o valor de "ouros" com ícone de moeda
        self.botao_incrementar = QPushButton(self)
        self.botao_incrementar.setIcon(QIcon(os.path.join("resources", "icons", "coin.svg")))
        self.botao_incrementar.setIconSize(QSize(80, 80))  # Aumentar o tamanho do ícone
        self.botao_incrementar.setStyleSheet("border: none; background: transparent;")
        self.botao_incrementar.clicked.connect(self.incrementar_ouros)
        layout_jogo.addWidget(self.botao_incrementar, alignment=Qt.AlignCenter)

        layout_jogo.addStretch()  # Adiciona espaço flexível para empurrar o texto do autor para baixo

        # Texto discreto abaixo do botão de incrementar
        self.label_autor = QLabel("Developed by @lucashaetingerr", self)
        self.label_autor.setAlignment(Qt.AlignCenter)
        self.label_autor.setFont(QFont('Karla-Bold', 10, QFont.Bold))
        self.label_autor.setStyleSheet("color: #999; margin-top: 15px; margin-bottom: 7px;")
        layout_jogo.addWidget(self.label_autor, alignment=Qt.AlignBottom)

        # Adicionar sombra ao label "Developed by..."
        sombra_autor = QGraphicsDropShadowEffect()
        sombra_autor.setBlurRadius(10)
        sombra_autor.setOffset(2, 2)
        sombra_autor.setColor(QColor(0, 0, 0, 75))
        self.label_autor.setGraphicsEffect(sombra_autor)

        layout_principal.addLayout(layout_jogo, 2)

        # Divisória à esquerda do layout de ícones
        divisoria_esquerda_icones = QFrame(self)
        divisoria_esquerda_icones.setFrameShape(QFrame.VLine)
        divisoria_esquerda_icones.setFrameShadow(QFrame.Sunken)
        divisoria_esquerda_icones.setStyleSheet("color: #d9d9d9;")
        
        layout_principal.addWidget(divisoria_esquerda_icones)

        # Botão de configurações
        self.botao_configuracoes = QPushButton(self)
        self.botao_configuracoes.setIcon(QIcon(os.path.join("resources", "icons", "settings.svg")))  # Ajustar caminho do ícone
        self.botao_configuracoes.setIconSize(self.botao_configuracoes.size())
        self.botao_configuracoes.setStyleSheet("border: none;")
        self.botao_configuracoes.setFixedSize(30, 30)
        self.botao_configuracoes.clicked.connect(self.mostrar_janela_configuracoes)

        # Botão de som
        self.botao_som = QPushButton(self)
        self.botao_som.setIcon(QIcon(os.path.join("resources", "icons", "sound.svg")))  # Ajustar caminho do ícone
        self.botao_som.setIconSize(self.botao_som.size())
        self.botao_som.setStyleSheet("border: none;")
        self.botao_som.setFixedSize(30, 30)
        self.botao_som.clicked.connect(self.toggle_som)

        # Layout para ícones
        layout_icones = QVBoxLayout()
        layout_icones.addWidget(self.botao_configuracoes, alignment=Qt.AlignTop)
        layout_icones.addWidget(self.botao_som, alignment=Qt.AlignTop)
        layout_icones.addStretch()

        layout_principal.addLayout(layout_icones, 0)

        self.setLayout(layout_principal)

        self.installEventFilter(self)

        # Timer para atualizar os ouros periodicamente
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_ouros)
        self.timer.start(1000)

        # Variável para armazenar a quantidade de ouros por segundo
        self.ouros_por_segundo = 0

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize:
            self.atualizar_tamanho_fonte(self.size())
        return super().eventFilter(source, event)

    def atualizar_tamanho_fonte(self, size):
        # Atualizar tamanho da fonte com base no tamanho da janela
        tamanho_fonte = max(size.width() // 60, 12)
        self.label_ouros.setFont(QFont('Karla-Bold', int(tamanho_fonte * 1.5), QFont.Bold))

    @pyqtSlot(QPushButton)
    def botao_lista_clicado(self, botao):
        # Animação e lógica para o botão da lista quando clicado
        botao.animar()
        # Lógica para comprar o item se tiver ouros suficientes
        valor_atual = int(self.label_ouros.text().split(": ")[1])
        if valor_atual >= botao.preco:
            valor_atual -= botao.preco
            self.label_ouros.setText(f"Ouro atual: {valor_atual}")
            botao.metodo()
            # Incrementar o valor dos ouros por segundo
            self.ouros_por_segundo += botao.incremento
            self.label_ouros_por_segundo.setText(f"Rendimento: {self.ouros_por_segundo} ouro/s")
            # Incrementar a quantidade comprada
            botao.quantidade_comprada += 1
            # Aumentar o preço do item
            botao.preco += botao.preco // 2  # Aumentar o preço em 50%
            botao.atualizar_texto()
            # Atualizar estado dos botões
            self.atualizar_estado_botoes()
            # Tocar som de compra, se o som estiver ativado
            if self.sound:
                self.tocar_som('buy')

    @pyqtSlot()
    def incrementar_ouros(self):
        # Incrementar o valor de "ouros"
        valor_atual = int(self.label_ouros.text().split(": ")[1])
        novo_valor = valor_atual + 1
        self.label_ouros.setText(f"Ouro atual: {novo_valor}")
        self.atualizar_estado_botoes()
        # Tocar som de farm, se o som estiver ativado
        if self.sound:
            self.tocar_som('farm')

    def atualizar_ouros(self):
        # Atualizar o valor de ouros por segundo
        valor_atual = int(self.label_ouros.text().split(": ")[1])
        novo_valor = valor_atual + self.ouros_por_segundo
        self.label_ouros.setText(f"Ouro atual: {novo_valor}")
        self.atualizar_estado_botoes()

    def atualizar_estado_botoes(self):
        # Atualizar o estado dos botões com base na quantidade de ouros
        valor_atual = int(self.label_ouros.text().split(": ")[1])
        for botao in self.botoes:
            if valor_atual >= botao.preco:
                botao.set_bloqueado(False)
            else:
                botao.set_bloqueado(True)

    def mostrar_janela_configuracoes(self):
        # Mostrar janela de configurações
        janela_configuracoes = ConfigDialog()
        janela_configuracoes.setWindowModality(Qt.ApplicationModal)
        janela_configuracoes.exec_()

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
        print("Item comprado!")

    def spawn_gift_icon(self):
        if self.gift_icon is not None:
            return  # Já existe um gift na tela

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

        # Timer para remover o ícone após 4 segundos
        QTimer.singleShot(4000, self.remove_gift_icon)

    def remove_gift_icon(self):
        if self.gift_icon is not None:
            self.gift_icon.deleteLater()
            self.gift_icon = None

    def collect_gift(self):
        valor_atual = int(self.label_ouros.text().split(": ")[1])
        novo_valor = int(valor_atual * 1.20)
        if valor_atual == 0:
            novo_valor = 100  # Adiciona 100 ouros se o valor atual for zero
        self.label_ouros.setText(f"Ouro atual: {novo_valor}")
        self.atualizar_estado_botoes()
        self.remove_gift_icon()
        # Tocar som de farm, se o som estiver ativado
        if self.sound:
            self.tocar_som('farm')

    def update_elapsed_time(self):
        self.elapsed_time = self.elapsed_time.addSecs(1)
        self.label_tempo.setText(f"Tempo: {self.elapsed_time.toString('hh:mm:ss')}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join("resources", "icons", "coin.svg")))  # Definir ícone da barra de tarefas
    janela_principal = MainWindow()
    janela_principal.show()
    sys.exit(app.exec_())
