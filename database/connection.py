from pymysql import connect
from pymysql.err import OperationalError


class DBContextManager:
    def __init__(self, config: dict):
        self.config = config
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()

            self.conn.begin()

            return self.cursor

        except OperationalError as err:
            print(err.args)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type:
            print(exc_type, exc_val)

        if self.cursor and self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()

            self.cursor.close()
            self.conn.close()
        return True
