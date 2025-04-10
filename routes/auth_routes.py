from flask import request, jsonify, Blueprint
from flask_api import status
from models import db
from models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username', default=None)
    email = data.get('email', default=None)
    password = data.get('password', default=None)
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), status.HTTP_400_BAD_REQUEST

    new_user = User(username=username, email=email, password=password)
    if User.query.filter(User.email == email).first():
        return jsonify({"error": "User with given email already exists"}), status.HTTP_409_CONFLICT

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': f'User {username} created successfully!'}), status.HTTP_201_CREATED


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username
    }), status.HTTP_200_OK

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first_or_404()
    if user.check_password(password):
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'username': user.username
        })
    return jsonify({
        'message': 'Invalid credentials',
        'status': 'error'
    })

@user_bp.route('/logout', methods=['POST'])
def logout():
    # TODO - Add token invalidation logic here
    return jsonify({"message": "Logout successful (client-side token invalidation required)"}), 200

@user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Deleted user with user_id = {user_id} successfully"}), 200

@user_bp.route('update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username and not email and not password:
        return jsonify({"error": "No fields to update"}), status.HTTP_400_BAD_REQUEST
    
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
    return jsonify(response_json), status.HTTP_200_OK

@user_bp.route('/all', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify(users), status.HTTP_200_OK

