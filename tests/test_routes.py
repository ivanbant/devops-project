import pytest

from app import create_app
from app import routes
from book import Book


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    routes.books.clear()
    routes.books.extend([
        Book(1, "Dune", "Frank Herbert", 1965, False),
        Book(2, "1984", "George Orwell", 1949, True),
        Book(3, "The Hobbit", "J.R.R. Tolkien", 1937, False),
        Book(4, "Fahrenheit 451", "Ray Bradbury", 1953, True),
        Book(5, "Brave New World", "Aldous Huxley", 1932, False)
    ])

    with app.test_client() as client:
        yield client

def test_healthz(client):
    response = client.get('/healthz')

    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_get_books(client):
    response = client.get('/books')

    assert response.status_code == 200
    assert len(response.json) == 5

def test_get_book(client):
    response = client.get('/books/1')

    assert response.status_code == 200
    assert response.json['title'] == 'Dune'
    assert response.json['author'] == 'Frank Herbert'

def test_create_book(client):
    response = client.post('/books', json={
        "title": "Animal Farm",
        "author": "George Orwell",
        "year": 1945,
        "read": False
    })

    assert response.status_code == 201
    assert response.json['book']['title'] == 'Animal Farm'
    assert len(routes.books) == 6

def test_update_book(client):
    response = client.put('/books/1', json={
        "title": "Dune Messiah",
        "read": True
    })

    assert response.status_code == 200
    assert response.json['book']['title'] == 'Dune Messiah'
    assert response.json['book']['read'] is True

def test_delete_book(client):
    response = client.delete('/books/1')

    assert response.status_code == 200
    assert len(routes.books) == 4

def test_get_nonexistent_book(client):
    response = client.get('/books/999')

    assert response.status_code == 404

def test_update_nonexistent_book(client):
    response = client.put('/books/999', json={
        "title": "Unknown"
    })

    assert response.status_code == 404

def test_delete_nonexistent_book(client):
    response = client.delete('/books/999')

    assert response.status_code == 404