from dataclasses import dataclass


@dataclass
class Item:
    """ An item of the LR(0) parser. """
    nonterminal: str            # the nonterminal on the left-hand side production
    production: list[str]       # the right-hand side of the production
    current_symbol_idx: int     # the symbol of the production that is currently processed (it represents the symbol right after the dot)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        result = f"{self.nonterminal} -> "
        for idx, symbol in enumerate(self.production):
            if idx == self.current_symbol_idx:
                result += '.'
            result += symbol
            if idx < len(self.production) - 1:
                result += ' '
        if self.current_symbol_idx == len(self.production):
            result += '.'
        return result
