import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session as T_Session
from sqlalchemy.orm import sessionmaker

from blindage.models import Account, table_registry
from blindage.security import decrypt
from blindage.settings import DATABASE_URL

if int(os.getenv('DEBUG', '0')):
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
else:
    engine = create_engine(DATABASE_URL)

Session = sessionmaker(engine)


def find_account_by_name(
    name: str, main_password: str, session: T_Session
) -> Account:
    accounts = session.scalars(select(Account)).all()

    for account in accounts:
        if (
            name.strip().lower()
            in decrypt(main_password, account.name).lower()
        ):
            return account
