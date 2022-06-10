from moonlan.dal.infrastructure.base_query_builders.insert_one_query_builder import InsertOneQueryBuilder
from moonlan.models.internal_user import InternalUser


class CreateUserQueryBuilder(InsertOneQueryBuilder):
    def __init__(self, user: InternalUser):
        self._user = user

    def _get_document(self) -> dict:
        return self._user.dict()
