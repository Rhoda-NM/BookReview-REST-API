from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from .config import Config
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()
bcrypt = Bcrypt()
api = Api()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from app.models import User, Book, Review
    from app.routes import auth_bp, BookListResource, BookResource, ReviewListResource, ReviewResource

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    api.add_resource(BookListResource, '/books')
    api.add_resource(BookResource, '/books/<int:book_id>')
    api.add_resource(ReviewListResource, '/books/<int:book_id>/reviews')
    api.add_resource(ReviewResource, '/reviews/<int:review_id>')

    return app