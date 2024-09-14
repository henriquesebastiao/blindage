import os
import unittest

from blindage.cli.app import app
from blindage.database import engine
from blindage.models import table_registry
from tests.conftest import MAIN_PASSWORD_TEST, runner


class NewTest(unittest.TestCase):
    def setUp(self):
        os.environ['DEBUG'] = '1'
        table_registry.metadata.create_all(engine)
        runner.invoke(
            app,
            ['init'],
            input=f'{MAIN_PASSWORD_TEST}\n{MAIN_PASSWORD_TEST}\n',
        )

    def tearDown(self):
        table_registry.metadata.drop_all(engine)

    def test_new(self):
        result = runner.invoke(
            app,
            ['new'],
            input=f'Email\ntest@email.com\n12345678\nhttps://email.com\nJKLSHDFSD SDFKJSDLF\nasfdasf fdsf\nn\n{MAIN_PASSWORD_TEST}\n',
        )

        assert result.exit_code == 0

    def test_new_with_more_attributes(self):
        result = runner.invoke(
            app,
            ['new'],
            input=f'Email\ntest@email.com\n12345678\nhttps://email.com\nJKLSHDFSD SDFKJSDLF\nasfdasf fdsf\ny\nPIN\n1234\nn\n{MAIN_PASSWORD_TEST}\n',
        )

        assert result.exit_code == 0

    def test_newwit_wrong_password(self):
        result = runner.invoke(
            app,
            ['new'],
            input='Email\ntest@email.com\n12345678\nhttps://email.com\nJKLSHDFSD SDFKJSDLF\nasfdasf fdsf\nn\nwrong_password\n',
        )

        assert result.exit_code == 1
        assert 'Wrong main password!' in result.stdout
