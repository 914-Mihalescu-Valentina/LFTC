from Pif import Pif
from SymbolTable import SymTable
from Scanner import Scanner
from TestScanner import TestScanner


def main():
    pif = Pif()
    symtbl = SymTable(30)
    s = Scanner("C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\perr.in","C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\token.in",pif,symtbl)
    result = s.scan()
    if result:
        print("Lexically correct!")
        result[0].toString()
        result[1].toString()

if __name__ == "__main__":
    main()
