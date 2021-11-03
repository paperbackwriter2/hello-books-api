import pytest
from app import create_app
from app import db
from app.models.book import Book


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_saved_book(app):
    persuasion = Book(title='Persuasion', description='Jane Austen')
    db.session.add(persuasion)
    db.session.commit()








@pytest.fixture
def two_saved_books(app):
    pride_and_prejudice = Book(title='Pride and Prejudice', description='Jane Austen')
    the_stranger = Book(title='The Stranger', description='Albert Camus')
    db.session.add_all([pride_and_prejudice, the_stranger])
    db.session.commit()