from collections import namedtuple

product = namedtuple("Product", ["id", "name", "link", "price", "cachback", "finalPrice"])


class Good():
    

    def __init__(self) -> None:
        self._products = list()
    def __len__(self) -> int:
        return len(self._products)
    
    def __add__(self, id, name, link, price, cachback, finalPrice):
        self._products.append(product(id,name,link,price,cachback,finalPrice))

    def __getitem__(self, position) -> product:
        return self._products[position]