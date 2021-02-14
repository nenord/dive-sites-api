import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = os.environ.get('USER')
password = os.environ.get('PASSWORD')
server = os.environ.get('SERVER')
db = os.environ.get('DATABASE')

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://{username}:{password}@{server}/{db}".format(username, password, server, db)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
