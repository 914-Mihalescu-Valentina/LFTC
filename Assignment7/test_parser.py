import unittest
from src.parser.parser import Item, State, _augment_grammar, _get_canonical_collection
from src.structures.grammar import Grammar


class TestParser(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar("../input/g1.toml")

    def test_augment_grammar(self):
        _augment_grammar(self.grammar)
        self.assertEqual(self.grammar.start,"S'")
        self.assertTrue("S'" in self.grammar.nonterminals)
        self.assertEqual(self.grammar.productions["S'"],[["S"]])

    def test_get_canonical_collection(self):
        canonical_collection = _get_canonical_collection(self.grammar)
        self.assertEqual(canonical_collection,[
            State(closure=[
                Item(nonterminal='S', production=['a', 'A'], current_symbol_idx=0)
            ]),
            State(closure=[
                Item(nonterminal='S', production=['a', 'A'], current_symbol_idx=1),
                Item(nonterminal='A', production=['b', 'A'], current_symbol_idx=0),
                Item(nonterminal='A', production=['c'], current_symbol_idx=0)
            ]),
            State(closure=[
                Item(nonterminal='A', production=['b', 'A'], current_symbol_idx=1),
                Item(nonterminal='A', production=['b', 'A'], current_symbol_idx=0),
                Item(nonterminal='A', production=['c'], current_symbol_idx=0)
            ]),
            State(closure=[
                Item(nonterminal='A', production=['c'], current_symbol_idx=1)
            ]),
            State(closure=[
                Item(nonterminal='S', production=['a', 'A'], current_symbol_idx=2)
            ]),
            State(closure=[
                Item(nonterminal='A', production=['b', 'A'], current_symbol_idx=2)
            ])
        ])
