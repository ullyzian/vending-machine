import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QWidget, QHBoxLayout, QGridLayout, QPushButton, QVBoxLayout, \
    QLabel, QPlainTextEdit, QStackedLayout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vending Machine")
        self.setFixedSize(800, 600)

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.createStatusBar()
        self.createItemsList()
        self.createMainDisplay()

    def createItemsList(self):
        self.itemsLayout = ItemsGrid()
        self.itemsLayout.setAlignment(Qt.AlignTop)
        self.generalLayout.addLayout(self.itemsLayout)

    def createMainDisplay(self):
        self.displayLayout = MainDisplay()
        self.displayLayout.setAlignment(Qt.AlignTop)
        self.generalLayout.addLayout(self.displayLayout)

    def createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("Status: Ok")
        self.setStatusBar(self.status)

    def setStatusBarText(self, text):
        self.status.showMessage(f"Status: {text}")

    def displayWindow(self, i):
        self.displayLayout.stack.setCurrentIndex(i)


class MainDisplay(QVBoxLayout):

    def __init__(self):
        super().__init__()

        self.displayUi()

        self.stack = QStackedLayout()
        self.currencySelectMenu = QWidget()
        self.paymentTypeMenu = QWidget()

        self.currencySelectUi()
        self.paymentTypeUi()

        self.stack.addWidget(self.currencySelectMenu)
        self.stack.addWidget(self.paymentTypeMenu)

        self.addLayout(self.stack)

    def displayUi(self):
        self.display = QPlainTextEdit("Select product")
        self.display.setReadOnly(True)
        self.display.setMaximumHeight(100)
        self.display.setFont(QFont("Arial", 18))
        self.addWidget(self.display)

    def setDisplayText(self, text):
        self.display.setPlainText(text)
        self.display.setFocus()

    def currencySelectUi(self):
        self.currencySelectLayout = QHBoxLayout()
        self.currencySelectLayout.setAlignment(Qt.AlignTop)
        self.buttonPLN = QPushButton("PLN")
        self.buttonPLN.setMinimumHeight(70)
        self.buttonUSD = QPushButton("USD")
        self.buttonUSD.setMinimumHeight(70)
        self.buttonEUR = QPushButton("EUR")
        self.buttonEUR.setMinimumHeight(70)

        self.currencySelectLayout.addWidget(self.buttonPLN)
        self.currencySelectLayout.addWidget(self.buttonEUR)
        self.currencySelectLayout.addWidget(self.buttonUSD)
        self.currencySelectMenu.setLayout(self.currencySelectLayout)

    def paymentTypeUi(self):
        self.paymentTypelayout = QHBoxLayout()
        self.paymentTypelayout.setAlignment(Qt.AlignTop)
        buttonPayCash = QPushButton("Gotówka")
        buttonPayCash.setMinimumHeight(70)
        buttonPayCreditCard = QPushButton("Karta")
        buttonPayCreditCard.setMinimumHeight(70)

        self.paymentTypelayout.addWidget(buttonPayCash)
        self.paymentTypelayout.addWidget(buttonPayCreditCard)
        self.paymentTypeMenu.setLayout(self.paymentTypelayout)

    # def cardPaymentUi(self):
    #     self.cardPaymentLayout = QHBoxLayout()
    #     buttonPayment = QPushButton()
    #     buttonPayment.setMinimumHeight(200)
    #     buttonPayment.setMaximumWidth(200)
    #     buttonPayment.setIcon(QIcon(os.path.join(BASE_DIR, 'assets/utilities/card-payment.png')))
    #     buttonPayment.setIconSize(QSize(200, 200))
    #     self.cardPaymentLayout.addWidget(buttonPayment)
    #     self.cardPaymentMenu.setLayout(self.cardPaymentLayout)
    #
    # def cashPaymentUi(self):
    #     self.cashPaymentLayout = QVBoxLayout()
    #     label = QLabel("Wrzuc monete")
    #     submit = QPushButton("Zaplać monetami")
    #     submit.setMinimumHeight(40)
    #     grid = QGridLayout()
    #
    #     buttonHalfPLN = QPushButton("0.50")
    #     button1PLN = QPushButton("1.00")
    #     button2PLN = QPushButton("2.00")
    #     button5PLN = QPushButton("5.00")
    #
    #     grid.addWidget(buttonHalfPLN, 0, 0)
    #     grid.addWidget(button1PLN, 0, 1)
    #     grid.addWidget(button2PLN, 1, 0)
    #     grid.addWidget(button5PLN, 1, 1)
    #
    #     self.cashPaymentLayout.addWidget(label)
    #     self.cashPaymentLayout.addLayout(grid)
    #     self.cashPaymentLayout.addWidget(submit)
    #     self.cashPaymentMenu.setLayout(self.cashPaymentLayout)


class ItemsGrid(QGridLayout):

    def __init__(self):
        super().__init__()
        self.buttons = []
        self.items = [
            {
                "position": (1, 1),
                "name": "Kawa",
                "image_url": "assets/products/kawa.jpg",
                "price": 2.00
            },
            {
                "position": (2, 1),
                "name": "Herbata",
                "image_url": "assets/products/tea.jpg",
                "price": 2.00
            },
            {
                "position": (3, 1),
                "name": "Woda",
                "image_url": "assets/products/water.jpeg",
                "price": 1.00
            },
            {
                "position": (1, 2),
                "name": "Snickers",
                "image_url": "assets/products/snickers.jpeg",
                "price": 4.00
            },
            {
                "position": (2, 2),
                "name": "Twix",
                "image_url": "assets/products/twix.png",
                "price": 4.00
            },
            {
                "position": (3, 2),
                "name": "Kitkat",
                "image_url": "assets/products/kitkat.png",
                "price": 4.00
            },
            {
                "position": (1, 3),
                "name": "Cola",
                "image_url": "assets/products/cola.jpeg",
                "price": 5.00
            },
            {
                "position": (2, 3),
                "name": "Sok",
                "image_url": "assets/products/sok.jpg",
                "price": 5.00
            },
            {
                "position": (3, 3),
                "name": "Czipsy",
                "image_url": "assets/products/lays.jpeg",
                "price": 3.00
            }
        ]
        label = QLabel("Wybierz product")
        label.setAlignment(Qt.AlignHCenter)
        self.addWidget(label, 0, 0, 1, 4)
        self.createButtons()

    def disableButtons(self):
        for button in self.buttons:
            button.setEnabled(False)

    def createButtons(self):
        for product in self.items:
            buttonItem = ProductButton(product["name"], product["price"], product["image_url"])
            self.buttons.append(buttonItem)
            self.addWidget(buttonItem, product["position"][0], product["position"][1])


class ProductButton(QPushButton):

    def __init__(self, name, price, imageUrl):
        super().__init__()
        self.setFixedSize(80, 80)
        self.setIcon(QIcon(os.path.join(BASE_DIR, imageUrl)))
        self.setIconSize(QSize(70, 70))
        self.name = name
        self.price = price
