# database connection setup

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# create the DB engine
engine = create_engine(DATABASE_URL)

# create a session factory (for handling DB transactions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for sqlalchemy models
Base = declarative_base()


