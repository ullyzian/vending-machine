import os
from decimal import Decimal

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton

from package import BASE_DIR
from package.model import Product


class ProductsGrid(QGridLayout):
    items = [
        {
            "position": (1, 1),
            "name": "Kawa",
            "image_url": "assets/products/kawa.jpg",
            "price": Decimal("2.00")
        },
        {
            "position": (2, 1),
            "name": "Herbata",
            "image_url": "assets/products/tea.jpg",
            "price": Decimal("2.00")
        },
        {
            "position": (3, 1),
            "name": "Woda",
            "image_url": "assets/products/water.jpeg",
            "price": Decimal("1.00")
        },
        {
            "position": (1, 2),
            "name": "Snickers",
            "image_url": "assets/products/snickers.jpeg",
            "price": Decimal("4.00")
        },
        {
            "position": (2, 2),
            "name": "Twix",
            "image_url": "assets/products/twix.png",
            "price": Decimal("4.00")
        },
        {
            "position": (3, 2),
            "name": "Kitkat",
            "image_url": "assets/products/kitkat.png",
            "price": Decimal("4.00")
        },
        {
            "position": (1, 3),
            "name": "Cola",
            "image_url": "assets/products/cola.jpeg",
            "price": Decimal("5.00")
        },
        {
            "position": (2, 3),
            "name": "Sok",
            "image_url": "assets/products/sok.jpg",
            "price": Decimal("5.00")
        },
        {
            "position": (3, 3),
            "name": "Czipsy",
            "image_url": "assets/products/lays.jpeg",
            "price": Decimal("3.00")
        }
    ]

    def __init__(self) -> None:
        super().__init__()
        self.setAlignment(Qt.AlignTop)
        label = QLabel("Wybierz product")
        label.setAlignment(Qt.AlignHCenter)
        self.addWidget(label, 0, 0, 1, 4)

        self.productButtons = []
        self.buttonsUi()

    def buttonsUi(self) -> None:
        for product in self.items:
            buttonItem = ProductButton(product["name"], product["price"], product["image_url"])
            self.productButtons.append(buttonItem)
            self.addWidget(buttonItem, product["position"][0], product["position"][1])


class ProductButton(QPushButton):

    def __init__(self, name: str, price: Decimal, imageUrl: str) -> None:
        super().__init__()
        self.setFixedSize(80, 80)
        self.setIcon(QIcon(os.path.join(BASE_DIR, imageUrl)))
        self.setIconSize(QSize(70, 70))
        self.product = Product(name, price)
