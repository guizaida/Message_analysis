import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from SqlupdataGui import Ui_MainWindow

class AppWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())