from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required
from app.models import db
from app.models.user import User
from app.utils import is_valid_email, is_valid_password



auth_bp = Blueprint('user', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
    if not is_valid_password(password):
        return jsonify({'error': 'Password must be at least 8 characters long,'
        ' contain at least one uppercase, one lowecase and a special caracter'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email!'}), 400


    new_user = User(username=username, email=email, password=password)
    if User.query.filter(User.email == email).first():
        return jsonify({"error": "User with given email already exists"}), 409

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': f'User {username} created successfully!'}), 201


@auth_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return jsonify(user.to_dict()), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first_or_404()
    if user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'message': 'Login successful',
            'user': {
                'user_id': user.id,
                'username': user.username,
                'token': access_token
            }
        }), 200
    return jsonify({
        'message': 'Invalid credentials',
        'status': 'error'
    }), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # TODO - Add token invalidation logic here
    return jsonify({"message": "Logout successful (client-side token invalidation required)"}), 200

@auth_bp.route('/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = db.session.execute(
        db.select(User).
        filter_by(id=user_id).
        limit(1)
        ).scalars().first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Deleted user with user_id = {user_id} successfully"}), 200

@auth_bp.route('/update/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = db.session.execute(
        db.select(User).
        filter_by(id=user_id).
        limit(1)
        ).scalars().first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username and not email and not password:
        return jsonify({"error": "No fields to update"}), 400
    
    response_json = {
        "message": "User updated successfully, fields updated: ",
    }
    fields = []
    if username:
        user.username = username
        fields.append('username')
    if email:
        user.email = email
        fields.append('email')
    if password:
        user.set_password(password)
        fields.append('password')
    response_json['message'] += ', '.join(fields) + '.'
    db.session.commit()
    return jsonify(response_json), 200

@auth_bp.route('/all', methods=['GET'])
def get_all_users():
    users = [u.to_dict() for u in User.query.all()]
    return jsonify(users), 200

