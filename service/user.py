from models import User


def get_user(username:str):
    if username in User:
        user_dict = db[username]
        return UserInDb(**user_dict)


def authenticate(username, password):
    user = get_user(username)