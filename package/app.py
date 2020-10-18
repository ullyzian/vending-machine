import sys

from PyQt5.QtWidgets import QApplication

from package.view import Window
from package.controller import Controller
from package.model import Model

def run():
    app = QApplication(sys.argv)
    view = Window()
    view.show()
    model = Model()
    Controller(view=view, model=model)
    sys.exit(app.exec_())



