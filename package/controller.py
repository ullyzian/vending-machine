from functools import partial
from .view import Window


class Controller:

    def __init__(self, view: Window):
        self._view = view
        self.selectedProduct = {}
        self._selectProduct()
        self._selectCurrency()

    def _buildProductSelection(self, text, name, price):
        self.selectedProduct["name"] = name
        self.selectedProduct["base_price"] = price
        self.selectedProduct["price"] = price
        self.selectedProduct["currency"] = "PLN"
        self._view.displayLayout.setDisplayText(text)
        self._view.itemsLayout.disableButtons()
        self._view.displayWindow(0)

    def _selectProduct(self):
        for buttonItem in self._view.itemsLayout.buttons:
            buttonItem.clicked.connect(
                partial(self._buildProductSelection, f"{buttonItem.name} selected! \nPlease enter currency payment",
                buttonItem.name, buttonItem.price))

    def _convertCurrencyPrice(self, currency):
        self.selectedProduct["currency"] = currency

        if currency == "PLN":
            self.selectedProduct["price"] = self.selectedProduct["base_price"]
            self._view.displayLayout.setDisplayText("PLN waluta została wybrana")
        elif currency == "USD":
            self.selectedProduct["price"] = self.selectedProduct["base_price"] * 0.26
            self._view.displayLayout.setDisplayText("USD waluta została wybrana")
        elif currency == "EUR":
            self.selectedProduct["price"] = self.selectedProduct["base_price"] * 0.22
            self._view.displayLayout.setDisplayText("EUR waluta została wybrana")
        else:
            raise Exception("Invalid currency type")

        self._view.displayWindow(1)

    def _selectCurrency(self):
        self._view.displayLayout.buttonPLN.clicked.connect(partial(self._convertCurrencyPrice, "PLN"))
        self._view.displayLayout.buttonUSD.clicked.connect(partial(self._convertCurrencyPrice, "USD"))
        self._view.displayLayout.buttonEUR.clicked.connect(partial(self._convertCurrencyPrice, "EUR"))


