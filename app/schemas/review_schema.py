from app import ma
from app.models import Review
from marshmallow import fields

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= Review
        load_instance = True

    id = fields.Int(dump_only=True)
    rating = fields.Int(required=True)
    comment = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    book_id = fields.Int(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

review_schema = ReviewSchema()  
review_list_schema = ReviewSchema(many=True)