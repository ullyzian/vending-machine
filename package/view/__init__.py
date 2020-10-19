from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget

from .display import MainDisplay
from .products import ProductsGrid


class Window(QMainWindow):
    """
    Top level main window view
    It has 2 subviews: ProductsGrid view and MainDisplayView
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Vending Machine")
        self.setFixedSize(800, 600)

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Products
        self.productsMenu = ProductsGrid()
        self.generalLayout.addLayout(self.productsMenu)

        # Display
        self.displayMenu = MainDisplay()
        self.generalLayout.addLayout(self.displayMenu)

    def switchMenu(self, menu: str) -> None:
        """
        Switch windows menu
        :param menu: name
        :return: None
        """
        menus = {
            "empty": 0,
            "currency": 1,
            "paymentType": 2,
            "cash": 3,
            "cashResult": 4,
            "card": 5,
        }
        self.displayMenu.stack.setCurrentIndex(menus[menu])

    def setDisplayText(self, text: str) -> None:
        """
        Sets display information
        :param text: text to display
        :return: None
        """
        self.displayMenu.displayScreen.setPlainText(text)

    def setButtonsEnabled(self, enabled: bool) -> None:
        """
        Disable or enables product buttons
        :param enabled:
        :return: None
        """
        for button in self.productsMenu.productButtons:
            button.setEnabled(enabled)

    def updateChangeTable(self, changeTableValues: dict) -> None:
        """
        Updates change table with given values
        :param changeTableValues: columns and rows
        :return: None
        """
        self.displayMenu.cashPaymentResultMenu.changeDialog.changeTable.updateTable(changeTableValues)

    def updateDenominationsTable(self, denominationsTableValues: dict) -> None:
        """
        Updates denominations table with given values
        :param denominationsTableValues: columns and rows
        :return: None
        """
        self.displayMenu.cashPaymentResultMenu.denominationsDialog.denominationsTable.updateTable(
            denominationsTableValues)

    def resetUI(self) -> None:
        """
        Resets UI
        :return: None
        """
        self.setButtonsEnabled(True)
        self.switchMenu("empty")
        self.setDisplayText("Wybierz produkt")
