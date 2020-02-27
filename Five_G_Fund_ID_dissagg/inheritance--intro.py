class Decimal:
    def __init__(self, number, places):
        self.number = number
        self.places = places


    def __repr__(self):
        return "%{}.2f".format(self.places) % self.number


class Currency(Decimal):
    def __init__(self, symbol,number, places):
        super().__init__(number, places)
        self.symbol = symbol

    def __repr__(self):
        return "{} {}".format(self.symbol,super().__repr__())
        


print(Currency("$",15.6789, 3))