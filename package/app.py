import sys

from PyQt5.QtWidgets import QApplication

from package.controller import Controller
from package.model import Core
from package.view import Window


def run():
    app = QApplication(sys.argv)
    app.processEvents()
    view = Window()
    view.show()
    model = Core()
    Controller(view=view, model=model)
    sys.exit(app.exec_())
