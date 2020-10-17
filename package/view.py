import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QWidget, QHBoxLayout, QGridLayout, QPushButton, QVBoxLayout, \
    QLabel, QPlainTextEdit, QStackedLayout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Window(QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Vending Machine")
        self.setFixedSize(800, 600)

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Products
        self.productsMenu = ItemsGrid()
        self.generalLayout.addLayout(self.productsMenu)

        # Display
        self.displayMenu = MainDisplay()
        self.generalLayout.addLayout(self.displayMenu)

        # StatusBar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def setStatusBarText(self, text: str) -> None:
        self.statusBar.showMessage(f"Status: {text}")

    def switchWindow(self, i: int) -> None:
        self.displayMenu.stack.setCurrentIndex(i)


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


class ItemsGrid(QGridLayout):

    def __init__(self) -> None:
        super().__init__()
        self.setAlignment(Qt.AlignTop)

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
        self.buttonsUi()

    def disableButtons(self) -> None:
        for button in self.buttons:
            button.setEnabled(False)

    def buttonsUi(self) -> None:
        for product in self.items:
            buttonItem = ProductButton(product["name"], product["price"], product["image_url"])
            self.buttons.append(buttonItem)
            self.addWidget(buttonItem, product["position"][0], product["position"][1])


class ProductButton(QPushButton):

    def __init__(self, name: str, price: float, imageUrl: str) -> None:
        super().__init__()
        self.setFixedSize(80, 80)
        self.setIcon(QIcon(os.path.join(BASE_DIR, imageUrl)))
        self.setIconSize(QSize(70, 70))
        self.name = name
        self.price = price
