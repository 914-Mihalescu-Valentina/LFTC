from pathlib import Path
from src.adt.stack import Stack
from src.errors import GrammarError
from src.parser.action import Action, Accept, Reduce, Shift
from src.parser.configuration import Configuration
from src.parser.item import Item
from src.parser.parser_output import ParserOutput
from src.parser.state import State
from src.structures.grammar import Grammar
from src.structures.pif import ProgramInternalForm


class Parser:
    """ LR(0) parser. """

    def __init__(self, grammar_path: str | Path):
        """ Initializes the parser with the given grammar.

        Args:
            grammar_path (str | Path): path to grammar description
        """
        # read grammar
        self.__grammar = Grammar(grammar_path)

        # augment the grammar
        self.__grammar = self._augment_grammar(self.__grammar)

        # compute canonical collection
        canonical_collection = self._get_canonical_collection()

        # generate parsing table
        self.__table = self._generate_parsing_table(canonical_collection)

        # # print canonical collection to see if it works :)
        # for state in canonical_collection:
        #     items_str = []
        #     for item in state.closure:
        #         items_str.append(str(item))
        #
        #     result = ',\n'.join(f"\t{i}" for i in items_str)
        #     print(f"[\n{result}\n]\n")

        # print(f"States:")
        # for idx, state in enumerate(self.__table.keys()):
        #     print(f"\t{idx}: {state}")
        # print()
        #
        # for state, action in self.__table.items():
        #     print(f"- {list(self.__table.keys()).index(state)}: ", end='')
        #     if isinstance(action, Accept):
        #         print("accept")
        #     elif isinstance(action, Reduce):
        #         print(f"reduce {action.nonterminal}_{action.production_no}")
        #     elif isinstance(action, Shift):
        #         print(f"shift: {dict(map(lambda x: (x[0], list(self.__table.keys()).index(x[1])), action.goto.items()))}")
        #     else:
        #         print(f"wtf")
        #     print()

    def parse(self, pif: ProgramInternalForm) -> ParserOutput:
        """ Parses the PIF using the syntax described in `syntax_path`.

        The LR(0) parser is used.
        """
        # find initial state
        initial_state = None
        for state in self.__table.keys():
            if Item(self.__grammar.start, self.__grammar.productions[self.__grammar.start][0], 0) in state.closure:
                initial_state = state
                break

        # create initial configuration
        config = Configuration(Stack([initial_state]), Stack(pif.pairs[::-1]), Stack())

        # start parsing
        while True:
            state = config.working_stack.top()
            action = self.__table[state]

            # apply action on current configuration
            if isinstance(action, Shift):
                action.apply(config)
            elif isinstance(action, Reduce):
                action.apply(config, self.__table)
            elif isinstance(action, Accept):
                action.apply(config)
                break
            else:
                # this should not happen
                assert False

        return ParserOutput(self.__grammar, config.output_stack)

    @classmethod
    def _augment_grammar(cls, grammar: Grammar) -> Grammar:
        """ Returns an augmented grammar of `grammar`.

        Args:
            grammar (Grammar): grammar of the language

        Returns: an augmented grammar of `grammar`
        """
        new_start = f"{grammar.start}'"
        grammar.nonterminals.append(new_start)
        grammar.productions[new_start] = [[grammar.start]]
        grammar.start = new_start
        return grammar

    def _get_closure(self, initial_item: Item) -> set[Item]:
        """ Computes the closure of `initial_item`.

        Args:
            initial_item (Item): the item on which the closure is computed

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
                if symbol not in self.__grammar.nonterminals:
                    continue

                # add the items of the nonterminal with the dot at the beginning
                for production in self.__grammar.productions[symbol]:
                    temp_item = Item(symbol, production, 0)
                    # add the item if it doesn't already exist
                    if temp_item not in closure:
                        # mark that at least one new item was found
                        was_modified = True
                        closure.append(temp_item)

            # break if no other items were found
            if not was_modified:
                break

        return set(closure)

    def _goto(self, state: State, symbol: str) -> None | State:
        """ Performs the goto action on `state` using `symbol`.

        Args:
            state (State): the state on which the goto is performed
            symbol (str): the symbol used in goto

        Returns: the new State if one was found, otherwise None
        """
        # init the closure of the state
        new_closure = set()

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
            for elem in self._get_closure(new_item):
                if elem not in new_closure:
                    new_closure.add(elem)

        # return None if no state could be constructed
        if len(new_closure) == 0:
            return None

        return State(new_closure)

    def _get_canonical_collection(self) -> set[State]:
        """ Computes the canonical collection of the grammar.

        Returns: the canonical collection as a list of states
        """
        # compute the initial state using the start symbol of the augmented grammar
        item = Item(self.__grammar.start, self.__grammar.productions[self.__grammar.start][0], 0)
        state0 = State(self._get_closure(item))

        # init the canonical collection
        canonical_collection = [state0]

        # find all the states and add them to the collection
        while True:
            was_modified = False    # marks that no other state could be found

            # perform `goto` on every state using every terminal / nonterminal
            for state in canonical_collection:
                for symbol in self.__grammar.terminals + self.__grammar.nonterminals:
                    temp_state = self._goto(state, symbol)

                    # add the state if it is valid and doesn't already exist
                    if temp_state is not None and temp_state not in canonical_collection:
                        # mark that at least one new state was found
                        was_modified = True
                        canonical_collection.append(temp_state)

            # break if no other states were found
            if not was_modified:
                break

        return set(canonical_collection)

    def _generate_parsing_table(self, canonical_collection: set[State]) -> dict[State, Action]:
        """ Generates the LR(0) parsing table based on the canonical collection.

        Args:
            canonical_collection (set[State]): the canonical collection of the augmented grammar

        Returns: the parsing table as a mapping from a State to an Action
        """
        def _find_next_state(_item: Item) -> State | None:
            """ Finds the next state based on an item by checking what state contains that item. """
            for _state in canonical_collection:
                if _item in _state.closure:
                    return _state
            return None

        # parsing table
        table: dict[State, Action] = {}

        # find the action for each state of the canonical collection
        for state in canonical_collection:
            for item in state.closure:
                # check for accept / reduce
                if item.current_symbol_idx == len(item.production):
                    # check for accept action
                    if item.nonterminal == self.__grammar.start:
                        # check if the state does not already have an action assigned
                        if state not in table:
                            table[state] = Accept()
                        else:
                            # this should not happen
                            assert False
                    # check for reduce action
                    else:
                        # find number of production for the nonterminal
                        production_no = self.__grammar.productions[item.nonterminal].index(item.production)

                        # check if the state does not already have an action assigned
                        if state not in table:
                            table[state] = Reduce(item.nonterminal, item.production, production_no)
                        else:
                            # shift-reduce / reduce-reduce error
                            raise GrammarError(f"action reduce \"{item.nonterminal} -> {' '.join(item.production)}\" found for state {state}, but it already has {type(table[state]).__name__.lower()} action assigned")
                            # print(f"action reduce \"{item.nonterminal} -> {' '.join(item.production)}\" found for state {state}, but it already has {type(table[state]).__name__.lower()} action assigned")

                # check for shift action
                else:
                    # find next state
                    next_state = _find_next_state(Item(item.nonterminal, item.production, item.current_symbol_idx + 1))

                    if state not in table:
                        # add shift with the symbol
                        table[state] = Shift()
                        table[state].goto[item.production[item.current_symbol_idx]] = next_state
                    elif state in table and isinstance(table[state], Shift):
                        # add the symbol to the shift
                        table[state].goto[item.production[item.current_symbol_idx]] = next_state
                    else:
                        # shift-reduce error
                        raise GrammarError(f"action shift ({item.production[item.current_symbol_idx]}, {next_state}) found for state {state}, but it already has {type(table[state]).__name__.lower()} action assigned")
                        # print(f"action shift ({item.production[item.current_symbol_idx]}, {next_state}) found for state {state}, but it already has {type(table[state]).__name__.lower()} action assigned")

        return table
