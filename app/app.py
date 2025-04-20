from flask import Flask
from flask import Flask
from app.models import db
from flask_jwt_extended import JWTManager



def create_app(database_uri='sqlite:///app.db'):
    """Create and configure the flask application"""
    app = Flask(__name__)
    # app.config['DATABASE_URI'] = '123'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri  # Or your preferred DB
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Should come from your .env in production
    jwt = JWTManager(app)
    db.init_app(app)

    with app.app_context():
        from app.models.user import User
        from app.models.blog import Blog
        db.create_all()

        from app.routes.auth_routes import auth_bp
        from app.routes.blog_routes import blog_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(blog_bp)
        @app.route("/")
        def hello_world():
            return "<p>Hello, World!</p>"

    # migrate = Migrate(app, db)

    return app
