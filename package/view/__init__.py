from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStatusBar

from .display import MainDisplay
from .products import ItemsGrid


class Window(QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Vending Machine")
        self.setFixedSize(800, 600)

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Products
        self.productsMenu = ItemsGrid()
        self.generalLayout.addLayout(self.productsMenu)

        # Display
        self.displayMenu = MainDisplay()
        self.generalLayout.addLayout(self.displayMenu)

        # StatusBar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def setStatusBarText(self, text: str) -> None:
        self.statusBar.showMessage(f"Status: {text}")

    def switchWindow(self, i: int) -> None:
        self.displayMenu.stack.setCurrentIndex(i)
