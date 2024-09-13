import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blindage.models import table_registry
from blindage.settings import DATABASE_URL

if int(os.getenv('DEBUG', '0')):
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
else:
    engine = create_engine(DATABASE_URL)

Session = sessionmaker(engine)
