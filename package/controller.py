from functools import partial

from .model import Product
from .view import Window


class Controller:

    def __init__(self, view: Window):
        self.view = view
        self.selectedProduct = None
        self.paymentType = None

        # Product menu
        self.productMenu = ProductMenu(self)
        self.productMenu.listenSignal()

        # Currency menu
        self.currencyMenu = CurrencyMenu(self)
        self.currencyMenu.listenSignal()

        # Payment Type menu
        self.paymentTypeMenu = PaymentTypeMenu(self)
        self.paymentTypeMenu.listenSignal()


class ProductMenu:

    def __init__(self, controller: Controller):
        self.controller = controller

    def _performAction(self, message: str, name: str, price: float) -> None:
        """
        Create product instance and make UI changes. Default currency 'PLN'
        :param message: text of display message
        :param name: product name
        :param price: product price.
        :return: None
        """
        self.controller.selectedProduct = Product(name, price)
        self.controller.view.displayMenu.displayScreen.setPlainText(message)  # Update display with selected product
        self.controller.view.productsMenu.disableButtons()  # Disable buttons
        self.controller.view.switchWindow(1)  # switch to Currency menu

    def listenSignal(self) -> None:
        """
        Listen fro product selection
        :return: None
        """
        for productButton in self.controller.view.productsMenu.buttons:
            message = f"{productButton.name} selected! \nPlease enter currency payment"
            productButton.clicked.connect(
                partial(self._performAction, message, productButton.name, productButton.price))


class CurrencyMenu:

    def __init__(self, controller: Controller) -> None:
        self.controller = controller

    def _performAction(self, currency: str) -> None:
        """
        Change product currency and convert old price to new price, based on given currency
        :param currency: 'USD', 'PLN' or 'EUR'
        :return: None
        """
        if self.controller.selectedProduct is None:
            raise Exception("Product not initialized")
        self.controller.view.displayMenu.displayScreen.setPlainText(self.controller.selectedProduct.convertCurrency(currency))
        self.controller.view.switchWindow(2)  # switch to PaymentType menu

    def listenSignal(self) -> None:
        """
        Listen to currency selection
        :return: None
        """
        self.controller.view.displayMenu.currencySelectMenu.buttonPLN.clicked.connect(
            partial(self._performAction, "PLN"))
        self.controller.view.displayMenu.currencySelectMenu.buttonUSD.clicked.connect(
            partial(self._performAction, "USD"))
        self.controller.view.displayMenu.currencySelectMenu.buttonEUR.clicked.connect(
            partial(self._performAction, "EUR"))


class PaymentTypeMenu:

    def __init__(self, controller: Controller) -> None:
        self.controller = controller

    def _performAction(self, paymentType: dict) -> None:
        """
        Get payment type from user
        :param paymentType: Cash or Card
        :return: None
        """
        self.controller.paymentType = paymentType["value"]
        message = f"Wybrany typ platności: {paymentType['name']}"
        self.controller.view.displayMenu.displayScreen.setPlainText(message)
        if paymentType["value"] == "cash":
            self.controller.view.switchWindow(3)  # switch to Cash menu
        elif paymentType["value"] == "card":
            self.controller.view.switchWindow(4)  # switch to Card menu

    def listenSignal(self) -> None:
        """
        Listen to payment type selection
        :return: None
        """
        self.controller.view.displayMenu.paymentTypeMenu.buttonPaymentCash.clicked.connect(
            partial(self._performAction, {"name": "gotówka", "value": "cash"}))
        self.controller.view.displayMenu.paymentTypeMenu.buttonPaymentCard.clicked.connect(
            partial(self._performAction, {"name": "karta", "value": "card"}))
