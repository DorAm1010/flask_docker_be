from flask import Flask
from flask import Flask
from models import db


def create_app():
    """Create and configure the flask application"""
    app = Flask(__name__)
    app.config['DATABASE_URI'] = '123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Or your preferred DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes import user_bp, blog_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(blog_bp)

    # migrate = Migrate(app, db)

    return app
