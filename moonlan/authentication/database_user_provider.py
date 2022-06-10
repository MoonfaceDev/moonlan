from moonlan.authentication.base_user_provider import BaseUserProvider
from moonlan.dal import users_dal
from moonlan.dal.infrastructure.exceptions import DocumentNotFoundError
from moonlan.models.internal_user import InternalUser


class DatabaseUserProvider(BaseUserProvider):

    def get_user(self, email: str) -> InternalUser | None:
        try:
            user_document = users_dal.get_user_by_email(email)
        except DocumentNotFoundError:
            return None
        return InternalUser(**user_document.dict())

    def insert_user(self, user: InternalUser):
        users_dal.create_user(user)
