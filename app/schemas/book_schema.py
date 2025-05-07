from app import ma
from app.models import Book
from marshmallow import fields

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
        
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    genre = fields.Str()
    isbn = fields.Str()
    summary = fields.Str()
    cover_url = fields.Str()
    published_date = fields.Date()
    created_at = fields.DateTime(dump_only=True)
    average_rating = fields.Float(dump_only=True)

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)