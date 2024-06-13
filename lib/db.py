from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

engine = create_engine('sqlite:///books.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
