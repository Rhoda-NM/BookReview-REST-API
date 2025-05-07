from  sqlalchemy import func
from app.models.reviews import Review
from app import db

def update_average_rating(book_id):
    avg = db.session.query(func.avg(Review.rating))\
        .filter(Review.book_id == book_id)\
        .scalar() or 0
    
    book = db.session.get(Book, book_id)
    book.average_rating = round(avg, 2)
    db.session.commit()

