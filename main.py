import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QScrollArea, QPushButton, QDialog, QCheckBox, QDialogButtonBox, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEvent, QEasingCurve, pyqtSlot
from PyQt5.QtGui import QFontDatabase, QFont, QIcon, QColor

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
    def __init__(self, texto, parent=None):
        super().__init__(texto, parent)
        self.setFont(QFont('Karla', 16))
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 16px;
                margin: 7px 0;
                border: 1px solid #d9d9d9;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)

        # Adicionar sombra ao botão e ao texto do botão
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(10)
        sombra.setOffset(2, 2)
        sombra.setColor(QColor(0, 0, 0, 75))
        self.setGraphicsEffect(sombra)

        sombra_texto = QGraphicsDropShadowEffect()
        sombra_texto.setBlurRadius(5)
        sombra_texto.setOffset(1, 1)
        sombra_texto.setColor(QColor(0, 0, 0, 75))
        self.setGraphicsEffect(sombra_texto)

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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Carregar fontes Karla
        QFontDatabase.addApplicationFont(os.path.join("resources", "fonts", "Karla", "static", "Karla-Regular.ttf"))
        QFontDatabase.addApplicationFont(os.path.join("resources", "fonts", "Karla", "static", "Karla-Bold.ttf"))

        self.setWindowIcon(QIcon(os.path.join("resources", "icons", "window_game_icon.svg")))  # Definir ícone da janela
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("[ALPHA] 1st Game")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)

        # Layout principal
        layout_principal = QVBoxLayout(self)

        # Layout horizontal para lista e label "Coins"
        layout_horizontal = QHBoxLayout()

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
                background: #4CAF50;
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

        # Adicionar botões à lista
        for i in range(1, 21):
            botao = BotaoAnimado(f"Item {i}")
            botao.clicked.connect(lambda _, b=botao: self.botao_lista_clicado(b))
            layout_area_rolagem.addWidget(botao)

        layout_area_rolagem.addStretch()

        # Label central com o texto "Coins: 0"
        self.label_coins = QLabel("Coins: 0", self)
        self.label_coins.setAlignment(Qt.AlignCenter)
        self.label_coins.setFont(QFont('Karla', 24))
        self.label_coins.setStyleSheet("""
            QLabel {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #56ab2f, stop:1 #a8e063);
                color: white;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 20px;
                border: 1px solid #d9d9d9;
            }
        """)

        # Adicionar sombra ao label "Coins"
        sombra_coins = QGraphicsDropShadowEffect()
        sombra_coins.setBlurRadius(10)
        sombra_coins.setOffset(2, 2)
        sombra_coins.setColor(QColor(0, 0, 0, 75))
        self.label_coins.setGraphicsEffect(sombra_coins)

        # Botão para incrementar o valor de "Coins"
        self.botao_incrementar = BotaoAnimado("Incrementar Coins")
        self.botao_incrementar.setFont(QFont('Karla', 16, QFont.Bold))
        self.botao_incrementar.clicked.connect(self.incrementar_coins)

        # Layout vertical para o texto "Coins", o botão de incrementar e o texto do autor
        layout_vertical_coins = QVBoxLayout()
        layout_vertical_coins.addWidget(self.label_coins)
        layout_vertical_coins.addWidget(self.botao_incrementar, alignment=Qt.AlignCenter)
        layout_vertical_coins.addStretch()  # Adiciona espaço flexível para empurrar o texto do autor para baixo

        # Texto discreto abaixo do botão de incrementar
        self.label_autor = QLabel("Developed by @lucashaetingerr", self)
        self.label_autor.setAlignment(Qt.AlignCenter)
        self.label_autor.setFont(QFont('Karla', 10))
        self.label_autor.setStyleSheet("color: #999; margin-top: 15px; margin-bottom: 7px;")
        layout_vertical_coins.addWidget(self.label_autor, alignment=Qt.AlignBottom)

        # Adicionar sombra ao label "Developed by..."
        sombra_autor = QGraphicsDropShadowEffect()
        sombra_autor.setBlurRadius(10)
        sombra_autor.setOffset(2, 2)
        sombra_autor.setColor(QColor(0, 0, 0, 75))
        self.label_autor.setGraphicsEffect(sombra_autor)

        # Adicionar widgets ao layout horizontal
        layout_horizontal.addWidget(area_rolagem, 1)
        layout_horizontal.addLayout(layout_vertical_coins, 3)

        # Adicionar layout horizontal ao layout principal
        layout_principal.addLayout(layout_horizontal)

        self.setLayout(layout_principal)

        # Botão de configurações
        self.botao_configuracoes = QPushButton(self)
        self.botao_configuracoes.setIcon(QIcon(os.path.join("resources", "icons", "settings.svg")))  # Ajustar caminho do ícone
        self.botao_configuracoes.setIconSize(self.botao_configuracoes.size())
        self.botao_configuracoes.setStyleSheet("border: none;")
        self.botao_configuracoes.setFixedSize(30, 30)
        self.botao_configuracoes.clicked.connect(self.mostrar_janela_configuracoes)

        # Adicionar botão de configurações ao layout principal
        layout_principal.addWidget(self.botao_configuracoes, alignment=Qt.AlignRight)

        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize:
            self.atualizar_tamanho_fonte(self.size())
        return super().eventFilter(source, event)

    def atualizar_tamanho_fonte(self, size):
        # Atualizar tamanho da fonte com base no tamanho da janela
        tamanho_fonte = max(size.width() // 60, 12)
        self.label_coins.setFont(QFont('Karla', int(tamanho_fonte * 1.5)))

    @pyqtSlot(QPushButton)
    def botao_lista_clicado(self, botao):
        # Animação e lógica para o botão da lista quando clicado
        botao.animar()

    @pyqtSlot()
    def incrementar_coins(self):
        # Incrementar o valor de "Coins"
        valor_atual = int(self.label_coins.text().split(": ")[1])
        novo_valor = valor_atual + 1
        self.label_coins.setText(f"Coins: {novo_valor}")

    def mostrar_janela_configuracoes(self):
        # Mostrar janela de configurações
        janela_configuracoes = ConfigDialog()
        janela_configuracoes.setWindowModality(Qt.ApplicationModal)
        janela_configuracoes.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join("resources", "icons", "window_game_icon.svg")))  # Definir ícone da barra de tarefas
    janela_principal = MainWindow()
    janela_principal.show()
    sys.exit(app.exec_())
