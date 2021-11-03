# My Tests
def test_get_request_returns_empty_array(client):
    response = client.get("/books")
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert response_body == []

def test_get_single_book_by_id(client, one_saved_book):
    response = client.get("/books/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body['id'] == 1
    assert response_body['title'] == 'Persuasion'
    assert response_body['description'] == 'Jane Austen'

def test_get_single_book_not_in_db(client):
    response = client.get('/books/1')
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == None

def test_get_returns_all_books(client, two_saved_books):
    response = client.get('/books')
    response_body = response.get_json()

    book_1 = {
        'id': 1,
        'title': 'Pride and Prejudice',
        'description': 'Jane Austen'
        }

    book_2 = {
        'id': 2,
        'title': 'The Stranger',
        'description': 'Albert Camus'
        }

    assert len(response_body) == 2
    assert book_1 in response_body
    assert book_2 in response_body

def test_create_one_book(client):
    book = {
        'title': 'Emma',
        'description': 'Jane Austen'
    }
    response = client.post('/books', json=book)
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == None