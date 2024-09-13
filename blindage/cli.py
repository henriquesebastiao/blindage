import typer
from rich import print
from sqlalchemy import select
from typing_extensions import Annotated, Optional

from blindage.database import Session
from blindage.models import Account, OtherAttribute

app = typer.Typer(
    help='Pythonic Password Manager.',
    no_args_is_help=True,
    rich_markup_mode='rich',
)

__version__ = '0.1.0'


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


@app.command()
def new():
    """Create a new credentials record."""
    name = typer.prompt('Name')
    username = typer.prompt('Username')
    password = typer.prompt('Password', hide_input=True)
    url = typer.prompt('URL')
    otp_secret = typer.prompt('OTP Secret')
    recovery_codes = typer.prompt('Recovery Codes')

    custom_fields = []

    while True:
        more_attributes = typer.confirm('\nWant to add custom fields?')

        if more_attributes:
            cf_name = typer.prompt('Custom field name')
            cf_value = typer.prompt('Custom field value')
            custom_fields.append([cf_name, cf_value])
        else:
            break

    with Session() as session:
        account = Account(
            password=password,
            name=name,
            username=username,
            url=url,
            otp_secret=otp_secret,
            recovery_codes=recovery_codes,
        )

        session.add(account)
        session.commit()

        account = session.scalar(select(Account).where(Account.name == name))

        if custom_fields:
            for field_item in custom_fields:
                other_attribute = OtherAttribute(
                    name=field_item[0],
                    content=field_item[1],
                    account_id=account.id,
                )

                session.add(other_attribute)
                session.commit()

    print(
        '\nRegistration created [bold green]successfully[/bold green] :white_heavy_check_mark:'
    )
