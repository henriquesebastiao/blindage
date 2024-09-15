import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typer.testing import CliRunner

from blindage.models import table_registry
from blindage.settings import DATABASE_NAME

runner = CliRunner(env={'DEBUG': '1'})
MAIN_PASSWORD_TEST = 'Test12345@#$'


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def drop_db():
    if Path(DATABASE_NAME).exists():
        os.remove(DATABASE_NAME)
