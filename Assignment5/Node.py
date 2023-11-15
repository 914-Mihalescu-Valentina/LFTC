class Node:
    def __init__(self,_symbol,_next=None):
        self.__keysymbol = _symbol
        self.__next = _next

    def get_keysymbol(self):
        return self.__keysymbol
    
    def get_next(self):
        return self.__next
    
    def set_keysymbol(self, new_symbol):
        self.__keysymbol = new_symbol

    def set_next(self, new_next):
        self.__next = new_next