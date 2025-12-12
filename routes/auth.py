from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import User
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate input
        if not all([name, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return render_template('register.html', name=name, email=email)
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html', name=name, email=email)
        
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Please enter a valid email address', 'danger')
            return render_template('register.html', name=name, email=email)
        
        # Password validation (at least 6 characters)
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template('register.html', name=name, email=email)
        
        # Create user
        if User.create(name, email, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email already exists', 'danger')
            return render_template('register.html', name=name)
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        if not all([email, password]):
            flash('All fields are required', 'danger')
            return render_template('login.html', email=email)
        
        # Authenticate user
        user = User.authenticate(email, password)
        
        if user:
            # Set session variables
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['is_admin'] = user['is_admin']
            
            if user['is_admin']:
                flash(f'Welcome back, Admin {user["name"]}!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash(f'Welcome back, {user["name"]}!', 'success')
                return redirect(url_for('quiz.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return render_template('login.html', email=email)
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Clear session
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))