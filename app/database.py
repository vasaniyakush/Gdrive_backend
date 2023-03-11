from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#this vvv is just a varialble, we can name it anything
# SQLALCHEMY_DATABSE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<databse_name>'

# used to create an engine
# engine = create_engine(SQLALCHEMY_DATABSE_URL)
from .config import settings
SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_gdrive}'

engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
 
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()