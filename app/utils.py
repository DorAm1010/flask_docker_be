import re
import secrets

# generate uuid for unique identification of user
def generate_unique_id():
    return secrets.token_hex(4)[:8]

# validate name
def is_valid_name(name):
    return len(name) >= 3

#validate email
def is_valid_email(email):
    # Regular expression for a simple email validation
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))

#validate password
def is_valid_password(password):
    password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    return bool(re.match(password_pattern, password))

# import re
# from flask import abort

# def validate_password(password: str):
#     pattern = re.compile(
#         r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$'
#     )
#     if not pattern.match(password):
#         abort(400, description="Password must be at least 8 characters long and include one lowercase letter, one uppercase letter, and one special character.")
