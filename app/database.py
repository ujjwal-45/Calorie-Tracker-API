from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


database_file_name = "calorie.db"
DATABASE_URL = f"sqlite:///{database_file_name}"

connect_args= {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()
