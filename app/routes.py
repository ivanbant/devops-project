from flask import Blueprint, render_template,request, jsonify
from app.book import Book

main = Blueprint('main', __name__)


books = [
    Book(1, "Dune", "Frank Herbert", 1965, False),
    Book(2, "1984", "George Orwell", 1949, True),
    Book(3, "The Hobbit", "J.R.R. Tolkien", 1937, False),
    Book(4, "Fahrenheit 451", "Ray Bradbury", 1953, True),
    Book(5, "Brave New World", "Aldous Huxley", 1932, False)
]


@main.route('/books', methods=['GET'])
def get_books():
    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "read": book.read
        }
        for book in books
    ])

@main.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    new_book = Book(
        id=len(books) + 1,
        title=data.get('title'),
        author=data.get('author'),
        year=data.get('year'),
        read=data.get('read', False)
    )

    books.append(new_book)

    return jsonify({
        "message": "Book created",
        "book": {
            "id": new_book.id,
            "title": new_book.title,
            "author": new_book.author,
            "year": new_book.year,
            "read": new_book.read
        }
    }), 201

@main.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):

    book = next((b for b in books if b.id == book_id), None)

    if book is None:
        return jsonify({"message": "Book not found"}), 404

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "read": book.read
    }), 200

@main.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()

    book = next((b for b in books if b.id == book_id), None)

    if book is None:
        return jsonify({"message": "Book not found"}), 404

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year = data.get('year', book.year)
    book.read = data.get('read', book.read)

    return jsonify({
        "message": "Book updated",
        "book": {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "read": book.read
        }
    }), 200


@main.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):

    book = next((b for b in books if b.id == book_id), None)

    if book is None:
        return jsonify({"detail": f"no book with id {book_id}"}), 404

    books.remove(book)

    return jsonify({
        "message": "Book deleted",
        "id": book_id
    }), 200

@main.route('/healthz', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok"
    }), 200