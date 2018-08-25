import sendgrid_console as console
import sendgrid_shared as shared


def test_field_prompt():
    assert console.field_prompt('Name') == 'Name: '


def test_boolean_formatter():
    assert console.boolean_formatter('Do you like me?') == 'Do you like me? [Y|N] '


def test_validate_boolean():
    _regex_test_helper(console.validate_boolean, ['Y', 'N', 'y', 'n'],
                                                 ['a', '1', ' ', '\n'])


def test_validate_email():
    _regex_test_helper(shared.validate_email, ['bob@email.com', 'hello123@250ok.org', 'bill@sub.domain.in'],
                                              ['username', 'joe@', '@hotmail.com', 'sam@gmail'])


def test_get_basename():
    assert shared.get_basename('path/file.txt') == 'file.txt'


def test_get_extension():
    assert shared.get_extension('path/file.txt') == '.txt'


def _regex_test_helper(function_name, valid_tests, invalid_tests):
    for valid in valid_tests:
        assert function_name(valid)
    for invalid in invalid_tests:
        assert not function_name(invalid)