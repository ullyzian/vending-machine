import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QStackedLayout, QWidget, QPlainTextEdit, QHBoxLayout, QPushButton, QLabel, \
    QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QComboBox

from package import BASE_DIR, resource_path


class MainDisplay(QVBoxLayout):

    def __init__(self) -> None:
        super().__init__()

        # Align layout
        self.setAlignment(Qt.AlignTop)

        # Display screen
        self.displayScreen = DisplayUI()
        self.addWidget(self.displayScreen)

        # Initialization of menu
        self.stack = QStackedLayout()
        self.emptyMenu = QWidget()
        self.currencySelectMenu = CurrencyUI()
        self.paymentTypeMenu = PaymentTypeUI()
        self.cashPaymentMenu = CashPaymentUI()
        self.cashPaymentResultMenu = CashResultUI()
        self.cardPaymentMenu = CardPaymentUI()

        # Adding menu to stack layout
        self.stack.addWidget(self.emptyMenu)
        self.stack.addWidget(self.currencySelectMenu)
        self.stack.addWidget(self.paymentTypeMenu)
        self.stack.addWidget(self.cashPaymentMenu)
        self.stack.addWidget(self.cashPaymentResultMenu)
        self.stack.addWidget(self.cardPaymentMenu)

        # Adding stack layout to general layout
        self.addLayout(self.stack)


class DisplayUI(QPlainTextEdit):

    def __init__(self) -> None:
        super().__init__()
        self.setPlainText("Wybierz produkt")
        self.setReadOnly(True)
        self.setMaximumHeight(100)
        self.setFont(QFont("Arial", 18))


class CurrencyUI(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.buttonPLN = QPushButton("PLN")
        self.buttonUSD = QPushButton("USD")
        self.buttonEUR = QPushButton("EUR")

        self.layout.addWidget(self.buttonPLN)
        self.layout.addWidget(self.buttonEUR)
        self.layout.addWidget(self.buttonUSD)

        self.setLayout(self.layout)


class PaymentTypeUI(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.buttonPaymentCash = QPushButton("Gotówka")
        self.buttonPaymentCard = QPushButton("Karta")

        self.layout.addWidget(self.buttonPaymentCash)
        self.layout.addWidget(self.buttonPaymentCard)

        self.setLayout(self.layout)


class CashPaymentUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        label = QLabel("Wrzuc monete")
        self.submitButton = QPushButton("Zaplać monetami")
        self.grid = QGridLayout()

        self.buttonCash1 = QPushButton("0.50")
        self.buttonCash2 = QPushButton("1.00")
        self.buttonCash3 = QPushButton("2.00")
        self.buttonCash4 = QPushButton("5.00")

        self.grid.addWidget(self.buttonCash1, 0, 0)
        self.grid.addWidget(self.buttonCash2, 0, 1)
        self.grid.addWidget(self.buttonCash3, 1, 0)
        self.grid.addWidget(self.buttonCash4, 1, 1)

        self.layout.addWidget(label)
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.submitButton)

        self.setLayout(self.layout)

    def setCurrencyButtons(self, currency):
        if currency == "PLN":
            self.buttonsPLN()
        elif currency == "USD":
            self.buttonsUSD()
        elif currency == "EUR":
            self.buttonsEUR()
        else:
            raise ValueError(f"Unknown currency given: {currency}")

    def buttonsPLN(self):
        self.buttonCash1.setText("0.50")
        self.buttonCash2.setText("1.00")
        self.buttonCash3.setText("2.00")
        self.buttonCash4.setText("5.00")

    def buttonsEUR(self):
        self.buttonCash1.setText("0.20")
        self.buttonCash2.setText("0.50")
        self.buttonCash3.setText("1.00")
        self.buttonCash4.setText("2.00")

    def buttonsUSD(self):
        self.buttonCash1.setText("0.10")
        self.buttonCash2.setText("0.25")
        self.buttonCash3.setText("0.50")
        self.buttonCash4.setText("1.00")


class CashResultUI(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        # buttons
        self.buttonChange = QPushButton("Pokaż resztę")
        self.buttonAvaliableDenomninations = QPushButton("Pokaż dostępny nominały")
        self.buttonReset = QPushButton("Wróc do początku")

        # dialogs
        self.changeDialog = ChangeDialog()
        self.denominationsDialog = AvailableDenominationsDialog()

        self.layout.addWidget(self.buttonChange)
        self.layout.addWidget(self.buttonAvaliableDenomninations)
        self.layout.addWidget(self.buttonReset)

        self.setLayout(self.layout)


class ChangeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tablica reszty")
        self.changeTable = TableView({}, 8, 3)


class AvailableDenominationsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tablica nominałów")
        self.denominationsTable = TableView({}, 8, 3)


class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.setMinimumHeight(300)
        self.setMinimumWidth(400)
        self.setVisible(False)

    def updateTable(self, data):
        self.data = data
        self.setData()
        self.setVisible(True)
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)

    def setData(self):
        horHeaders = []
        for n, key in enumerate(self.data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)


class CardPaymentUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.selectLayout = QHBoxLayout()
        self.accountSelect = QComboBox()
        self.cardSelect = QComboBox()

        self.selectLayout.addWidget(self.accountSelect)
        self.selectLayout.addWidget(self.cardSelect)

        self.buttonPayment = QPushButton()
        self.buttonPayment.setMinimumHeight(200)
        self.buttonPayment.setMaximumWidth(200)
        self.buttonPayment.setIcon(QIcon(resource_path('package/assets/utilities/card-payment.png')))
        self.buttonPayment.setIconSize(QSize(200, 200))
        self.buttonReset = QPushButton("Wróc do początku")

        self.layout.addLayout(self.selectLayout)
        self.layout.addWidget(self.buttonPayment)
        self.layout.addWidget(self.buttonReset)
        self.setLayout(self.layout)

    def setAccounts(self, accounts):
        for account in accounts:
            self.accountSelect.addItem(account.fullname, account)
        self.onAccountSelect(self.accountSelect.currentData())

    def onAccountSelect(self, account):
        self.cardSelect.clear()
        for card in account.cards:
            self.cardSelect.addItem(f"{card.accountNumber} {card.balance}{card.currency}", card)
