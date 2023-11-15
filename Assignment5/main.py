from MenuFA import MenuFA
from Pif import Pif
from SymbolTable import SymTable
from Scanner import Scanner
from TestScanner import TestScanner
from FiniteAutomata import FiniteAutomata

def main():
    # pif = Pif()
    # symtbl = SymTable(30)
    # s = Scanner("C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab4\\p1.in","C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab4\\token.in",pif,symtbl)
    # result = s.scan()
    # if result:
    #     print("Lexically correct!")
    #     result[0].toString()
    #     result[1].toString()

    mfa = MenuFA()
    mfa.run()


    # print(fa.getStates())
    # print(fa.getAlphabet())
    # print(fa.getInitialState())
    # print(fa.getFinalStates())
    # print(fa.getTransitions())


   


if __name__ == "__main__":
    main()
