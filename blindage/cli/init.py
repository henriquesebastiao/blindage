from pathlib import Path

import typer
from rich import print

from blindage.database import Session, engine
from blindage.messages import (
    DB_ALREADY_EXISTS,
    DB_CREATING_SUCCESSFULLY,
    HELP_INIT,
)
from blindage.models import BlindageSettings, table_registry
from blindage.security import hash_main_password
from blindage.settings import DATABASE_NAME

command = typer.Typer(help=HELP_INIT)


@command.callback(invoke_without_command=True)
def main():
    """Generates a new database, this command should only be used once."""
    if Path(DATABASE_NAME).exists():
        print(DB_ALREADY_EXISTS)
        raise typer.Exit(2)

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

    print(f'\n{DB_CREATING_SUCCESSFULLY}')
