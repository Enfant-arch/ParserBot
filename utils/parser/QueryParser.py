import clr
clr.AddRefernce("ParserOut") 
from Parser.Parser import MyClass


class QP:
    def __init__(self, query:str) -> None:
        self.query = query

    def parser(self) -> None:
        my_instance = MyClass()