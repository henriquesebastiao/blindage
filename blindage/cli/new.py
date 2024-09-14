import typer
from rich import print
from sqlalchemy import select

from blindage.database import Session, find_account_by_name
from blindage.models import Account, BlindageSettings, OtherAttribute
from blindage.security import encrypt, verify_main_password

command = typer.Typer(help='Create a new credentials record.')


@command.callback(invoke_without_command=True)
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
