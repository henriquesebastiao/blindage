import typer
from rich import print
from typing_extensions import Annotated, Optional

from blindage.cli import init, new

app = typer.Typer(
    help='Pythonic Password Manager :locked_with_key:',
    no_args_is_help=True,
    rich_markup_mode='rich',
)

__version__ = '0.1.0'

app.add_typer(init.command, name='init')
app.add_typer(new.command, name='new')


def get_version(value: bool):
    if value:
        print(
            f'[bold blue]Blindage[/bold blue] version: [green]{__version__}[/green]'
        )
        print('Developed by [bold]Henrique Sebastião[/bold]')


@app.callback(
    invoke_without_command=True,
    epilog='Made with :heart: in [blue]Earth[/blue]',
)
def main(
    ctx: typer.Context,
    version: Annotated[
        Optional[bool],
        typer.Option(
            '--version',
            '-v',
            callback=get_version,
            help='Returns the version of Blindage.',
        ),
    ] = None,
): ...
