from app import ma
from app.models import User
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ("id", "username", "email","is_admin", "created_at")

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)
