import secrets
import string

import typer
from rich import print

command = typer.Typer(
    help='Generates password and username suggestions.', no_args_is_help=True
)


@command.command(
    help='Generates password suggestions with numbers, letters and special characters incluindo !@#$%&*-_+=.,?'
)
def password():
    length = typer.prompt('Password length', type=int, default=20)
    alphabet = string.ascii_letters + string.digits + '!@#$%&*-_+=.,?'
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    print(f'\n{password}')


@command.command(
    help='Generates username suggestions with numbers and letters.'
)
def username():
    length = typer.prompt('Username length', type=int, default=15)
    alphabet = string.ascii_letters + string.digits
    username = ''.join(secrets.choice(alphabet) for i in range(length))
    print(f'\n{username}')
