from collections import namedtuple

product = namedtuple("Product", ["name", "link", "image_link", "price", "bonusPercent", "bonusAmount", "reviewCount", "seller"])


class Good():
    

    def __init__(self) -> None:
        self._products = set()

    def __len__(self) -> int:
        return len(self._products)
    
    def __add__(self, name, link, price, image_link, bonusPercent, reviewCount, seller, bonusAmount):
        self._products.add(product(name, link, image_link, price, bonusPercent, bonusAmount, reviewCount, seller))

    def __getitem__(self, position) -> product:
        return self._products[position]