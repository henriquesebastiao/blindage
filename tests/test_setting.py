from blindage.settings import DATABASE_URL


def test_db_url():
    assert DATABASE_URL == 'sqlite:///blindage.db'
