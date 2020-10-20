from dataclasses import dataclass
from decimal import Decimal
from random import randint
from typing import List, Dict, Union, Optional


@dataclass
class Product:
    """
    Product representation in a vending machine
    """
    name: str
    price: Decimal
    currency: str = "PLN"

    def __post_init__(self):
        self.base_price = self.price

    def convertCurrency(self, currency: str) -> None:
        """
        Converts product currency and price based on given currency
        :param currency: USD, PLN or EUR
        :return: None
        """
        self.currency = currency
        self.price = self.getConvertedPrice(currency)

    def getConvertedPrice(self, currency: str) -> Decimal:
        """
        Converts price for given currency
        :param currency:
        :return:
        """
        try:
            price = {
                "PLN": self.base_price.quantize(Decimal('0.01')),
                "USD": (self.base_price * Decimal("0.26")).quantize(Decimal('0.01')),
                "EUR": (self.base_price * Decimal("0.22")).quantize(Decimal('0.01'))
            }
            return price[currency]
        except KeyError:
            raise KeyError(f"Invalid currency type: {currency}")


@dataclass
class Card:
    accountNumber: str
    balance: Decimal
    currency: str

    def pay(self, product: Product) -> None:
        """
        Pay for given price
        :param product: Product
        :return: None
        """
        self.balance = (self.balance - product.getConvertedPrice(self.currency)).quantize(Decimal('0.01'))

    def __str__(self):
        return f"{self.accountNumber} - {float(self.balance)} {self.currency}"


@dataclass
class Account:
    fullname: str
    cards: List[Card]


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


@dataclass
class Denomination:
    """
    Denomination representation in vending machine
    For now, it's just coins
    """
    value: Decimal
    amount: int
    currency: str


def populateAccounts() -> List[Account]:
    accounts = []

    card1 = Card("423746237462", Decimal("200.00"), "PLN")
    account1 = Account("Jan Kawalski", [card1])
    accounts.append(account1)

    card2 = Card("42352465364", Decimal("100.00"), "USD")
    card3 = Card("92378647823", Decimal("25.00"), "EUR")
    account2 = Account("Piotr Maniewski", [card2, card3])
    accounts.append(account2)

    card4 = Card("48723658473623", Decimal("0.00"), "PLN")
    card5 = Card("456745235423423", Decimal("89.00"), "EUR")
    account3 = Account("Leszek Jung", [card4, card5])
    accounts.append(account3)

    return accounts


@dataclass
class Core:
    """
    Top level model in vending-machine
    """
    selectedProduct: Optional[Product] = None
    selectedAccount: Optional[Account] = None
    selectedCard: Optional[Card] = None
    store: Optional[Union[StorePLN, StoreUSD, StoreEUR]] = None
    payed: Optional[Decimal] = None
    error: Optional[str] = None
    change: Optional[Dict[str, List[str]]] = None
    enteredAmount: Decimal = Decimal("0.00")

    def __post_init__(self) -> None:
        self.accounts: List[Account] = populateAccounts()

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

    def processCardPayment(self) -> None:
        self.error = None
        if self.selectedAccount is None:
            self.error = "Error: wybierz konto"
        elif self.selectedCard is None:
            self.error = "Error: wybierz kartę"
        elif self.selectedCard.balance < self.selectedProduct.getConvertedPrice(self.selectedCard.currency):
            self.error = f"Error: nie wystarczy środków na koncie. środki: {self.selectedCard.balance}{self.selectedCard.currency}"
        else:
            self.selectedCard.pay(self.selectedProduct)

    def insertDenomination(self, value: Decimal) -> None:
        self.enteredAmount += value

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

    def calculateChange(self) -> Optional[List[Denomination]]:
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
        self.error = None
        self.payed = None
