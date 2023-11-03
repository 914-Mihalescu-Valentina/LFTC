class Pif:
     def __init__(self):
          self.__pif = []

     def add(self,token,pair_values):
          self.__pif.append((token, pair_values))

     def toString(self):
          print("Token     ST_Pos")
          print("-----------------")
          for token,pair_values in self.__pif:
               print(f"{token}     {pair_values}")
     
     def len(self):
          return len(self.__pif)
     
     def getElemOnPos(self,pos):
          return self.__pif[pos]




    

