from typer.testing import CliRunner

from blindage.cli import app

runner = CliRunner()


def test_get_version():
    result = runner.invoke(app, ['--version'])
    assert result.exit_code == 0
    assert 'Developed by' in result.stdout
    assert 'Henrique Sebastião' in result.stdout


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert 'USAGE: skyport' in result.stdout
