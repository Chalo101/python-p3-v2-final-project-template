from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, session

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship("Author", back_populates="books")

    @classmethod
    def create(cls, title, genre, author_id):
        book = cls(title=title, genre=genre, author_id=author_id)
        session.add(book)
        session.commit()
        return book

    @classmethod
    def delete(cls, book_id):
        book = cls.find_by_id(book_id)
        if book:
            session.delete(book)
            session.commit()

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, book_id):
        return session.query(cls).filter_by(id=book_id).first()

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, genre={self.genre}, author={self.author.name})>"
