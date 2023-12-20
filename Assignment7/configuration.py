from src.adt.stack import Stack
from dataclasses import dataclass


@dataclass
class Configuration:
    """ A configuration of LR(0) parser. """
    working_stack: Stack
    input_stack: Stack
    output_stack: Stack
