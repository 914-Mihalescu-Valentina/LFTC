import unittest

from FiniteAutomata import FAException, FiniteAutomata
class TestScanner(unittest.TestCase):
    def test_fa(self):
        fa = FiniteAutomata()
        fa.loadFA("FA.in")
        self.assertEqual(fa.getAlphabet(),["a","b"])
        self.assertEqual(fa.getStates(),['p','q','r'])
        self.assertEqual(fa.getFinalStates(),["r"])
        self.assertEqual(fa.getInitialState(),["p"])
        self.assertEqual(fa.getTransitions(),{('p', 'a'): 'q', ('p', 'b'): 'q', ('q', 'b'): 'r'})
        self.assertEqual(fa.getIsDFA(),True)
        self.assertEqual(fa.checkSequenceAccepted(fa.getInitialState(),"ab",fa.getFinalStates(),fa.getTransitions()),True)
        self.assertEqual(fa.checkSequenceAccepted(fa.getInitialState(),"ba",fa.getFinalStates(),fa.getTransitions()),False)

    def test_fa_error(self):
        fa = FiniteAutomata()
        fa.loadFA("FA2.in")
        self.assertEqual(fa.getTransitions(),{('p', 'a'): ['q', 'r'], ('p', 'b'): 'q', ('q', 'b'): 'r', ('r', 'a'): 'q'})
        self.assertEqual(fa.getIsDFA(),False)
    
    def test_fa_checkFails(self):
        fa = FiniteAutomata()
        fa.initializeFA("FAerr.in")
        self.assertRaises(FAException,fa.checkTransitions)
        self.assertRaises(FAException,fa.checkFinalState)
        self.assertRaises(FAException,fa.checkRedundantState)


   


        