import random

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from database import DbEngine


class User(UserMixin, DbEngine.BASE):
    """
    This is a class for managing the User model for the database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(128))
    unique_id = Column(String(180), unique=True, nullable=True)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the password for checking and being saved.

        :param password: (str) password to be hashed
        :return: (str) hashed password
        """
        return generate_password_hash(password=password)

    def check_password(self, password: str) -> bool:
        """
        Checks the password to see if it matches the User's password.

        :param password: (str) password to be checked
        :return: True is matched => False if not
        """
        return check_password_hash(self.password, password)

    def _generate_unique_id(self) -> str:
        """
        Generates a random id so the user can be identified by other users when adding them as contact.

        :return: (str) the unique ID for the user
        """
        random_int: int = random.randint(3, 900)
        return f"{self.username[0].upper()}{self.username[1].upper()}{random_int}"

    def save_instance(self) -> None:
        """
        Saves instance to database.

        :return: None
        """
        self.password = self.hash_password(password=self.password)
        self.unique_id = self._generate_unique_id()
        database = DbEngine()
        database.session.add(self)
        database.session.commit()

    def __repr__(self) -> str:
        return "<User: {}>".format(self.username)