import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Item(Base):
    __tablename__ = 'item'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    department = Column(String(2), nullable=False)
    product_type = Column(String(4), nullable=False)
    q1 = Column(String(12), nullable=True)
    q2 = Column(String(12), nullable=True)
    q3 = Column(String(12), nullable=True)
    q4 = Column(String(12), nullable=True)
    q5 = Column(String(12), nullable=True)
    q6 = Column(String(12), nullable=True)
  
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///db.sqlite3')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)