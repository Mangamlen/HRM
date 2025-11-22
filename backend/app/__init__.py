from flask import Flask
from .extensions import db
from .routes import api_bp
from .config import Config

def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix='/api')
    with app.app_context():
        # create tables
        db.create_all()
        # create an initial admin user if not exists
        from .models import User
        if User.query.filter_by(username='admin').first() is None:
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    return app
