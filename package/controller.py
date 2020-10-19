from functools import partial

from .model import Product, Model
from .view import Window


class Controller:

    def __init__(self, view: Window, model: Model) -> None:
        self.view = view
        self.model = model
        self.selectedProduct = None
        self.paymentType = None

        ProductMenu(self)
        CurrencyMenu(self)
        PaymentTypeMenu(self)
        CashPaymentMenu(self)
        CashResultMenu(self)


class ProductMenu:

    def __init__(self, controller: Controller):
        self.controller = controller
        self.listenSignal()

    def _performAction(self, name: str, price: float) -> None:
        """
        Create product instance and make UI changes. Default currency 'PLN'
        :param message: text of display message
        :param name: product name
        :param price: product price.
        :return: None
        """
        message = f"Wybrany produkt: {name}!\n" \
                  f"Poproszę wybrać wałutę"
        self.controller.model.selectedProduct = Product(name, price)
        self.controller.view.displayMenu.displayScreen.setPlainText(message)  # Update display with selected product
        self.controller.view.productsMenu.disableButtons()  # Disable buttons
        self.controller.view.switchWindow(1)  # switch to Currency menu

    def listenSignal(self) -> None:
        """
        Listen fro product selection
        :return: None
        """
        for productButton in self.controller.view.productsMenu.buttons:
            productButton.clicked.connect(
                partial(self._performAction, productButton.name, productButton.price))


class CurrencyMenu:

    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.listenSignal()

    def _performAction(self, currency: str) -> None:
        """
        Change product currency and convert old price to new price, based on given currency
        :param currency: 'USD', 'PLN' or 'EUR'
        :return: None
        """
        if self.controller.model.selectedProduct is None:
            raise Exception("Product not initialized")
        message = f"{self.controller.model.selectedProduct.convertCurrency(currency)}\n" \
                  f"Wybierz typ płatności"
        self.controller.view.displayMenu.displayScreen.setPlainText(message)
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
        self.listenSignal()

    def _performAction(self, paymentType: dict) -> None:
        """
        Get payment type from user
        :param paymentType: Cash or Card
        :return: None
        """
        self.controller.model.paymentType = paymentType["value"]
        message = f"Wybrana wałuta: {self.controller.model.selectedProduct.currency}\n" \
                  f"Cena produktu: {self.controller.model.selectedProduct.price}\n" \
                  f"Wplacona suma: {self.controller.model.enteredAmount}"
        self.controller.view.displayMenu.displayScreen.setPlainText(message)
        if paymentType["value"] == "cash":
            self.controller.view.switchWindow(3)  # switch to Cash menu
        elif paymentType["value"] == "card":
            self.controller.view.switchWindow(5)  # switch to Card menu

    def listenSignal(self) -> None:
        """
        Listen to payment type selection
        :return: None
        """
        self.controller.view.displayMenu.paymentTypeMenu.buttonPaymentCash.clicked.connect(
            partial(self._performAction, {"name": "gotówka", "value": "cash"}))
        self.controller.view.displayMenu.paymentTypeMenu.buttonPaymentCard.clicked.connect(
            partial(self._performAction, {"name": "karta", "value": "card"}))


class CashPaymentMenu:

    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.listenSignal()

    def _performAction(self, coinValue: float) -> None:
        """
        Get payment type from user
        :param coinValue: float value of coin representation
        :return: None
        """
        self.controller.model.enteredAmount += coinValue
        message = f"Wybrana wałuta: {self.controller.model.selectedProduct.currency}\n" \
                  f"Cena produktu: {self.controller.model.selectedProduct.price}\n" \
                  f"Wplacona suma: {self.controller.model.enteredAmount}"
        self.controller.view.displayMenu.displayScreen.setPlainText(message)

    def _processPayment(self):
        self.controller.model.processCashPayment()
        if self.controller.model.error is not None:
            self.controller.view.displayMenu.displayScreen.appendPlainText(self.controller.model.error)
        elif self.controller.model.change is not None:
            message = f"Wyplacona suma: {self.controller.model.payed}\n" \
                      f"Odbierz produkt\nDziękuję"
            self.controller.view.displayMenu.displayScreen.setPlainText(message)
            self.controller.view.switchWindow(4)  # switch to Card menu

    def listenSignal(self) -> None:
        """
        Listen to payment type selection
        :return: None
        """
        self.controller.view.displayMenu.cashPaymentMenu.buttonHalfPrice.clicked.connect(
            partial(self._performAction, 0.50))
        self.controller.view.displayMenu.cashPaymentMenu.button1Price.clicked.connect(
            partial(self._performAction, 1.00))
        self.controller.view.displayMenu.cashPaymentMenu.button2Price.clicked.connect(
            partial(self._performAction, 2.00))
        self.controller.view.displayMenu.cashPaymentMenu.button5Price.clicked.connect(
            partial(self._performAction, 5.00))

        # submit
        self.controller.view.displayMenu.cashPaymentMenu.submitButton.clicked.connect(
            partial(self._processPayment)
        )


class CashResultMenu:
    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.listenSignal()

    def _showChangeDialog(self):
        self.controller.view.displayMenu.cashPaymentResultMenu.changeDialog.changeTable.updateTable(
            self.controller.model.change)

    def _showDenominationsDialog(self):
        denominations = self.controller.model.store.denominations
        self.controller.view.displayMenu.cashPaymentResultMenu.denominationsDialog.denominationsTable.updateTable(
            self.controller.model.changeToTable(denominations))

    def _reset(self):
        self.controller.view.resetUI()
        self.controller.model.reset()

    def listenSignal(self) -> None:
        """
        Listen to payment type selection
        :return: None
        """
        self.controller.view.displayMenu.cashPaymentResultMenu.buttonChange.clicked.connect(
            partial(self._showChangeDialog))
        self.controller.view.displayMenu.cashPaymentResultMenu.buttonAvaliableDenomninations.clicked.connect(
            partial(self._showDenominationsDialog))
        self.controller.view.displayMenu.cashPaymentResultMenu.buttonReset.clicked.connect(
            partial(self._reset))
