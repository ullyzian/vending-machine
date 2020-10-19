from decimal import Decimal, getcontext
from random import randint

from typing import List, Dict, Union

getcontext().prec = 2

class BaseStore:
    """
    Abstract store
    """

    def __init__(self) -> None:
        self.currency = None
        self.denominationValues = None
        self.denominations = []

    def populateStore(self) -> None:
        for value in self.denominationValues:
            self.denominations.append(Denomination(Decimal(value), randint(0, 20), self.currency))

    def __str__(self) -> str:
        return f"<Store: {self.denominations}>"


class StorePLN(BaseStore):
    """
    Store in PLN
    """

    def __init__(self):
        super().__init__()
        self.denominationValues = ["5.00", "2.00", "1.00", "0.50", "0.20", "0.10", "0.05", "0.01"]
        self.currency = "PLN"
        self.populateStore()

    def __str__(self):
        return super().__str__()


class StoreUSD(BaseStore):
    """
    Store in USD
    """

    def __init__(self):
        super().__init__()
        self.denominationValues = ["1.00", "0.50", "0.25", "0.1", "0.05", "0.01"]
        self.currency = "USD"
        self.populateStore()


class StoreEUR(BaseStore):
    """
    Store in EUR
    """

    def __init__(self):
        super().__init__()
        self.denominationValues = ["2.00", "1.00", "0.50", "0.20", "0.10", "0.05", "0.02", "0.01"]
        self.currency = "EUR"
        self.populateStore()


class Product:
    """
    Product representation in a vending machine
    """

    def __init__(self, name: str, price: Decimal, currency: str = "PLN") -> None:
        self.name = name
        self.price = price
        self.base_price = price
        self.currency = currency

    def convertCurrency(self, currency: str) -> str:
        """
        Converts price and currency attributes into given currency equivalent
        :param currency: to which convert
        :return: message about converted currency
        """
        self.currency = currency

        if currency == "PLN":
            self.price = self.base_price
            return "Wybrana wałuta: PLN"
        elif currency == "USD":
            self.price = self.base_price * Decimal("0.26")  # PLN to USD ~= 0.26
            return "Wybrana wałuta: USD"
        elif currency == "EUR":
            self.price = self.base_price * Decimal("0.22")  # PLN to EUR ~= 0.22
            return "Wybrana wałuta: EUR"
        else:
            raise Exception("Invalid currency type")

    def __str__(self) -> str:
        return f"<Product: name={self.name} price={self.price} currency={self.currency}>"


class Denomination:
    """
    Denomination representation in vending machine
    For now, it's just coins
    """

    def __init__(self, value: Decimal, amount: int, currency: str) -> None:
        self.value = value
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return f"<Denomination: value={self.value} amount={self.amount} currency={self.currency}>"

    def __repr__(self):
        return f"<Denomination: value={self.value} amount={self.amount} currency={self.currency}>"


class Model:
    """
    Top level model in vending-machine
    """

    def __init__(self) -> None:
        self.selectedProduct = None
        self.paymentType = None
        self.enteredAmount = Decimal("0.00")
        self.error = None
        self.change = None
        self.store = None
        self.payed = None

    def processCashPayment(self) -> None:
        """
        Processing cash payment
        :return: None
        """
        self.error = None
        if self.enteredAmount < self.selectedProduct.price:
            self.error = "Za mało pieniędzy!"
        change = self.calculateChange()
        if change is not None:
            self.change = self.changeToTable(change)

    @staticmethod
    def getCurrencyStore(currency: str) -> Union[StorePLN, StoreUSD, StoreEUR]:
        """
        Currency store factory
        :param currency: 'PLN', 'USD' or 'EUR'
        :return: store based on given currency
        """

        store = {
            "PLN": StorePLN(),
            "USD": StoreUSD(),
            "EUR": StoreEUR()
        }
        return store[currency]

    @staticmethod
    def changeToTable(change: List[Denomination]) -> Dict[str, List[str]]:
        """
        Converts list of Denominations instances to dict as table view
        :param change: list of denominations
        :return: dict as table view
        """

        table = {
            "value": [],
            "amount": [],
            "currency": []
        }

        for denomination in change:
            table["value"].append(str(denomination.value))
            table["amount"].append(str(denomination.amount))
            table["currency"].append(str(denomination.currency))

        return table

    def calculateChange(self) -> Union[List[Denomination], None]:
        """
        Algorithm which calculates amount and type of denominations
        :return: list of denominations or None if it can't be calculated
        """

        change = []
        toPay = self.enteredAmount - self.selectedProduct.price
        self.payed = toPay
        self.store = self.getCurrencyStore(self.selectedProduct.currency)

        for denomination in self.store.denominations:
            # if sum can already be given then break calculations
            if toPay <= 0:
                break

            # calculates maximum numbers of denominations in current denomination
            numberOfDenominations = int(toPay // denomination.value)

            # if denomination can be given and it exists in store then add
            if 0 < numberOfDenominations <= denomination.amount:
                toPay = toPay - (denomination.value * numberOfDenominations)
                change.append(Denomination(denomination.value, numberOfDenominations, denomination.currency))

        # Display error if change can't be given
        if toPay > 0:
            self.error = "Nie można wydać resztę"
            return None
        else:
            return change

    def reset(self) -> None:
        """
        Reset model
        :return: None
        """

        self.selectedProduct = None
        self.store = None
        self.change = None
        self.enteredAmount = Decimal("0.00")
        self.paymentType = None
        self.error = None
        self.payed = None
