from moonlan.models.user import User


class InternalUser(User):
    hashed_password: str
