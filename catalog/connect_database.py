from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database_setup import Base

def connect_database():
    engine = create_engine('sqlite:////var/www/coffeeshops/catalog/coffeeshopmenu.db')
    Base.metadata.bind = engine
    db_session = scoped_session(sessionmaker(bind=engine))
    session = db_session()

    return session
