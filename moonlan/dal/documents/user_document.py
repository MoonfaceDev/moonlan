from pydantic import BaseModel

from moonlan.dal.infrastructure.bson_utils import ObjectId


class UserDocument(BaseModel):
    id: ObjectId
    full_name: str
    email: str
    hashed_password: str
    disabled: bool

    class Config:
        fields = {'id': '_id'}
