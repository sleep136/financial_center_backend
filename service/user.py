from models.User import get_user_by_name,verify_password


def authenticate(username, password):
    user = get_user_by_name(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user






