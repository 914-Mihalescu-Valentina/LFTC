from dataclasses import dataclass
from src.parser.item import Item


@dataclass
class State:
    """ A state of the LR(0) parser. """
    closure: set[Item]     # the items within the state

    def __hash__(self):
        return hash(frozenset(self.closure))

    def __str__(self):
        return '{' + ', '.join(str(item) for item in self.closure) + '}'
