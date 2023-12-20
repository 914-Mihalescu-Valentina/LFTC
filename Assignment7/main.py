import sys
from pathlib import Path
from src.lexer import lexer
from src.parser.parser import Parser
from src.structures.pif import ProgramInternalForm
from src.structures.program import Program
from src.errors import LexicalError, GrammarError, SyntaxError


def compile(source_path: str | Path, output_dir: str | Path) -> None:
    """ Compiles the source code and dumps the output in `output_dir` directory.

    The path to the used grammar is hardcoded.

    Args:
        source_path (str | Path): path to source code
        output_dir (str | Path): path to output directory
    """
    # create output dir if it does not already exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    source_path = Path(source_path)
    output_dir = Path(output_dir)

    grammar_path = Path('input/g1.toml')

    id_symtable_path = output_dir / 'ID_SYMTABLE.out'
    literal_symtable_path = output_dir / 'LITERAL_SYMTABLE.out'
    pif_path = output_dir / 'PIF.out'
    parsing_tree_path = output_dir / 'PARSING_TREE.out'

    try:
        # # scan
        # program: Program = lexer.scan(source_path)
        # print("Lexically correct")
        #
        # program.id_symtable.dump(id_symtable_path)
        # program.literal_symtable.dump(literal_symtable_path)
        # program.pif.dump(pif_path, pretty=False)
        #
        # # parse
        # parser = Parser(grammar_path)
        # parser_output = parser.parse(program.pif)

        pif = ProgramInternalForm()
        pif.load('examples/input/seq.txt')
        parser = Parser(grammar_path)
        parser_output = parser.parse(pif)

        parser_output.dump(parsing_tree_path)
        print(f"Parsing tree:\n{parser_output}")
    except LexicalError as e:
        print(f"{e}", file=sys.stderr)
    except GrammarError as e:
        print(f"{e}", file=sys.stderr)
    except SyntaxError as e:
        print(f"{e}", file=sys.stderr)


def main():
    # compile
    source_code_path = 'examples/p1.mat'
    output_dir = 'examples/output/'
    compile(source_code_path, output_dir)


if __name__ == '__main__':
    main()
