__author__ = 'kohn'

from mendeleycache.data.config import create_engine
from mendeleycache.config import DatabaseConfiguration
from mendeleycache.data.schema import read_mysql_schema, read_sqlite_schema
from mendeleycache.data.api_scripts import ApiScripts
from mendeleycache.data.crawl_scripts import CrawlScripts

from sqlalchemy.exc import DBAPIError


class DataController:
    """
    The DataController provides access to the engine
    """

    def __init__(self, config: DatabaseConfiguration):
        self._config = config
        self._engine = create_engine(self._config)
        self._api_data = ApiScripts(self._engine)
        self._crawl_data = CrawlScripts(self._engine)

    @property
    def engine(self):
        """
        Return the initialized database engine
        :return:
        """
        return self._engine

    @property
    def api_data(self):
        return self._api_data

    @property
    def crawl_data(self):
        return self._crawl_data

    def table_exists(self, table_name: str) -> bool:
        """
        Tests if the database is already initialized
        :return:
        """
        try:
            with self._engine.connect() as conn:
                result = conn.execute("SELECT * FROM %s" % table_name)
                return True
        except DBAPIError as e:
            return False

    def run_schema(self):
        """
        Runs the schema initialization and returns if it was successfull
        """
        schema = []
        if self._config.engine == "sqlite":
            schema = read_sqlite_schema()
        elif self._config.engine == "mysql":
            schema = read_mysql_schema()

        with self._engine.connect() as conn:
            for cmd in schema:
                conn.execute(cmd)

