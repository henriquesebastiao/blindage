import os

from blindage.cli import app
from tests.conftest import runner


def test_init():
    os.environ['DEBUG'] = '1'
    result = runner.invoke(app, ['init'], input='Test12345@#$\nTest12345@#$\n')

    assert result.exit_code == 0
    assert 'Database created' in result.stdout


def test_init_with_error_when_repeating_password():
    os.environ['DEBUG'] = '1'
    result = runner.invoke(app, ['init'], input='Test12345@#$\nTest1245@#$\n')

    assert result.exit_code == 1
    assert (
        'Confirmation password is not the same as main password.'
        in result.stdout
    )
