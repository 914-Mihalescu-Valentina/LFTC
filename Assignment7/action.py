from src.parser.state import State
from src.parser.configuration import Configuration
from src.errors import SyntaxError
from src.structures.pif import TokenType, ProgramInternalForm


class Action:
    """ An action (accept / shift / reduce) for a state in LR(0) parser. """
    pass


class Accept(Action):
    def apply(self, config: Configuration) -> None:
        """ Performs accept action on LR(0) configuration. """
        if len(config.input_stack) != 0:
            raise SyntaxError(f"final configuration reached, but input stack is not empty")


class Reduce(Action):
    def __init__(self, nonterminal: str, production: list[str], production_no: int):
        """ Initializes a reduce action for nonterminal and its production. """
        self.nonterminal: str = nonterminal
        self.production: list[str] = production
        self.production_no: int = production_no

    def apply(self, config: Configuration, table: dict[State, Action]) -> None:
        """ Performs reduce action on LR(0) configuration. """
        num_reduced_elements = 2 * len(self.production)

        if len(config.working_stack) < num_reduced_elements:
            raise SyntaxError(f"")

        config.working_stack.pop(num_reduced_elements)

        prev_state = config.working_stack.top()
        action = table[prev_state]
        if not isinstance(action, Shift):
            # this should not happen
            assert False

        next_state = action.goto[self.nonterminal]

        config.working_stack.push([self.nonterminal, next_state])
        config.output_stack.push([(self.nonterminal, self.production_no)])


class Shift(Action):
    def __init__(self):
        self.goto: dict[str, State] = {}

    def apply(self, config: Configuration) -> None:
        """ Performs shift action on LR(0) configuration. """
        if len(config.input_stack) == 0:
            raise SyntaxError(f"failed to apply shift action, input stack is empty")

        entry: ProgramInternalForm.Entry = config.input_stack.pop(1)[0]
        symbol = entry.token
        symbol_type = entry.type
        if symbol_type == TokenType.IDENTIFIER and 'ID' in self.goto:
            next_state = self.goto['ID']
        elif symbol_type == TokenType.LITERAL:
            if 'INT' in self.goto:
                next_state = self.goto['INT']
            elif 'STR' in self.goto:
                next_state = self.goto['STR']
            else:
                raise SyntaxError(f"failed to apply shift action, there is not a next state for ({symbol}, {config.working_stack.top()})")
        elif symbol in self.goto:
            next_state = self.goto[symbol]
        else:
            raise SyntaxError(f"failed to apply shift action, there is not a next state for ({symbol}, {config.working_stack.top()})")

        config.working_stack.push([symbol, next_state])
