import re
from models.user import User


def is_valid_username(uname) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9]{5,}$", uname))

def validate_username(old_username, new_username) -> bool:
    return old_username == new_username

def validate_password(password, confirm_password) -> bool:
    return password == confirm_password


# Check if same username already exists in db.
def validate_user(username) -> bool:
    user = User.get_user_by_username(username)
    return True if user else False


def get_user_info(username: str) -> dict:
    if not validate_username(username):
        return None
    user_data = User.get_user_by_username(username)
    return user_data


def authorise_info(new_data: str, data: str) -> bool:
    if User.authorise(new_data, data):
        return True
    return False


def update_password(user_id, new_password, new_sq, new_sa) -> bool:
    hashed_password = User.encrypt(new_password)
    hashed_sa = User.encrypt(new_sa)
    if User.update_user(user_id, None, hashed_password, new_sq, hashed_sa):
        return True
    return False


def update_username(user_id: int, new_username: str) -> bool:
    if User.update_user(user_id, new_username):
        return True
    return False


def register_user(username, password, security_question, security_answer):
    if User.create_user(username, password, security_question, security_answer):
        return True
    return False


def get_user_by_user_id(user_id: int) -> dict:
    return User.get_user(user_id)


def login():
    pass
