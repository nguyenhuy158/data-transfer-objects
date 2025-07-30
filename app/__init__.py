from flask import Flask, render_template
from config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Home route - Web interface
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/users')
    def users_page():
        return render_template('users.html')
    
    @app.route('/posts')
    def posts_page():
        return render_template('posts.html')
    
    return app