from decimal import Decimal
from random import randint


class Product:

    def __init__(self, name: str, price: float, currency: str = "PLN") -> None:
        self.name = name
        self.price = price
        self.base_price = price
        self.currency = currency

    def convertCurrency(self, currency: str) -> str:
        self.currency = currency

        if currency == "PLN":
            self.price = self.base_price
            return "Wybrana wałuta: PLN"
        elif currency == "USD":
            self.price = self.base_price * 0.26
            return "Wybrana wałuta: USD"
        elif currency == "EUR":
            self.price = self.base_price * 0.22
            return "Wybrana wałuta: EUR"
        else:
            raise Exception("Invalid currency type")

    def __str__(self) -> str:
        return f"<Product: name={self.name} price={self.price} currency={self.currency}>"


class Denomination:

    def __init__(self, value: float, amount: int, currency: str) -> None:
        self.value = value
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return f"<Denomination: value={self.value} amount={self.amount} currency={self.currency}>"

    def __repr__(self):
        return f"<Denomination: value={self.value} amount={self.amount} currency={self.currency}>"


class Model:
    selectedProduct = None
    paymentType = None
    enteredAmount = 0.00
    error = None

    def processCashPayment(self):
        if self.enteredAmount < self.selectedProduct.price:
            self.error = "Za mało pieniędzy!"

        print(self.calculateChange())

    def _getCurrencyStore(self, currency: str):
        store = {
            "PLN": StorePLN(),
            "USD": StoreUSD(),
            "EUR": StoreEUR()
        }
        return store[currency]

    def calculateChange(self):
        changeInDenominations = []
        print(self.selectedProduct.price)
        print(self.enteredAmount)
        toBePaid = float(Decimal(str(self.enteredAmount)) - Decimal(str(self.selectedProduct.price)))
        store = self._getCurrencyStore(self.selectedProduct.currency)

        for denomination in store.denominations:
            print(f"To pay: {toBePaid}")
            print(f"Denomination: {denomination}")
            if toBePaid <= 0:
                break
            numberOfDenominations = int(Decimal(str(toBePaid)) // Decimal(str(denomination.value)))
            print(f"{numberOfDenominations}")

            if 0 < numberOfDenominations <= denomination.amount:
                toBePaid = float(Decimal(str(toBePaid)) - Decimal(str(denomination.value * numberOfDenominations)))
                changeInDenominations.append(
                    Denomination(denomination.value, numberOfDenominations, denomination.currency))

        if toBePaid > 0:
            self.error = "Nie można wydać resztę"
        else:
            return changeInDenominations


class BaseStore:

    def __init__(self):
        self.currency = None
        self.denominationValues = None
        self.denominations = []

    def populateStore(self):
        for value in self.denominationValues:
            self.denominations.append(Denomination(value, randint(0, 20), self.currency))

    def canChangeBeGiven(self, productPrice: float, enteredAmount: float) -> bool:
        pass

    def __str__(self):
        return f"<Store: {self.denominations}>"


class StorePLN(BaseStore):

    def __init__(self):
        super().__init__()
        self.denominationValues = [5.00, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.01]
        self.currency = "PLN"
        self.populateStore()

    def __str__(self):
        return super().__str__()


class StoreUSD(BaseStore):

    def __init__(self):
        super().__init__()
        self.denominationValues = [1.0, 0.5, 0.25, 0.1, 0.05, 0.01]
        self.currency = "USD"
        self.populateStore()


class StoreEUR(BaseStore):

    def __init__(self):
        super().__init__()
        self.denominationValues = [2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
        self.currency = "EUR"
        self.populateStore()
