from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps

# Import routes
from routes.auth import auth_bp
from routes.quiz import quiz_bp
from routes.admin import admin_bp

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secure secret key for sessions

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(admin_bp)

# Initialize database
from database import init_db
init_db()

# Root route
@app.route('/')
def index():
    return render_template('index.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="404 - Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error="500 - Internal Server Error"), 500

if __name__ == '__main__':
    app.run(debug=True)