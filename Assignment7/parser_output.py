from queue import Queue
from pathlib import Path
from src.adt.stack import Stack
from src.structures.grammar import Grammar
from dataclasses import dataclass


class ParserOutput:
    """ Represents the output of parsing """

    @dataclass
    class Entry:
        """ Entry in parsing table. """
        symbol: str
        parent: int
        right_sibling: int

    def __init__(self, grammar: Grammar, output_stack: Stack):
        """ Initializes and constructs the parsing table given the grammar and the string of production found in `output_stack`.

        Args:
            grammar (Grammar): grammar of the language
            output_stack (Stack): output stack of LR(0) parser (contains string of productions)
        """
        self.table: list[ParserOutput.Entry] = self._construct(grammar, output_stack)

    def _construct(self, grammar: Grammar, output_stack: Stack) -> list["ParserOutput.Entry"]:
        """ Constructs the parsing table given the grammar and the string of production found in `output_stack`.

        Args:
            grammar (Grammar): grammar of the language
            output_stack (Stack): output stack of LR(0) parser (contains string of productions)

        Returns: the parsing table represented as a list of `ParserOutput.Entry` instances
        """
        q = Queue()
        table: list[ParserOutput.Entry] = []

        symbol, _ = output_stack.top()
        q.put((symbol, 0))

        entry = self.Entry(symbol, -1, -1)
        table.append(entry)

        while not q.empty():
            symbol, idx = q.get()

            if symbol in grammar.nonterminals:
                _, production_no = output_stack.pop(1)[0]
                production = grammar.productions[symbol][production_no]

                for child_idx, child in enumerate(production):
                    entry = self.Entry(child, idx, -1 if child_idx == 0 else len(table) - 1)
                    table.append(entry)

                    q.put((child, len(table) - 1))

        return table

    def dump(self, filepath: str | Path) -> None:
        """ Dumps the parsing table to a file.

        Args:
            filepath (str | Path): path to file
        """
        with open(filepath, 'w') as file:
            file.write(str(self))

    def __str__(self):
        result = ''
        width_table = 65
        no_columns = 4
        width_column = (width_table - 13) // no_columns

        result += ('+' + '-' * (width_column + 2)) * no_columns + '+\n'
        result += f"| {'INDEX':^{width_column}} | {'SYMBOL':^{width_column}} | {'PARENT':^{width_column}} | {'RIGHT SIBLING':^{width_column}} |\n"
        result += ('+' + '-' * (width_column + 2)) * no_columns + '+\n'
        for idx, entry in enumerate(self.table):
            result += f"| {str(idx):<{width_column}} | {entry.symbol:<{width_column}} | {str(entry.parent):>{width_column}} | {str(entry.right_sibling):>{width_column}} |\n"
        result += ('+' + '-' * (width_column + 2)) * no_columns + '+\n'
        return result
