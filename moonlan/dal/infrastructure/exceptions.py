class DatabaseError(Exception):
    pass


class DocumentNotFoundError(DatabaseError):
    pass


class QueryBuildingError(DatabaseError):
    pass


class QueryExecutionError(DatabaseError):
    pass
