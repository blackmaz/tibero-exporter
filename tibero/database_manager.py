import jaydebeapi
import logging
import os

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, db_config):
        self.host = db_config.host
        self.port = db_config.port
        self.sid = db_config.sid
        self.user = db_config.username
        self.password = db_config.password
        self.url = f"jdbc:tibero:thin:@{self.host}:{self.port}:{self.sid}"
        self.jdbc_jar = db_config.jdbc_jar
        self.driver = db_config.driver
        self.connection = None
        # JDBC 드라이버 존재 여부 확인
        if not os.path.exists(self.jdbc_jar):
            logger.warning(f"Can not find JDBC Driver: {self.jdbc_jar}")

    def connect(self):
        if self.connection:
            return self.connection
        self.connection = jaydebeapi.connect(
            self.driver,
            self.url,
            [self.user, self.password],
            jars=[self.jdbc_jar],
        )
        self.connection.jconn.setAutoCommit(False)

    def is_connected(self):
        if self.connection is None:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            cursor.close()
            return True
        except Exception:
            return False

    def get_connection(self):
        return self.connection

    def execute(self, sql_text):
        try:
            cursor = self.con.cursor()
            cursor.execute(sql_text)
        except TypeError as e:
            logger.error(f"Error while run sql to DBMS: {e}")
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            try:
                self.connection.close()
                logger.info("Database connection closed")
            except Exception as e:
                logger.error(f"Error while trying to close the connection: {e}")
            finally:
                self.connection = None
