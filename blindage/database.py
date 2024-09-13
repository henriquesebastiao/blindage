from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from blindage.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
