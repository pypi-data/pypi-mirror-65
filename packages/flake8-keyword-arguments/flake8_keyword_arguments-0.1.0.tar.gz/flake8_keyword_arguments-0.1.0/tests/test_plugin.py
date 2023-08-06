from typing import Tuple

from flake8_keyword_arguments.checker import KeywordArgumentsChecker
from tests.conftest import run_validator_for_test_file


def get_error(line: int, column: int, function_name: str, number_of_args: int) -> Tuple[int, int, str, type]:
    message = KeywordArgumentsChecker.MESSAGE_TEMPLATE.format(
        function_name=function_name,
        number_of_args=number_of_args,
    )
    return (line, column, message, KeywordArgumentsChecker)


def test_always_ok_for_empty_file() -> None:
    errors = run_validator_for_test_file(filename='empty.py', max_pos_args=1)
    assert len(errors) == 0


def test_file_with_errors() -> None:
    errors = run_validator_for_test_file('test.py', max_pos_args=1)
    expected_errors = [
        get_error(
            line=20,
            column=0,
            function_name='two_arguments',
            number_of_args=2,
        ),
        get_error(
            line=23,
            column=0,
            function_name='multiple_arguments',
            number_of_args=3,
        ),
        get_error(
            line=25,
            column=0,
            function_name='unknown',
            number_of_args=3,
        ),
        get_error(
            line=27,
            column=0,
            function_name='bar',
            number_of_args=3,
        ),
    ]
    assert errors == expected_errors

    errors = run_validator_for_test_file(filename='test.py', max_pos_args=2)
    expected_errors = [
        get_error(
            line=23,
            column=0,
            function_name='multiple_arguments',
            number_of_args=3,
        ),
        get_error(
            line=25,
            column=0,
            function_name='unknown',
            number_of_args=3,
        ),
        get_error(
            line=27,
            column=0,
            function_name='bar',
            number_of_args=3,
        ),
    ]
    assert errors == expected_errors
