from pymongo import MongoClient

from moonlan.authentication.base_user_provider import BaseUserProvider
from moonlan.models.internal_user import InternalUser


class DatabaseUserProvider(BaseUserProvider):
    def __init__(self, database_name: str):
        self._users = MongoClient().get_database(database_name).get_collection('users')

    def get_user(self, email: str) -> InternalUser:
        user_dict = self._users.find_one({
            'email': email
        })
        if user_dict is not None:
            return InternalUser(**user_dict)

    def insert_user(self, user: InternalUser):
        self._users.insert_one(user.dict())
