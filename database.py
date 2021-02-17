import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#engine = create_engine(SQLALCHEMY_DATABASE_URI)
engine = create_engine("postgres://jrvscjelvwefxb:9b0833938c8ad5c13b4d1aa0ff8e839cdc3ecbbae189bd2780b9c7a2ae62d13a@ec2-34-192-58-41.compute-1.amazonaws.com:5432/d6j9r3trl47ohl")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
