from flask import request, jsonify, Blueprint
from flask_api import status
from models import db
from models.blog import Blog
import os

blog_bp = Blueprint('blog', __name__, url_prefix='/blogs')

# Directory to save uploaded images
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@blog_bp.route('/create-blog', methods=['POST'])
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
    }), status.HTTP_201_CREATED

@blog_bp.route('/<int:blog_id>', methods=['GET'])
def get_blog_by_id(blog_id):
    """Get a single blog entry by its ID."""
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"error": "Blog not found"}), status.HTTP_404_NOT_FOUND

    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url
    }), status.HTTP_200_OK

@blog_bp.route('/<string:blog_title>', methods=['GET'])
def get_blog_by_title(blog_titlee):
    """Get a single blog entry by its ID."""
    blog = Blog.query.get(blog_titlee)
    if not blog:
        return jsonify({"error": f"Blog with title {blog_titlee} not found"}), status.HTTP_404_NOT_FOUND

    return jsonify({
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url
    }), status.HTTP_200_OK


@blog_bp.route('/all', methods=['GET'])
def get_all_blogs():
    """Get a list of all blog entries."""
    blogs = Blog.query.all()
    # results = []
    # for blog in blogs:
    #     results.append({
    #         "id": blog.id,
    #         "title": blog.title,
    #         "content": blog.content,
    #         "image_url": blog.image_url
    #     })
    return jsonify(blogs), status.HTTP_200_OK

@blog_bp.route('/<int:blog_id>', methods=['PUT'])
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
    }), status.HTTP_200_OK

@blog_bp.route('/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    """Delete a blog entry."""
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"error": "Blog not found"}), status.HTTP_404_NOT_FOUND

    db.session.delete(blog)
    db.session.commit()
    return jsonify({"message": f"Blog {blog_id} deleted successfully!"}), status.HTTP_200_OK