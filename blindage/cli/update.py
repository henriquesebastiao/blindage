from pathlib import Path

import typer
from rich import print
from sqlalchemy import select

from blindage.database import Session, find_account_by_name
from blindage.messages import (
    ACCOUNT_NOT_FOUND,
    DB_NOT_EXISTS,
    INCENTIVE_TO_CREATE_DB,
    WRONG_MAIN_PASSWORD,
)
from blindage.models import BlindageSettings, PasswordHistory
from blindage.security import encrypt, verify_main_password
from blindage.settings import DATABASE_NAME

command = typer.Typer(help='Update account credentials.', no_args_is_help=True)


@command.command(name='password', help='Update an account password.', no_args_is_help=True)
def update_password(account_name: str):
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

        if not account:
            print(ACCOUNT_NOT_FOUND)
            raise typer.Exit(4)

        typer.confirm(
            'Are you sure you want to change your password?', abort=True
        )
        new_password = typer.prompt('Enter new password', hide_input=True)

        password_history = PasswordHistory(
            password=account.password, account_id=account.id
        )

        session.add(password_history)

        account.password = encrypt(main_password, new_password)

        session.commit()

    print('Password changed [bold green]successfully[/bold green] :sparkles:')
