from flask_restful import Resource
from flask import request
from app.models import Book, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import error_response, success_response


class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return [book.to_dict() for book in books], 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user.is_admin:
            return error_response("Only admins can add books", 403)

        data = request.get_json()
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
        return book.to_dict(), 201


class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return book.to_dict()

    @jwt_required()
    def put(self, book_id):
        user = User.query.get(get_jwt_identity())
        if not user.is_admin:
            return error_response("Admins only", 403)

        book = Book.query.get_or_404(book_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(book, key, value)
        db.session.commit()
        return book.to_dict()

    @jwt_required()
    def delete(self, book_id):
        user = User.query.get(get_jwt_identity())
        if not user.is_admin:
            return error_response("Admins only", 403)

        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted"}, 200
