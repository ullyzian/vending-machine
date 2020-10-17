import sys

from PyQt5.QtWidgets import QApplication

from package.view import Window
from package.controller import Controller

def run():
    app = QApplication(sys.argv)
    view = Window()
    view.show()
    Controller(view=view)
    sys.exit(app.exec_())



