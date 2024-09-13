import unittest

from blindage.cli import app
from blindage.database import engine
from blindage.models import table_registry
from tests.conftest import runner


class NewTest(unittest.TestCase):
    def setUp(self):
        table_registry.metadata.create_all(engine)

    def tearDown(self):
        table_registry.metadata.drop_all(engine)

    def test_new(self):
        result = runner.invoke(
            app,
            ['new'],
            input='Email\ntest@email.com\n12345678\nhttps://email.com\nJKLSHDFSD SDFKJSDLF\nasfdasf fdsf\nn\n',
        )

        assert result.exit_code == 0

    def test_new_with_more_attributes(self):
        result = runner.invoke(
            app,
            ['new'],
            input='Email\ntest@email.com\n12345678\nhttps://email.com\nJKLSHDFSD SDFKJSDLF\nasfdasf fdsf\ny\nPIN\n1234\nn\n',
        )

        assert result.exit_code == 0
