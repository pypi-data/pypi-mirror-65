from __future__ import annotations


class Node:
    def __init__(self, data:int, next: Node = None):
        self.__data:int = data
        self.__next:Node = next

    def __str__(self) -> str:
        s = str(self.__data) + "  "
        if self.__next != None:
            s + str(self.__next)
        return s.strip()

    def getdata(self) -> int:
        return self.__data

    def setnext(self, next: Node):
        self.__next = next

    def getnext(self) -> Node:
        return self.__next

    def __repr__(self):
        return str(self)
