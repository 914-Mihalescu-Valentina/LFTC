from Node import *
class SLL:
    def __init__(self):
        self.__head = None
    
    @property
    def head(self):
        return self.__head
    
    def insert(self,symbolkey):
        new_node = Node(symbolkey)
        new_node.set_next(self.head)
        self.__head = new_node