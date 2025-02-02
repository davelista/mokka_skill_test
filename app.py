from flask import Flask
from routes.users_routes import users_bp
from routes.auth_routes import auth_bp

from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback_jwt_secret")

jwt = JWTManager(app)
@app.route('/')
def index():
    return 'Hello World!'

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
