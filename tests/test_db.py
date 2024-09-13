from sqlalchemy import select

from blindage.models import Account


def test_create_account(session):
    account = Account(
        password='secret_password',
        name='Google',
        username='test@gmail.com',
        url='https://google.com',
    )

    session.add(account)
    session.commit()

    result = session.scalar(
        select(Account).where(Account.username == 'test@gmail.com')
    )

    assert result.name == 'Google'
