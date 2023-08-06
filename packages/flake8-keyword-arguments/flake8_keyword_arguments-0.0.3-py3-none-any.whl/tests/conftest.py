import ast
import os
from typing import List, Tuple

from flake8.options.manager import OptionManager

from flake8_keyword_arguments.checker import KeywordArgumentsChecker


def run_validator_for_test_file(filename: str, max_pos_args: int) -> List[Tuple[int, int, str, type]]:
    test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files', filename)

    with open(test_file_path, 'r') as file_handler:
        raw_content = file_handler.read()

    tree = ast.parse(raw_content)

    options = OptionManager()
    options.max_pos_args = max_pos_args
    KeywordArgumentsChecker.parse_options(options)

    checker = KeywordArgumentsChecker(tree=tree, filename=filename)

    return list(checker.run())
