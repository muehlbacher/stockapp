import sys
import os

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.mysql import TINYINT


# Add the parent directory to the sys.path
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_directory)
# Now you can import the module from the parent folder
from data.models import *


# Define the database URL
DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1/market"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

print("Tables created successfully!")