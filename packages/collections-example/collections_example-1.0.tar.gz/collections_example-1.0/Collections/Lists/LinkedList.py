from __future__ import annotations
from Collections import Node


class LinkedList:
    def __init__(self, *args:Node):
        self.__head = None
        for node in args:
            self.addnode(node)

    def addnode(self, node:Node):
        if self.__head is None:
            self.__head:Node = node
        else:
            curr = self.__head
            while curr.getnext() is not None:
                curr = curr.getnext()
            curr.setnext(node)

    def __iter__(self) -> LinkedListIter:
        return LinkedListIter(self.__head)

    def __str__(self):
        s = ""
        for node in self:
            s += str(node)+"\n"
        return s


class LinkedListIter:

    def __init__(self, node:Node):
        self.__current = node

    def __iter__(self):
        return self

    def __next__(self) -> Node:
        if self.__current is None:
            raise StopIteration
        else:
            node = self.__current.getdata()
            self.__current = self.__current.getnext()
            return node