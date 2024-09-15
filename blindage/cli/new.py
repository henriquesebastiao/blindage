from pathlib import Path

import typer
from pydantic import ValidationError
from rich import print
from sqlalchemy import select

from blindage.database import Session, find_account_by_name
from blindage.messages import DB_NOT_EXISTS, INCENTIVE_TO_CREATE_DB
from blindage.models import Account, BlindageSettings, OtherAttribute
from blindage.security import encrypt, verify_main_password
from blindage.settings import DATABASE_NAME
from blindage.validators import Url

command = typer.Typer(help='Create a new credentials record.')


@command.callback(invoke_without_command=True)
def new():
    """Create a new credentials record."""
    if not Path(DATABASE_NAME).exists():
        print(DB_NOT_EXISTS)
        print(INCENTIVE_TO_CREATE_DB)
        raise typer.Exit(2)

    name = typer.prompt('Name')
    username = typer.prompt('Username')
    password = typer.prompt('Password', hide_input=True)

    while True:
        url = typer.prompt('URL', default='', show_default=False)

        if url:
            try:
                url = Url(url=str(url)).url
                break
            except ValidationError:
                print('[bold red]An invalid URL was provided![/bold red]')
                print('Leave blank or try again.')
                print(
                    'NOTE: A valid URL must start with http:// or https:// for example:'
                )
                print('https://example.com\n')
                continue
        break

    otp_secret = typer.prompt('OTP Secret', default='', show_default=False)
    recovery_codes = typer.prompt(
        'Recovery Codes', default='', show_default=False
    )

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
