from flask_restful import Resource
from flask import request
from app.models import Book, User, Review
from app import db
from app.schemas.book_schema import book_schema, book_list_schema
from app.utils import success_response, error_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import error_response, success_response
from sqlalchemy import func


class BookListResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        genre = request.args.get('genre', type=str)
        author = request.args.get('author', type=str)
        sort_by = request.args.get('sort_by', 'created_at')
        sort_dir = request.args.get('sort_dir', 'desc')
        search_query = request.args.get('q', type=str)

        query = Book.query

        if genre:
            query = query.filter(Book.genre.ilike(f"%{genre}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if search_query:
            query = query.filter(
                db.or_(
                    Book.title.ilike(f"%{search_query}%"),
                    Book.description.ilike(f"%{search_query}%"),
                    Book.author.ilike(f"%{search_query}%")
                )
            )
        if hasattr(Book, sort_by):
            sort_attr = getattr(Book, sort_by)
            query = query.order_by(sort_attr.desc() if sort_dir == 'desc' else sort_attr.asc())

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return success_response({
            "books": [
                {
                    **book.to_dict(),
                    "average_rating": round(
                        db.session.query(func.avg(Review.rating))
                        .filter(Review.book_id == book.id)
                        .scalar() or 0, 2
                    )
                }
                for book in paginated.items
            ],
            "total": paginated.total,
            "page": paginated.page,
            "pages": paginated.pages,
            "per_page": paginated.per_page
        })

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
        return success_response(book.to_dict(), "Book created successfully", 201)


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
