import ast
from typing import Any, Generator, List, Tuple

from flake8_keyword_arguments.utils import FlakeError

DEFAULT_MAX_POS_ARGS = 2


class KeywordArgumentsChecker:
    version = '1.0.0'
    name = 'flake8-keyword-arguments'

    max_pos_args = DEFAULT_MAX_POS_ARGS

    MESSAGE_TEMPLATE = "FKA01 {function_name}'s call uses {number_of_args} positional arguments, use keyword arguments."

    def __init__(self, tree: ast.AST, filename: str) -> None:
        self.filename = filename
        self.tree = tree

    @classmethod
    def add_options(cls, parser: Any) -> None:
        parser.add_option(  # pragma: no cover
            '--max-pos-args',
            type='int',
            metavar='n',
            default=DEFAULT_MAX_POS_ARGS,
            parse_from_config=True,
            help='How many positional arguments are allowed (default: 2)',
        )

    @classmethod
    def parse_options(cls, options: Any) -> None:
        cls.max_pos_args = int(options.max_pos_args)

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        errors: List[FlakeError] = []

        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue

            if not isinstance(node.func, (ast.Name, ast.Attribute)):
                continue

            if len(node.args) > self.max_pos_args:
                function_name = self._get_name(node.func)
                message = self.MESSAGE_TEMPLATE.format(function_name=function_name, number_of_args=len(node.args))
                error = FlakeError(line=node.lineno, column=node.col_offset, message=message)
                errors.append(error)

        for error in errors:
            yield error.line, error.column, error.message, type(self)

    @staticmethod
    def _get_name(node: Any) -> str:
        return node.id if hasattr(node, 'id') else node.attr
