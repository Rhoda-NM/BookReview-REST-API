from flask_restful import Resource
from flask import request
from app import db
from app.models import Review, Book, User
from app.utils import error_response, success_response
from flask_jwt_extended import jwt_required, get_jwt_identity

class ReviewListResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return [review.to_dict() for review in book.reviews]

    @jwt_required()
    def post(self, book_id):
        user_id = get_jwt_identity()
        existing = Review.query.filter_by(user_id=user_id, book_id=book_id).first()
        if existing:
            return error_response("You've already reviewed this book", 400)

        data = request.get_json()
        review = Review(
            rating=data["rating"],
            comment=data.get("comment"),
            user_id=user_id,
            book_id=book_id
        )
        db.session.add(review)
        db.session.commit()
        return review.to_dict(), 201


class ReviewResource(Resource):
    @jwt_required()
    def put(self, review_id):
        user = User.query.get(get_jwt_identity())
        review = Review.query.get_or_404(review_id)
        if review.user_id != user.id and not user.is_admin:
            return error_response("Unauthorized", 403)

        data = request.get_json()
        review.rating = data.get("rating", review.rating)
        review.comment = data.get("comment", review.comment)
        db.session.commit()
        return review.to_dict()

    @jwt_required()
    def delete(self, review_id):
        user = User.query.get(get_jwt_identity())
        review = Review.query.get_or_404(review_id)
        if review.user_id != user.id and not user.is_admin:
            return error_response("Unauthorized", 403)

        db.session.delete(review)
        db.session.commit()
        return {"message": "Review deleted"}
