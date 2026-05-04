from django.db.backends.oracle.introspection import (
    DatabaseIntrospection as OracleDatabaseIntrospection,
    TableInfo,
)


class DatabaseIntrospection(OracleDatabaseIntrospection):
    def get_table_list(self, cursor):
        """Avoid USER_TABLES, which raises ORA-00600 on this local Oracle."""
        cursor.execute("""
            SELECT object_name, 't', NULL
            FROM user_objects
            WHERE
                object_type = 'TABLE'
                AND object_name NOT IN (
                    SELECT mview_name FROM user_mviews
                )
            UNION ALL
            SELECT view_name, 'v', NULL FROM user_views
            UNION ALL
            SELECT mview_name, 'v', NULL FROM user_mviews
        """)
        return [
            TableInfo(self.identifier_converter(row[0]), row[1], row[2])
            for row in cursor.fetchall()
        ]
