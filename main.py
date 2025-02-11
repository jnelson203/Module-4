from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Book model
class Book(BaseModel):
    id: int
    book_name: str
    author: str
    publisher: str

# Fake database (a list of books)
books_db = []

# Create a new book
@app.post("/books/", response_model=Book)
def create_book(book: Book):
    books_db.append(book)
    return book

# Read all books
@app.get("/books/", response_model=List[Book])
def get_books():
    return books_db

# Read a single book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Update a book by ID
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book by ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[index]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
