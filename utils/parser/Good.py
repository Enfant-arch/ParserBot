from collections import namedtuple

product = namedtuple("Product", ["id", "name", "link", "price", "cachback", "finalPrice"])




class Good:
    def __init__(self)->None:
        self.good = product

    def __len__(self) -> int:
        return len(self.goods)
    
    def __getitem__(self, position) -> product:
        return self.goods[position]

    def __add__(self, id, name, link, price, cachback, finalPrice) -> product:
        self.good.__add__(product(id, name, link, price, cachback, finalPrice))
    