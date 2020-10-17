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
            return "PLN waluta została wybrana"
        elif currency == "USD":
            self.price = self.base_price * 0.26
            return "USD waluta została wybrana"
        elif currency == "EUR":
            self.price = self.base_price * 0.22
            return "EUR waluta została wybrana"
        else:
            raise Exception("Invalid currency type")

    def __str__(self) -> str:
        return f"<Product: name={self.name} price={self.price} currency={self.currency}>"
