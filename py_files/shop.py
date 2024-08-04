import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, pyqtSlot, QSize
from PyQt5.QtGui import QFontDatabase, QFont, QIcon, QColor

class BotaoAnimado(QPushButton):
    def __init__(self, nome, preco, incremento, metodo, icone, parent=None):
        super().__init__(parent)
        self.nome = nome
        self.preco = preco
        self.incremento = incremento
        self.quantidade_comprada = 0
        self.metodo = metodo
        self.icone = icone
        self.font_bold = QFont('Karla-Bold', 12, QFont.Bold)
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
        self.setFont(self.font_bold)
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


class Shop(QWidget):
    def __init__(self, parent=None, metodo_exemplo=None):
        super().__init__(parent)
        self.metodo_exemplo = metodo_exemplo
        self.main_window = parent

        # Carregar fontes Karla
        QFontDatabase.addApplicationFont(os.path.join("resources", "fonts", "Karla", "static", "Karla-Regular.ttf"))
        QFontDatabase.addApplicationFont(os.path.join("resources", "fonts", "Karla-Bold", "static", "Karla-Bold.ttf"))

        self.init_ui()

    def init_ui(self):
        # Layout da loja
        layout_loja = QVBoxLayout(self)
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

        # Widget de conteúdo para a lista de botões
        conteudo_area_rolagem = QWidget(self)
        layout_area_rolagem = QVBoxLayout(conteudo_area_rolagem)
        layout_area_rolagem.setContentsMargins(0, 0, 0, 0)

        # Dados dos botões
        self.botoes_dados = [
            {"nome": "Navio Pirata", "preco": 10, "incremento": 1, "icone": os.path.join("resources", "icons", "store_icons", "pirate-ship.svg")},
            {"nome": "Baú de Tesouro", "preco": 25, "incremento": 3, "icone": os.path.join("resources", "icons", "store_icons", "treasure-chest.svg")},
            {"nome": "Tripulação", "preco": 50, "incremento": 5, "icone": os.path.join("resources", "icons", "store_icons", "pirate-buccaneer.svg")},
            {"nome": "Chapéu do Capitão", "preco": 100, "incremento": 10, "icone": os.path.join("resources", "icons", "store_icons", "pirate-hat.svg")},
            {"nome": "Papagaio", "preco": 200, "incremento": 20, "icone": os.path.join("resources", "icons", "store_icons", "parrot.svg")},
            {"nome": "Canhão", "preco": 400, "incremento": 40, "icone": os.path.join("resources", "icons", "store_icons", "cannon.svg")},
            {"nome": "Mapa do Pirata", "preco": 800, "incremento": 80, "icone": os.path.join("resources", "icons", "store_icons", "pirate-map.svg")},
            {"nome": "Sabre", "preco": 1600, "incremento": 160, "icone": os.path.join("resources", "icons", "store_icons", "saber.svg")},
            {"nome": "Pérola Negra", "preco": 3200, "incremento": 320, "icone": os.path.join("resources", "icons", "store_icons", "pearl.svg")},
            {"nome": "Tesouro Lendário", "preco": 6400, "incremento": 640, "icone": os.path.join("resources", "icons", "store_icons", "legendary-treasure.svg")},
            # Novos itens em português e únicos
            {"nome": "Fantasma", "preco": 12800, "incremento": 1280, "icone": os.path.join("resources", "icons", "store_icons", "ghost.svg")},
            {"nome": "Pirata Vigarista", "preco": 25600, "incremento": 2560, "icone": os.path.join("resources", "icons", "store_icons", "pirate-vigarista.svg")},
            {"nome": "Kraken", "preco": 51200, "incremento": 5120, "icone": os.path.join("resources", "icons", "store_icons", "kraken.svg")},
            {"nome": "Bandeira Pirata", "preco": 102400, "incremento": 10240, "icone": os.path.join("resources", "icons", "store_icons", "flag.svg")},
            {"nome": "Rum Encantado", "preco": 204800, "incremento": 20480, "icone": os.path.join("resources", "icons", "store_icons", "rum.svg")}
        ]

        # Adicionar botões à lista
        self.botoes = []
        for dados in self.botoes_dados:
            botao = BotaoAnimado(dados['nome'], dados['preco'], dados['incremento'], self.metodo_exemplo, dados['icone'])
            botao.clicked.connect(lambda _, b=botao: self.botao_lista_clicado(b))
            self.botoes.append(botao)
            layout_area_rolagem.addWidget(botao)

        layout_area_rolagem.addStretch()
        layout_loja.addWidget(conteudo_area_rolagem)

        # Atualizar estado dos botões ao iniciar
        self.atualizar_estado_botoes()

    @pyqtSlot(QPushButton)
    def botao_lista_clicado(self, botao):
        botao.animar()
        valor_atual = int(self.main_window.info_panel.label_ouros.text().split(": ")[1])
        if valor_atual >= botao.preco:
            valor_atual -= botao.preco
            self.main_window.info_panel.label_ouros.setText(f"Ouro atual: {valor_atual}")
            botao.metodo()
            self.main_window.ouros_por_segundo += botao.incremento
            self.main_window.info_panel.label_ouros_por_segundo.setText(f"Rendimento: {self.main_window.ouros_por_segundo} ouro/s")
            botao.quantidade_comprada += 1
            botao.preco += botao.preco // 2
            botao.atualizar_texto()
            self.main_window.atualizar_estado_botoes()
            if self.main_window.sound:
                self.main_window.tocar_som('buy')

    def atualizar_estado_botoes(self):
        valor_atual = int(self.main_window.info_panel.label_ouros.text().split(": ")[1])
        for botao in self.botoes:
            if valor_atual >= botao.preco:
                botao.set_bloqueado(False)
            else:
                botao.set_bloqueado(True)
