import typer
from rich.console import Console
from typing_extensions import Annotated, Optional

app = typer.Typer(help='Pythonic Password Manager.')
console = Console()

__version__ = '0.1.0'


def get_version(value: bool):
    if value:
        console.print(
            f'[bold blue]Blindage[/bold blue] version: [green]{__version__}[/green]'
        )
        console.print('Developed by [bold]Henrique Sebastião[/bold]')
        raise typer.Exit()


@app.callback(invoke_without_command=True)
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
):
    message = 'USAGE: skyport [OPTIONS] COMMAND [OPTIONS]'

    if ctx.invoked_subcommand:
        return
    console.print(message)
