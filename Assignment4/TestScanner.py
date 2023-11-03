from Pif import Pif
from SymbolTable import SymTable
from Scanner import Scanner
import unittest
from Scanner import LexicalError
class TestScanner(unittest.TestCase):
    def test_scan(self):
        pif1 = Pif()
        symtbl1 = SymTable(30)
        s1 = Scanner("C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\p1.in","C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\token.in",pif1,symtbl1)
        pif1,symtbl1 = s1.scan()
        self.assertEqual(pif1.len(),28)
        self.assertEqual(pif1.getElemOnPos(0),('function',-1))
        self.assertEqual(pif1.getElemOnPos(1),('id',(11,0)))
        self.assertEqual(pif1.getElemOnPos(22),('const',(19,0)))
        self.assertEqual(symtbl1.len(),30)

        pif2 = Pif()
        symtbl2 = SymTable(30)
        s2 = Scanner("C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\p2.in","C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\token.in",pif2,symtbl2)
        pif2,symtbl2 = s2.scan()
        self.assertEqual(pif2.len(),26)
        self.assertEqual(pif2.getElemOnPos(1),('id',(12,0)))
        self.assertEqual(pif2.getElemOnPos(3),('id',(7,0)))
        self.assertEqual(pif2.getElemOnPos(25),(')',-1))
        self.assertEqual(symtbl2.len(),30)

        pif3 = Pif()
        symtbl3 = SymTable(30)
        s3 = Scanner("C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\p3.in","C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\token.in",pif3,symtbl3)
        pif3,symtbl3 = s3.scan()
        self.assertEqual(pif3.len(),31)
        self.assertEqual(pif3.getElemOnPos(1),('id',(13,0)))
        self.assertEqual(pif3.getElemOnPos(5),(':=',-1))
        self.assertEqual(pif3.getElemOnPos(8),('const',(18,0)))
        self.assertEqual(symtbl3.len(),30)

    def test_error(self):
        piferr = Pif()
        symtblerr = SymTable(30)
        piferr = Pif()
        symtblerr = SymTable(30)
        serr = Scanner("C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\perr.in","C:\\Users\\Valentina\\OneDrive\\Documents\\LFTC\\Lab3\\token.in",piferr,symtblerr)
        self.assertEqual(serr.scan(),None)
        
        





        