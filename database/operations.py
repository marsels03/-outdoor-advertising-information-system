from database.connection import DBContextManager


def select_from_DB(db_config: object, sql: object) -> object:
    with DBContextManager(db_config) as cursor:
        if cursor:
            cursor.execute(sql)
            schema = [column[0] for column in cursor.description]
            result = [dict(zip(schema, row)) for row in cursor.fetchall()]
            return result
        else:
            raise ValueError("Cursor hasn't created")


def execute_sql(db_config, _sql):
    with DBContextManager(db_config) as cursor:
        if cursor:
            cursor.execute(_sql)
            return True
        else:
            raise ValueError("Cursor hasn't created")

def call_proc(db_config, proc_name, param_list):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        result = cursor.callproc(proc_name, args=param_list)

        return result


def execute_transaction(db_config, sql_statements):
    with DBContextManager(db_config) as cursor:
        if not cursor:
            raise ValueError('Курсор не создан')

        for sql in sql_statements:
            cursor.execute(sql)

        return True
