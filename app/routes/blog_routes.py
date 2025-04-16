from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import db
from app.models.blog import Blog
import os

blog_bp = Blueprint('blog', __name__, url_prefix='/blogs')

# Directory to save uploaded images
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@blog_bp.route('/create-blog', methods=['POST'])
@jwt_required() 
def create_blog():
    """Create a new blog entry."""
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files.get('image')  # Optional file upload

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    image_url = None
    if file:
        filename = file.filename  # In a production app, secure and validate this filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        image_url = file_path  # Or adjust URL as needed if serving static files

    blog = Blog(title=title, content=content, image_url=image_url)
    db.session.add(blog)
    db.session.commit()
    
    return jsonify({
        "message": f"Blog '{title}' created successfully!",
        "blog": {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "image_url": blog.image_url
        }
    }), 201

@blog_bp.route('/<int:blog_id>', methods=['GET'])
def get_blog_by_id(blog_id):
    """Get a single blog entry by its ID."""
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"error": "Blog not found"}), 404

    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url
    }), 200

@blog_bp.route('/<string:blog_title>', methods=['GET'])
def get_blog_by_title(blog_title):
    """Get a single blog entry by its ID."""
    blog = Blog.query.get(blog_title)
    if not blog:
        return jsonify({"error": f"Blog with title {blog_title} not found"}), 404

    return jsonify({
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url
    }), 200


@blog_bp.route('/all', methods=['GET'])
def get_all_blogs():
    """Get a list of all blog entries."""
    blogs = Blog.query.all()
    return jsonify(blogs), 200

@blog_bp.route('/my-blogs', methods=['GET'])
@jwt_required()  # This enforces JWT protection on this route.
def get_user_blogs():
    current_user_id = get_jwt_identity()  # Retrieve the identity (e.g., user ID) from the token.
    user_blogs = Blog.query.filter_by(user_id=current_user_id).all()
    # Assume each Blog model has a `to_dict()` method for serialization
    return jsonify([blog.to_dict() for blog in user_blogs]), 200

@blog_bp.route('/<int:blog_id>', methods=['PUT'])
@jwt_required()
def update_blog(blog_id):
    """Update an existing blog entry."""
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"error": "Blog not found"}), 404

    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files.get('image')

    if title:
        blog.title = title
    if content:
        blog.content = content
    if file:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        blog.image_url = file_path

    db.session.commit()
    return jsonify({
        "message": f"Blog {blog_id} updated successfully!",
        "blog": {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "image_url": blog.image_url
        }
    }), 200

@blog_bp.route('/<int:blog_id>', methods=['DELETE'])
@jwt_required()
def delete_blog(blog_id):
    """Delete a blog entry."""
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"error": "Blog not found"}), 404

    db.session.delete(blog)
    db.session.commit()
    return jsonify({"message": f"Blog {blog_id} deleted successfully!"}), 200