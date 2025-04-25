from app import db
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='user', cascade="all, delete-orphan")

    def set_password(self, password):
        """Hash the password and store it in the database."""
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check the hashed password against the provided password."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    