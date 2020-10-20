from decimal import Decimal
from functools import partial

from .model import Product, Core
from .view import Window


class Controller:
    """
    Base controller of vending-machine
    """

    def __init__(self, view: Window, model: Core) -> None:
        self.model = model
        self.view = view

        # controller components
        ProductMenuController(self)
        CurrencyMenuController(self)
        PaymentTypeMenuController(self)
        CashPaymentMenuController(self)
        CashResultMenuController(self)
        CardPaymentMenuController(self)


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

    def _performAction(self, name: str, price: Decimal) -> None:
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

    def _setMessage(self) -> None:
        """
        Updates display with currency selection information
        :return: None
        """
        message = f"Wybrana waluta: {self.controller.model.selectedProduct.currency}\n" \
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

        self.controller.model.selectedProduct.convertCurrency(currency)
        self._setMessage()
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

    def _performAction(self, paymentType: str) -> None:
        """
        Get payment type from user
        :param paymentType: Cash or Card
        :return: None
        """
        self._setMessage()
        if paymentType == "cash":
            self.controller.view.displayMenu.cashPaymentMenu.setCurrencyButtons(self.controller.model.selectedProduct.currency)
            self.controller.view.switchMenu("cash")  # switch to Cash menu
        elif paymentType == "card":
            self.controller.view.switchMenu("card")  # switch to Card menu
        else:
            raise Exception(f"Invalid payment type given: {paymentType}")

    def listenSignal(self) -> None:
        """
        Listen to payment type selection
        :return: None
        """
        self.controller.view.displayMenu.paymentTypeMenu.buttonPaymentCash.clicked.connect(
            partial(self._performAction, "cash"))
        self.controller.view.displayMenu.paymentTypeMenu.buttonPaymentCard.clicked.connect(
            partial(self._performAction, "card"))


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

    def _performAction(self, buttonName: str) -> None:
        """
        Get payment type from user
        :param buttonName: name of button
        :return: None
        """
        cashMenu = self.controller.view.displayMenu.cashPaymentMenu
        values = {
            "btn1": cashMenu.buttonCash1.text(),
            "btn2": cashMenu.buttonCash2.text(),
            "btn3": cashMenu.buttonCash3.text(),
            "btn4": cashMenu.buttonCash4.text()
        }
        self.controller.model.insertDenomination(Decimal(values[buttonName]))
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
        cashMenu = self.controller.view.displayMenu.cashPaymentMenu

        cashMenu.buttonCash1.clicked.connect(partial(self._performAction, "btn1"))
        cashMenu.buttonCash2.clicked.connect(partial(self._performAction, "btn2"))
        cashMenu.buttonCash3.clicked.connect(partial(self._performAction, "btn3"))
        cashMenu.buttonCash4.clicked.connect(partial(self._performAction, "btn4"))

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


class CardPaymentMenuController:
    """
    Cash payment menu controller
    """

    def __init__(self, controller: Controller) -> None:
        self.controller = controller
        self.controller.view.displayMenu.cardPaymentMenu.setAccounts(self.controller.model.accounts)
        self.controller.model.selectedAccount = self.controller.view.displayMenu.cardPaymentMenu.accountSelect.currentData()
        self.controller.model.selectedCard = self.controller.view.displayMenu.cardPaymentMenu.cardSelect.currentData()

        self.listenSignal()

    def _reset(self) -> None:
        """
        Resets view and model
        :return: None
        """
        self.controller.view.resetUI()
        self.controller.model.reset()

    def _updateMessage(self) -> None:
        """
        Updates display information after certain actions
        :return: None
        """
        message = f"Wybrana wałuta: {self.controller.model.selectedProduct.currency}\n" \
                  f"Cena produktu: {self.controller.model.selectedProduct.price}\n" \
                  f"{self.controller.model.error if self.controller.model.error else ''}"
        self.controller.view.setDisplayText(message)

    def _setMessage(self) -> None:
        """
        Updates display information after successful payment
        :return: None
        """
        message = f"Zaplacił {self.controller.model.selectedAccount.fullname} kartą: {self.controller.model.selectedCard}\n" \
                  f"Odbierz produkt\n" \
                  f"Dziękuję"
        self.controller.view.setDisplayText(message)

    def _processPayment(self):
        self.controller.model.processCardPayment()
        if self.controller.model.error is not None:
            self._updateMessage()
        else:
            self.controller.view.displayMenu.cardPaymentMenu.buttonPayment.setEnabled(False)
            self.controller.view.displayMenu.cardPaymentMenu.buttonPayment.repaint()
            self._setMessage()

    def _onAccountSelect(self):
        account = self.controller.view.displayMenu.cardPaymentMenu.accountSelect.currentData()
        self.controller.view.displayMenu.cardPaymentMenu.onAccountSelect(account)
        self.controller.model.selectedAccount = account
        self.controller.model.selectedCard = self.controller.view.displayMenu.cardPaymentMenu.cardSelect.currentData()

    def listenSignal(self) -> None:
        """
        Listen to payment type selection
        :return: None
        """
        cardMenu = self.controller.view.displayMenu.cardPaymentMenu
        cardMenu.buttonPayment.clicked.connect(partial(self._processPayment))
        cardMenu.accountSelect.currentIndexChanged.connect(partial(self._onAccountSelect))
        cardMenu.buttonReset.clicked.connect(partial(self._reset))
