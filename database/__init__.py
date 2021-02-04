import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

db_engine = create_engine(os.getenv('POSTGRES_URI'), echo=True)

Session = sessionmaker(bind=db_engine)

Base = declarative_base()


def create_tables():
    Base.metadata.create_all(db_engine)
