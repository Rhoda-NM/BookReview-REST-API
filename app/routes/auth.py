from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utils import success_response, error_response

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return error_response("Missing Fields", 400)

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return error_response("User already exists", 409)

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return error_response("Invalid Credentials", 401)



@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", 404)
    
    return success_response(user.to_dict()), 200

"""@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():

    # Invalidate the token (this is a placeholder, actual implementation may vary)
    return jsonify({"message": "Logged out"}), 200"""