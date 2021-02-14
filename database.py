import os
import pyodbc
import urllib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

params = urllib.parse.quote_plus \ # urllib.parse.quote_plus for python 3
(r'Driver={ODBC Driver 13 for SQL Server};Server=tcp:dive-sites.database.windows.net,1433;Database=sites;Uid=nenord;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine = create_engine(conn_str,echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
