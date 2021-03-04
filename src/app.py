from typing import Dict, Optional, Union

from flask import Flask
from flask_admin import Admin

from admin_views.user_view import UserView
from database import DbEngine
from models.user import User

app = Flask(__name__)
database: DbEngine = DbEngine()

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(UserView(User, database.session))


@app.route("/")
def home():
    return "please go to admin"


@app.route("/create/<username>/<password>/")
def create_user(username: str, password: str) -> str:
    """
    This is a view that demonstrates how to create a user model.

    :param username: (str) the username to be created
    :param password: (str) the password for the user
    :return: (str) status confirming the creation
    """
    new_user: User = User(username=username, password=password)
    new_user.save_instance()
    return "user has been created"


@app.route("/get/<username>/")
def get_user(username: str) -> Union[Dict[str, Union[str, int]], str]:
    """
    This is a view that demonstrates how to get a user from the database.

    :param username: (str) the username of the user being queried from the database
    :return: (Union[Dict[str, Union[str, int]], str]) error message if not found, a Dict of user data if present in
             the database
    """
    db: DbEngine = DbEngine()

    user: Optional[User] = db.session.query(User).filter_by(username=username).one_or_none()

    if user is None:
        return f"user with the username {username} could not be found"

    return {
        "username": user.username,
        "password": user.password,
        "unique id": user.unique_id,
        "id": user.id
    }


@app.teardown_request
def teardown_request(*args, **kwargs):
    """
    This fires at the end of every request removing all database sessions so we do not jam our database.
    """
    database.session.expire_all()
    database.session.remove()


if __name__ == "__main__":
    app.run()
