import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)
    
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def find_user_by_id(user_id):
    for u in load_users():
        if u["id"] == user_id:
            return u
    return None

def find_user_by_email(email):
    for u in load_users():
        if u["email"] == email:
            return u
    return None

def verify_user(email, password):
    user = find_user_by_email(email)
    if user and check_password_hash(user["password"], password):
        return user
    return None

def register_user(name, email, password):
    users = load_users()
    if find_user_by_email(email):
        return None, "Email already registered"
    new_user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "is_admin": False
    }
    users.append(new_user)
    save_users(users)
    return new_user, None