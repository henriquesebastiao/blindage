from blindage.cli import app
from tests.conftest import runner


def test_get_version():
    result = runner.invoke(app, ['--version'])
    assert result.exit_code == 0
    assert 'Developed by' in result.stdout
    assert 'Henrique Sebastião' in result.stdout


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert 'Pythonic Password Manager.' in result.stdout
