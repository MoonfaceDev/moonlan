from moonlan.dal.infrastructure.base_query_builders.find_one_query_builder import FindOneQueryBuilder


class UserByEmailQueryBuilder(FindOneQueryBuilder):
    def __init__(self, email: str):
        self._email = email

    def _get_filter(self) -> dict:
        return {
            'email': self._email
        }
