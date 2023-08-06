from __future__ import annotations

class ArrayList:
    def __init__(self, *args):
        self.__data = []
        for data in args:
            self += data

    def getdata(self, index:int):
        if index >= 0 and index < len(self.__data):
            return self.__data[index]
        else:
            return -1

    def __add__(self, data):
        self.__data.append(data)
        return self
        
    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __str__(self):
        return str(self.__data)