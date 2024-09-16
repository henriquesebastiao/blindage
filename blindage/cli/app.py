from pathlib import Path

import pyotp
import pyperclip
import typer
from rich import print
from rich.console import Console
from rich.table import Table
from sqlalchemy import select
from typing_extensions import Annotated, Optional

from blindage.cli import gen, init, new, update
from blindage.database import Session, find_account_by_name
from blindage.messages import (
    DB_NOT_EXISTS,
    INCENTIVE_TO_CREATE_DB,
    WRONG_MAIN_PASSWORD,
)
from blindage.models import BlindageSettings
from blindage.security import decrypt, encrypt, verify_main_password
from blindage.settings import DATABASE_NAME, __version__

app = typer.Typer(
    help='Pythonic Password Manager :locked_with_key:',
    no_args_is_help=True,
    rich_markup_mode='rich',
)
console = Console()

app.add_typer(init.command, name='init')
app.add_typer(new.command, name='new')
app.add_typer(gen.command, name='gen')
app.add_typer(update.command, name='update')


def get_version(value: bool):
    if value:
        print(
            f'[bold blue]Blindage[/bold blue] version: [green]{__version__}[/green]'
        )
        print('Pythonic Password Manager :locked_with_key:')
        print('Made with :heart: in [blue]Earth[/blue]')


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


@app.command(help='Open the project repository on GitHub.')
def doc():
    print('Opening the Blindage repository on GitHub.')
    typer.launch('https://github.com/henriquesebastiao/blindage')


@app.command(help='Get the OTP code of an account.', no_args_is_help=True)
def otp(account_name: str):
    if not Path(DATABASE_NAME).exists():
        print(DB_NOT_EXISTS)
        print(INCENTIVE_TO_CREATE_DB)
        raise typer.Exit(2)

    main_password = typer.prompt('Main Password', hide_input=True)

    with Session() as session:
        blindage = session.scalars(select(BlindageSettings)).first()

        if not verify_main_password(blindage.main_password, main_password):
            print(WRONG_MAIN_PASSWORD)
            raise typer.Exit(1)

    with Session() as session:
        account = find_account_by_name(
            account_name.strip(), main_password, session
        )

    totp_auth_key = decrypt(main_password, account.otp_secret)
    totp = pyotp.TOTP(totp_auth_key).now()

    pyperclip.copy(totp)  # Copy the TOTP code to the clipboard.
    print(totp)


@app.command(
    help='Searches for an account and returns its data.', no_args_is_help=True
)
def find(account_name: str):
    main_password = typer.prompt('Main Password', hide_input=True)

    with Session() as session:
        blindage = session.scalars(select(BlindageSettings)).first()

        if not verify_main_password(blindage.main_password, main_password):
            print(WRONG_MAIN_PASSWORD)
            raise typer.Exit(1)

    with Session() as session:
        account = find_account_by_name(
            account_name.strip(), main_password, session
        )

    table = Table('Name', highlight=True)

    attributes = [account.name]

    if account.username:
        table.add_column('Username')
        attributes.append(account.username)

    table.add_column('Password')
    attributes.append(account.password)

    if account.otp_secret:
        table.add_column('OTP Code')
        totp_auth_key = decrypt(main_password, account.otp_secret)
        totp = pyotp.TOTP(totp_auth_key).now()
        attributes.append(encrypt(main_password, totp))

    if account.url:
        table.add_column('URL')
        attributes.append(account.url)

    if account.recovery_codes:
        table.add_column('Recovery Codes')
        attributes.append(account.recovery_codes)

    for i in range(len(attributes)):
        attributes[i] = decrypt(main_password, attributes[i])

    table.add_row(*attributes)
    console.print(table)
