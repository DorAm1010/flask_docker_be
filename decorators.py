from flask import session, flash, redirect, url_for
from functools import wraps
from app import db

# use a collection named "users"


global_settings = db['global_settings']

def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        user = session.get('user')        
        if 'user' in session and user['role'] == 'user':
            return route_function(*args, **kwargs)
        else:
            flash('You must be logged in to access this page.', 'error')
            return redirect(url_for('login'))
    return decorated_function

def onlyAdmin(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        admin = session.get('admin')
        if 'admin' in session and admin['role'] == 'admin':
            return route_function(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function


def route_enabled(route_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            route_settings = global_settings.find_one({'route_name': route_name})

            if route_settings and route_settings.get('is_enabled', False):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('error_404'))  # Forbidden, or redirect to a specific page if needed

        return wrapper
    return decorator
