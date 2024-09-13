import typer
from rich import print
from sqlalchemy import select
from typing_extensions import Annotated, Optional

from blindage.database import Session, engine, find_account_by_name
from blindage.models import (
    Account,
    BlindageSettings,
    OtherAttribute,
    table_registry,
)
from blindage.security import encrypt, hash_main_password, verify_main_password

app = typer.Typer(
    help='Pythonic Password Manager :locked_with_key:',
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


@app.command(
    help='Generates a new database, [bold]this command should only be used once[/bold].'
)
def init():
    """Generates a new database, this command should only be used once."""
    main_pwd = typer.prompt('Main password', hide_input=True)
    confirm_main_pwd = typer.prompt(
        'Confirm your main password', hide_input=True
    )

    if not main_pwd == confirm_main_pwd:
        print(
            '[bold red]Confirmation password is not the same as main password.[/bold red]'
        )
        raise typer.Exit(1)

    table_registry.metadata.create_all(engine)

    with Session() as session:
        blindage = BlindageSettings(main_password=hash_main_password(main_pwd))

        session.add(blindage)
        session.commit()

    print(
        '\n[bold]Database created [bold green]successfully[/bold green][/bold] :sparkles:'
    )


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

    main_password: str = typer.prompt('\nMain Password', hide_input=True)

    with Session() as session:
        blindage = session.scalars(select(BlindageSettings)).first()

        if not verify_main_password(blindage.main_password, main_password):
            print('[bold red]Wrong main password![/bold red]')
            raise typer.Exit(1)

    with Session() as session:
        account = Account(
            password=encrypt(main_password, password),
            name=encrypt(main_password, name),
            username=encrypt(main_password, username),
            url=encrypt(main_password, url),
            otp_secret=encrypt(main_password, otp_secret),
            recovery_codes=encrypt(main_password, recovery_codes),
        )

        session.add(account)
        session.commit()

        account = find_account_by_name(name, main_password, session)

        if custom_fields:
            for field_item in custom_fields:
                other_attribute = OtherAttribute(
                    name=encrypt(main_password, field_item[0]),
                    content=encrypt(main_password, field_item[1]),
                    account_id=account.id,
                )

                session.add(other_attribute)
                session.commit()

    print(
        '\nRegistration created [bold green]successfully[/bold green] :white_heavy_check_mark:'
    )
