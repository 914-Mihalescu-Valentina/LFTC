from SLL import SLL
class SymTable:
    def __init__(self,_m,n=0):
        self.__tbl = [SLL() for _ in range(_m)]
        self.__m =  _m
        self.__n = n
    
    def get_m(self):
        return self.__m

    def get_tbl(self):
        return self.__tbl
    

    def get_n(self):
        return self.__n
    
    def set_m(self,new_m):
        self.__m = new_m

    def set_tbl(self,new_tbl):
        self.__tbl = new_tbl
    

    def set_n(self,new_n):
        self.__n = new_n

    
    def hash_function(self,symbolkey):
        ascii_sum = 0
        for char in symbolkey:
            ascii_sum = ord(char)+ascii_sum
        return ascii_sum % self.get_m()

    def resize_and_rehash(self):
        self.set_m(self.get_m()*2)
        new_tbl = [SLL() for _ in range(self.get_m())]
        for i in range(0,self.get_m()//2):
            currentSLL = self.get_tbl()[i]
            currentNode = currentSLL.head
            while currentNode:
                pos = self.hash_function(currentNode.get_keysymbol())
                new_tbl[pos].insert(currentNode.get_keysymbol())
                currentNode = currentNode.get_next()
        self.set_tbl(new_tbl)
           
        

    def search(self,k):
        pos = self.hash_function(k)
        currentSLL = self.get_tbl()[pos]
        currentNode = currentSLL.head
        while currentNode!= None and currentNode.get_keysymbol()!=k:
            currentNode = currentNode.get_next()
        if currentNode!=None:
            return True
        else:
            return False

    def insert(self,symbolkey):
        pos = self.hash_function(symbolkey)
        currentSLL = self.get_tbl()[pos]
        currentSLL.insert(symbolkey)
        self.set_n(self.get_n()+1)
        if self.get_n()/self.get_m() >0.7:
            self.resize_and_rehash()
    
