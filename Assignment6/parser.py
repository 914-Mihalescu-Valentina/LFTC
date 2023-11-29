from dataclasses import dataclass
from src.structures.grammar import Grammar


@dataclass
class Item:
    """ An item of the LR(0) parser. """
    nonterminal: str            # the nonterminal on the left-hand side production
    production: list[str]       # the right-hand side of the production
    current_symbol_idx: int     # the symbol of the production that is currently processed (it represents the symbol right after the dot)

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


@dataclass
class State:
    """ A state of the LR(0) parser. """
    closure: list[Item]     # the items within the state

    def __eq__(self, other: "State"):
        if len(self.closure) != len(other.closure):
            return False

        for item in self.closure:
            if item not in other.closure:
                return False

        return True


def _augment_grammar(grammar: Grammar) -> Grammar:
    """ Returns an enhanced grammar of `grammar`.

    Args:
        grammar (Grammar): grammar of the language

    Returns: an augmented grammar of `grammar`
    """
    new_start = f"{grammar.start}'"
    grammar.nonterminals.append(new_start)
    grammar.productions[new_start] = [[grammar.start]]
    grammar.start = new_start
    return grammar


def _get_closure(initial_item: Item, grammar: Grammar) -> list[Item]:
    """ Computes the closure of `initial_item`.

    Args:
        initial_item (Item): the item on which the closure is computed
        grammar (Grammar): an augmented grammar of the language

    Returns: the closure as a list of items
    """
    # init the closure with the initial item
    closure = [initial_item]

    # find all the items and add them to the closure
    while True:
        was_modified = False    # mark that no other item could be found

        for item in closure:
            # skip if the dot is at the end
            if item.current_symbol_idx >= len(item.production):
                continue

            # skip if the symbol right after the dot is a terminal
            symbol = item.production[item.current_symbol_idx]
            if symbol not in grammar.nonterminals:
                continue

            # add the items of the nonterminal with the dot at the beginning
            for production in grammar.productions[symbol]:
                temp_item = Item(symbol, production, 0)
                # add the item if it doesn't already exist
                if temp_item not in closure:
                    # mark that at least one new item was found
                    was_modified = True
                    closure.append(temp_item)

        # break if no other items were found
        if not was_modified:
            break

    return closure


def _goto(state: State, symbol: str, grammar: Grammar) -> None | State:
    """ Performs the goto action on `state` using `symbol`.

    Args:
        state (State): the state on which the goto is performed
        symbol (str): the symbol used in goto
        grammar (Grammar): an augmented grammar of the language

    Returns: the new State if one was found, otherwise None
    """
    # init the closure of the state
    new_closure = []

    # find all the items that have `symbol` right after the dot,
    # compute their closures and add in the state's closure
    for item in state.closure:
        # skip if the dot is at the end
        if item.current_symbol_idx >= len(item.production):
            continue

        # skip if the symbol right after the dot is not `symbol`
        if item.production[item.current_symbol_idx] != symbol:
            continue

        # obtain the new item with the dot shifted to the right
        new_item = Item(item.nonterminal, item.production, item.current_symbol_idx + 1)

        # compute the closure and add its items in the state's closure if they don't already exist
        for elem in _get_closure(new_item, grammar):
            if elem not in new_closure:
                new_closure.append(elem)

    # return None if no state could be constructed
    if len(new_closure) == 0:
        return None

    return State(new_closure)


def _get_canonical_collection(grammar: Grammar) -> list[State]:
    """ Computes the canonical collection of the grammar.

    Args:
        grammar (Grammar): an augmented grammar of the language

    Returns: the canonical collection as a list of states
    """
    # compute the initial state using the start symbol of the augmented grammar
    item = Item(grammar.start, grammar.productions[grammar.start][0], 0)
    state0 = State(_get_closure(item, grammar))

    # init the canonical collection
    canonical_collection = [state0]

    # find all the states and add them to the collection
    while True:
        was_modified = False    # marks that no other state could be found

        # perform `goto` on every state using every terminal / nonterminal
        for state in canonical_collection:
            for symbol in grammar.terminals + grammar.nonterminals:
                temp_state = _goto(state, symbol, grammar)

                # add the state if it is valid and doesn't already exist
                if temp_state is not None and temp_state not in canonical_collection:
                    # mark that at least one new state was found
                    was_modified = True
                    canonical_collection.append(temp_state)

        # break if no other states were found
        if not was_modified:
            break

    return canonical_collection


def parse(syntax_path: str):
    """ Parses the PIF using the syntax described in `syntax_path`.

    The LR(0) parser is used.

    Args:
        syntax_path (str): path to the syntax of the language

    Returns: ?
    """
    # parse syntax and obtain grammar
    grammar = Grammar(syntax_path)

    # enhance the grammar
    grammar = _augment_grammar(grammar)

    # compute canonical collection
    canonical_collection = _get_canonical_collection(grammar)

    # print canonical collection to see if it works :)
    for state in canonical_collection:
        items_str = []
        for item in state.closure:
            items_str.append(str(item))
        print(items_str)
