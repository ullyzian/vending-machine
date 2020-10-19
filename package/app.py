import sys
from decimal import getcontext

from PyQt5.QtWidgets import QApplication

from package.controller import Controller
from package.model import Model
from package.view import Window

getcontext().prec = 2

def run():
    app = QApplication(sys.argv)
    view = Window()
    view.show()
    model = Model()
    Controller(view=view, model=model)
    sys.exit(app.exec_())



