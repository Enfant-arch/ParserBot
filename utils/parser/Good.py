from collections import namedtuple

product = namedtuple("Product", ["name", "link", "price", "bonusPercent", "bonusAmount"])


class Good():
    

    def __init__(self) -> None:
        self._products = list()

    def __len__(self) -> int:
        return len(self._products)
    
    def __add__(self, name, link, price,  bonusPercent, bonusAmount):
        self._products.append(product(name, link, price,  bonusPercent, bonusAmount))

    def __getitem__(self, position) -> product:
        return self._products[position]