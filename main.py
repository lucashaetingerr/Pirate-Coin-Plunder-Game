import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from py_files.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join("resources", "icons", "coin.svg")))
    janela_principal = MainWindow()
    janela_principal.show()
    sys.exit(app.exec_())
