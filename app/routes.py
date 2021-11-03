from typing_extensions import get_args
from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, request, make_response, abort

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("/", methods=["GET", "POST"], strict_slashes=False)
def handle_books():
    if request.method == "GET":
        title_param = request.args.get("title")
        if title_param:
            books_objects_list = Book.query.filter_by(title = title_param)
        else:
            books_objects_list = Book.query.all() # creates a list of book objects
        response_list = [ 
            {
            "id": book.id, 
            "title": book.title, 
            "description": book.description
            }
        for book in books_objects_list]
        return jsonify(response_list), 200
        
    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("Error in request body", 400)
        new_book = Book(title=request_body["title"],
                    description = request_body["description"])
        db.session.add(new_book)
        db.session.commit()
        
        return make_response(f"Book {new_book.title} successfully created", 201)

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_single_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"error":"book_id must be an int"}, 400))
    
    requested_book = Book.query.get_or_404(book_id)

    if request.method == "GET":
        return make_response(requested_book.to_json(), 200)

    elif request.method == "PUT":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("incomplete request body", 400)
        requested_book.title = request_body["title"]
        requested_book.description = request_body["description"]
        db.session.commit()
        return make_response(f"Successfully updated {requested_book.title}", 200)

    elif request.method == "DELETE":
        db.session.delete(requested_book)
        db.session.commit()
        return make_response(f"Deleted {requested_book.title}", 200)

