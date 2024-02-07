from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

load_dotenv() 

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
database = os.getenv("DATABASE")

# SQLite Database
# SQLARCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# engine = create_engine(SQLARCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# Postgres Database
SQLARCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@babar.db.elephantsql.com/{database}"
engine = create_engine(SQLARCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
