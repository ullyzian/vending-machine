from functools import partial

from .model import Product, Model
from .view import Window


class Controller:
    """
    Base controller of vending-machine
    """

    def __init__(self, view: Window, model: Model) -> None:
        self.view = view
        self.model = model

        # controller components
        ProductMenuController(self)
        CurrencyMenuController(self)
        PaymentTypeMenuController(self)
        CashPaymentMenuController(self)
        CashResultMenuController(self)


class ProductMenuController:
    """
    Product menu controller
    """

    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.listenSignal()

    def _setMessage(self, name: str) -> None:
        """
        Updates display with selected product
        :param name: name of product
        :return: None
        """
        message = f"Wybrany produkt: {name}!\n" \
                  f"Poproszę wybrać wałutę"
        self.controller.view.setDisplayText(message)

    def _performAction(self, name: str, price: float) -> None:
        """
        Create product instance and make UI changes. Default currency 'PLN'
        :param name: product name
        :param price: product price.
        :return: None
        """

        self.controller.model.selectedProduct = Product(name, price)
        self._setMessage(name)
        self.controller.view.setButtonsEnabled(False)  # Disable buttons
        self.controller.view.switchMenu("currency")  # switch to Currency menu

    def listenSignal(self) -> None:
        """
        Listen fro product selection
        :return: None
        """
        for button in self.controller.view.productsMenu.productButtons:
            button.clicked.connect(
                partial(self._performAction, button.product.name, button.product.price))


class CurrencyMenuController:
    """
    Currency menu controller
    """

    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.listenSignal()

    def _setMessage(self, currencyMessage: str) -> None:
        """
        Updates display with currency selection information
        :param currencyMessage: message
        :return: None
        """
        message = f"{currencyMessage}\n" \
                  f"Wybierz typ płatności"
        self.controller.view.setDisplayText(message)

    def _performAction(self, currency: str) -> None:
        """
        Change product currency and convert old price to new price, based on given currency
        :param currency: 'USD', 'PLN' or 'EUR'
        :return: None
        """
        if self.controller.model.selectedProduct is None:
            raise Exception("Product not initialized")

        message = self.controller.model.selectedProduct.convertCurrency(currency)
        self._setMessage(message)
        self.controller.view.switchMenu("paymentType")  # switch to PaymentType menu

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


class PaymentTypeMenuController:

    """
    Payment type selection menu controller
    """

    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.listenSignal()

    def _setMessage(self) -> None:
        """
        Updates display with prepayment information
        :return:
        """
        message = f"Wybrana wałuta: {self.controller.model.selectedProduct.currency}\n" \
                  f"Cena produktu: {self.controller.model.selectedProduct.price}\n" \
                  f"Wplacona suma: {self.controller.model.enteredAmount}"
        self.controller.view.setDisplayText(message)

    def _performAction(self, paymentType: dict) -> None:
        """
        Get payment type from user
        :param paymentType: Cash or Card
        :return: None
        """

        self.controller.model.paymentType = paymentType["value"]
        self._setMessage()
        if paymentType["value"] == "cash":
            self.controller.view.switchMenu("cash")  # switch to Cash menu
        elif paymentType["value"] == "card":
            self.controller.view.switchMenu("card")  # switch to Card menu
        else:
            raise Exception(f"Invalid payment type given: {paymentType['value']}")

    def listenSignal(self) -> None:
        """
        Listen to payment type selection
        :return: None
        """
        self.controller.view.displayMenu.paymentTypeMenu.buttonPaymentCash.clicked.connect(
            partial(self._performAction, {"name": "gotówka", "value": "cash"}))
        self.controller.view.displayMenu.paymentTypeMenu.buttonPaymentCard.clicked.connect(
            partial(self._performAction, {"name": "karta", "value": "card"}))


class CashPaymentMenuController:
    """
    Cash payment menu controller
    """

    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.listenSignal()

    def _updateMessage(self) -> None:
        """
        Updates display information after certain actions
        :return: None
        """
        message = f"Wybrana wałuta: {self.controller.model.selectedProduct.currency}\n" \
                  f"Cena produktu: {self.controller.model.selectedProduct.price}\n" \
                  f"Wplacona suma: {self.controller.model.enteredAmount}\n" \
                  f"{self.controller.model.error if self.controller.model.error else ''}"
        self.controller.view.setDisplayText(message)

    def _setMessage(self) -> None:
        """
        Updates display with information after payment
        :return: None
        """
        message = f"Wyplacona suma: {self.controller.model.payed}\n" \
                  f"Odbierz produkt\n" \
                  f"Dziękuję"
        self.controller.view.setDisplayText(message)

    def _performAction(self, coinValue: float) -> None:
        """
        Get payment type from user
        :param coinValue: float value of coin representation
        :return: None
        """
        self.controller.model.enteredAmount += coinValue
        self._updateMessage()

    def _processPayment(self) -> None:
        """
        After submitting payment, perform processing
        :return: None
        """

        self.controller.model.processCashPayment()

        # if error occurred, then display it
        if self.controller.model.error is not None:
            self._updateMessage()
        # if change exists, then show post payment page
        elif self.controller.model.change is not None:
            self._setMessage()
            self.controller.view.switchMenu("cashResult")  # switch to Card menu
        else:
            raise Exception("Change attribute doesn't set")

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


class CashResultMenuController:
    """
    Post payment cash result menu controller
    """
    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.listenSignal()

    def _showChangeDialog(self) -> None:
        """
        Shows change table dialog
        :return: None
        """
        changeTableValues = self.controller.model.change
        self.controller.view.updateChangeTable(changeTableValues)

    def _showDenominationsDialog(self) -> None:
        """
        Shows table dialog with available denominations
        :return: None
        """
        denominationsTableValues = self.controller.model.changeToTable(self.controller.model.store.denominations)
        self.controller.view.updateDenominationsTable(denominationsTableValues)

    def _reset(self) -> None:
        """
        Resets view and model
        :return: None
        """
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
