from flake8_keyword_arguments.checker import KeywordArgumentsChecker
from tests.conftest import run_validator_for_test_file

_checker = KeywordArgumentsChecker


def test_always_ok_for_empty_file() -> None:
    errors = run_validator_for_test_file(filename='empty.py', max_pos_args=1)
    assert len(errors) == 0


def test_file_with_errors() -> None:
    errors = run_validator_for_test_file('test.py', max_pos_args=1)
    expected_errors = [
        (
            15,
            0,
            _checker.MESSAGE_TEMPLATE.format(function_name='two_arguments', number_of_args=2),
            _checker,
        ),
        (
            18,
            0,
            _checker.MESSAGE_TEMPLATE.format(function_name='multiple_arguments', number_of_args=3),
            _checker,
        ),
    ]
    assert errors == expected_errors

    errors = run_validator_for_test_file(filename='test.py', max_pos_args=2)
    expected_errors = [
        (
            18,
            0,
            _checker.MESSAGE_TEMPLATE.format(function_name='multiple_arguments', number_of_args=3),
            _checker,
        ),
    ]
    assert errors == expected_errors
