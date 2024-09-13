from blindage.database import find_account_by_name
from blindage.models import Account
from blindage.security import decrypt, encrypt
from tests.conftest import MAIN_PASSWORD_TEST


def test_create_account(session):
    account = Account(
        password=encrypt(MAIN_PASSWORD_TEST, 'secret_password'),
        name=encrypt(MAIN_PASSWORD_TEST, 'Google'),
        username=encrypt(MAIN_PASSWORD_TEST, 'test@gmail.com'),
        url=encrypt(MAIN_PASSWORD_TEST, 'https://google.com'),
    )

    session.add(account)
    session.commit()

    result = find_account_by_name('Google', MAIN_PASSWORD_TEST, session)

    assert decrypt(MAIN_PASSWORD_TEST, result.name) == 'Google'
