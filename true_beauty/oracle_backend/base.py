from django.db.backends.oracle.base import DatabaseWrapper as OracleDatabaseWrapper

from .introspection import DatabaseIntrospection


class DatabaseWrapper(OracleDatabaseWrapper):
    introspection_class = DatabaseIntrospection
