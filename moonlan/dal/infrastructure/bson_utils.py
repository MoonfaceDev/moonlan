from bson.objectid import ObjectId as BsonObjectId


class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value) -> BsonObjectId:
        if not isinstance(value, BsonObjectId):
            raise TypeError('ObjectId required')
        return value
