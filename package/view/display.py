import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QStackedLayout, QWidget, QPlainTextEdit, QHBoxLayout, QPushButton, QLabel, \
    QGridLayout

from package import BASE_DIR


class MainDisplay(QVBoxLayout):

    def __init__(self) -> None:
        super().__init__()

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
        self.cardPaymentMenu = CardPaymentUI()

        # Adding menu to stack layout
        self.stack.addWidget(self.emptyMenu)
        self.stack.addWidget(self.currencySelectMenu)
        self.stack.addWidget(self.paymentTypeMenu)
        self.stack.addWidget(self.cashPaymentMenu)
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
        self.buttonPLN.setMinimumHeight(70)
        self.buttonUSD = QPushButton("USD")
        self.buttonUSD.setMinimumHeight(70)
        self.buttonEUR = QPushButton("EUR")
        self.buttonEUR.setMinimumHeight(70)

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
        self.buttonPaymentCash.setMinimumHeight(70)
        self.buttonPaymentCard = QPushButton("Karta")
        self.buttonPaymentCard.setMinimumHeight(70)

        self.layout.addWidget(self.buttonPaymentCash)
        self.layout.addWidget(self.buttonPaymentCard)

        self.setLayout(self.layout)


class CashPaymentUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        label = QLabel("Wrzuc monete")
        submitButton = QPushButton("Zaplać monetami")
        submitButton.setMinimumHeight(40)
        grid = QGridLayout()

        buttonHalfPLN = QPushButton("0.50")
        button1PLN = QPushButton("1.00")
        button2PLN = QPushButton("2.00")
        button5PLN = QPushButton("5.00")

        grid.addWidget(buttonHalfPLN, 0, 0)
        grid.addWidget(button1PLN, 0, 1)
        grid.addWidget(button2PLN, 1, 0)
        grid.addWidget(button5PLN, 1, 1)

        self.layout.addWidget(label)
        self.layout.addLayout(grid)
        self.layout.addWidget(submitButton)

        self.setLayout(self.layout)


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
