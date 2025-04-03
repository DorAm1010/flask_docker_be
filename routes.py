from flask import request, jsonify, flash, redirect, render_template, url_for, session
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from utils import generate_unique_id, is_valid_name, is_valid_email, is_valid_password
from decorators import route_enabled




users = db["user"]

def register_routes(app, db):
    @app.route('/hello', methods=['GET'])
    def hello():
        return jsonify({"message": "Hello, Docker!"})


    @app.route('/')
    def home():
        user = session.get('user')
        if user:
            return render_template('index.html', user=user)
        else:
            return render_template('landing_page.html')

    @app.route('/error_404')
    def error_404():
        return '404 error'

    @app.route('/signup', methods=['GET', 'POST'])
    @route_enabled('signup')
    def signup():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            term_condition = request.form.get('term_condition')

            # validating the user input
            if not name or not email or not password or not confirm_password:
                flash('All fields must be filled out.', 'error')
            elif password != confirm_password:
                flash('Password and confirm password do not match.', 'error')
            elif not is_valid_name(name):
                flash('Please enter a valid name.', 'error')
            elif not is_valid_email(email):
                flash('Please enter a valid email address.', 'error')
            elif not is_valid_password(password):
                flash('Please enter a strong password.', 'error')
            elif not term_condition:
                flash('Terms and conditions must be accepted.', 'error')
            else:
                #checking if email exists or not
                existing_user = users.find_one({'email': email})
                if existing_user:
                    flash('Email already registered. Please use a different email.', 'error')
                else:
                    #hashing password
                    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                    #genrating unique_hash
                    unique_id = generate_unique_id()
                    # Get the current time
                    current_time = datetime.utcnow()

                    user_data = {
                        'uuid':unique_id,
                        'name': name,
                        'email': email,
                        'role':'user',
                        'password':hashed_password,
                        'text_password':password, # removed before going to live
                        'created_At':current_time
                    }

                    users.insert_one(user_data)
                    flash('Signup successful! Please login.', 'success')
                    return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/', methods=['GET'])
    @app.route('/logout')
    def logout():
        user = session.get('user')
        if user:
            session.pop('user', None)
        else:
            session.pop('admin', None)
        flash('Logout successful!', 'success')
        return redirect(url_for('login'))

    @app.route('/login',methods=['GET', 'POST'])
    @route_enabled('login')
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            if not email or not password:
                flash('All fields must be filled out.', 'error')
            elif not is_valid_email(email):
                flash('Please enter a valid email address.', 'error')
            elif not is_valid_password(password):
                flash('Please enter a strong password.', 'error')
            else:
                #finding user with that email
                user = users.find_one({'email': email})
                if user and check_password_hash(user['password'], password):
                    if user['role'] == 'admin':
                        session['admin'] = {'uuid': user['uuid'], 'name': user['name'], 'email': user['email'],'role':user['role']}
                        return redirect(url_for('admin_dashboard'))                    
                    else:
                        session['user'] = {'uuid': user['uuid'], 'name': user['name'], 'email': user['email'],'role':user['role']}
                        # flash('Login successful!', 'success')
                        return redirect(url_for('home'))
                else:
                    flash('Invalid email or password. Please try again.', 'error')
        return render_template('login.html')
    



