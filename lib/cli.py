# lib/cli.py

from models.book import Book
from models.author import Author
from db import session
import sys

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            display_search_results()
        elif choice == "4":
            delete_book() 
        else:
            print("Invalid choice")

def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Add a new book")
    print("2. View existing books")
    print("3. Search for books")
    print("4. Delete a book")

def add_book():
    title = input("Enter the title of the book: ")
    genre = input("Enter the genre of the book: ")
    author_name = input("Enter the name of the author: ")

    author = session.query(Author).filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        session.add(author)
        session.commit()

    book = Book(title=title, genre=genre, author=author)
    session.add(book)
    session.commit()
    print("Book added successfully!")

def view_books():
    books = session.query(Book).all()
    if books:
        print("Existing books:")
        for book in books:
            print(f"Title: {book.title}, Genre: {book.genre}, Author: {book.author.name}")
    else:
        print("No books found.")

def search_books():
    criteria = input("Enter the search criteria (title/author/genre): ")
    keyword = input("Enter the keyword to search: ")
    books = []

    if criteria == "title":
        books = session.query(Book).filter(Book.title.ilike(f'%{keyword}%')).all()
    elif criteria == "author":
        books = session.query(Book).join(Author).filter(Author.name.ilike(f'%{keyword}%')).all()
    elif criteria == "genre":
        books = session.query(Book).filter(Book.genre.ilike(f'%{keyword}%')).all()
    else:
        print("Invalid search criteria.")
        return []
    
    # Returning the search results and count as a tuple
    return (books, len(books))

def display_search_results():
    results, count = search_books()
    if results:
        print(f"Search results ({count} found):")
        for book in results:
            print(f"Title: {book.title}, Genre: {book.genre}, Author: {book.author.name}")
    else:
        print("No books found.")

def delete_book():
    title = input("Enter the title of the book you want to delete: ")

    # Query the book by title
    book = session.query(Book).filter_by(title=title).first()
    if book:
        confirm = input(f"Are you sure you want to delete '{title}'? (yes/no): ")
        if confirm.lower() == "yes":
            session.delete(book)
            session.commit()
            print("Book deleted successfully!")
        else:
            print("Deletion canceled.")
    else:
        print("Book not found.")

def exit_program():
    print("Goodbye!")
    sys.exit()

if __name__ == "__main__":
    main()
