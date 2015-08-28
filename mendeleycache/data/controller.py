__author__ = 'kohn'

from mendeleycache.config import DatabaseConfiguration
from mendeleycache.data.api_data import ApiData
from mendeleycache.data.crawl_data import CrawlData
from mendeleycache.data.reader import read_sql_statements
from mendeleycache.utils.exceptions import InvalidConfigurationException
from mendeleycache.config import DatabaseConfiguration, MySQLConfiguration, SQLiteConfiguration
from mendeleycache.logging import log
import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DBAPIError

from mendeleycache.logging import log


def create_engine(config: DatabaseConfiguration) -> Engine:
    path = ""
    if config.engine == "mysql":
        path = "mysql://{user}:{secret}@{host}:{port}/{db}".format(
            user=config.user,
            secret=config.secret,
            host=config.hostname,
            port=config.port,
            db=config.db
        )
    elif config.engine == "sqlite":
        if not config.path:
            path = "sqlite://"
        else:
            path = "sqlite:///{path}".format(
                path=config.path
            )
    else:
        log.warn("Unknown engine '%s'" % config.engine)
        raise InvalidConfigurationException("Unknown database engine")

    log.info("Creating engine '{engine}' with path {path}".format(
        engine=config.engine,
        path=path
    ))

    # create engine
    return sqlalchemy.create_engine(path)


class DataController:
    """
    The DataController provides access to the engine
    """

    def __init__(self, config: DatabaseConfiguration):
        self._config = config
        self._engine = create_engine(self._config)
        self._api_data = ApiData(self._engine)
        self._crawl_data = CrawlData(self._engine)

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

    def is_initialized(self):
        """
        Checks whether all the different tables exist
        """
        return (
            self.table_exists('document') and
            self.table_exists('profile') and
            self.table_exists('cache_document') and
            self.table_exists('cache_profile') and
            self.table_exists('cache_field') and
            self.table_exists('cache_profile_has_cache_document') and
            self.table_exists('cache_document_has_cache_field')
        )

    def run_schema(self):
        """
        Runs the schema initialization and returns if it was successfull
        """
        schema = []
        if self._config.engine == "sqlite":
            schema = read_sql_statements('sql', 'schema', 'sqlite.sql')
        elif self._config.engine == "mysql":
            schema = read_sql_statements('sql', 'schema', 'mysql.sql')

        with self._engine.begin() as conn:
            for cmd in schema:
                conn.execute(cmd)

        log.info("Schema has been initialized")

    def drop_all(self):
        drops = read_sql_statements('sql', 'schema', 'drop_all.sql')

        with self._engine.begin() as conn:
            for drop in drops:
                log.info(drop)
                conn.execute(drop)

        log.info("Database has been dropped")

    def assert_schema(self):
        if self.is_initialized():
            log.info("Schema is already initialized")
        else:
            log.warning("The current schema is incomplete. Starting migration.")
            # TODO: Backup && Restore as soon as the database has state
            self.drop_all()
            self.run_schema()
