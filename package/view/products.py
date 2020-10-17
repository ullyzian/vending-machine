import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton

from package import BASE_DIR


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
