from app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    published_date = db.Column(db.DateTime, default=datetime.utcnow)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cover_url = db.Column(db.String(255), nullable=True)

    average_rating = db.Column(db.Float, default=0.0)

    # Relationships
    reviews = db.relationship('Review', back_populates='book', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'