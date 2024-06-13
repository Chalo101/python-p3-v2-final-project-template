from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base, session

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    books = relationship("Book", back_populates="author")

    @classmethod
    def create(cls, name):
        author = cls(name=name)
        session.add(author)
        session.commit()
        return author

    @classmethod
    def delete(cls, author_id):
        author = cls.find_by_id(author_id)
        if author:
            session.delete(author)
            session.commit()

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, author_id):
        return session.query(cls).filter_by(id=author_id).first()

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"
