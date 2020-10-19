import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QStackedLayout, QWidget, QPlainTextEdit, QHBoxLayout, QPushButton, QLabel, \
    QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QDialog

from package import BASE_DIR


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
        grid = QGridLayout()

        self.buttonHalfPrice = QPushButton("0.50")
        self.button1Price = QPushButton("1.00")
        self.button2Price = QPushButton("2.00")
        self.button5Price = QPushButton("5.00")

        grid.addWidget(self.buttonHalfPrice, 0, 0)
        grid.addWidget(self.button1Price, 0, 1)
        grid.addWidget(self.button2Price, 1, 0)
        grid.addWidget(self.button5Price, 1, 1)

        self.layout.addWidget(label)
        self.layout.addLayout(grid)
        self.layout.addWidget(self.submitButton)

        self.setLayout(self.layout)


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
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        buttonPayment = QPushButton()
        buttonPayment.setMinimumHeight(200)
        buttonPayment.setMaximumWidth(200)
        buttonPayment.setIcon(QIcon(os.path.join(BASE_DIR, 'assets/utilities/card-payment.png')))
        buttonPayment.setIconSize(QSize(200, 200))

        self.layout.addWidget(buttonPayment)
        self.setLayout(self.layout)
