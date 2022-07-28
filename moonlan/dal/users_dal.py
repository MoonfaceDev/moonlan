from pymongo import MongoClient

from moonlan import consts
from moonlan.config import config
from moonlan.dal.documents.user_document import UserDocument
from moonlan.dal.infrastructure.query_executors.find_one import find_one
from moonlan.dal.infrastructure.query_executors.insert_one import insert_one
from moonlan.dal.query_builders.users.create_user_query_builder import CreateUserQueryBuilder
from moonlan.dal.query_builders.users.user_by_email_query_builder import UserByEmailQueryBuilder
from moonlan.models.internal_user import InternalUser

collection = MongoClient(consts.Database.HOSTNAME).get_database(config.database.database_name).get_collection(
    consts.Database.USERS_COLLECTION_NAME
)


@find_one(collection, UserDocument)
def get_user_by_email(email: str):
    return UserByEmailQueryBuilder(email).build()


@insert_one(collection)
def create_user(user: InternalUser):
    return CreateUserQueryBuilder(user).build()
