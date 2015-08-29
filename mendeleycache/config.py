__author__ = 'kohn'

import os
from os.path import exists
from mendeleycache.utils.files import get_relative_path
from mendeleycache.utils.exceptions import InvalidConfigurationException

class CrawlerConfiguration:
    """
    Configuration of a base crawler
    """
    def __init__(self, research_group: str):
        self._research_group = research_group

    @property
    def research_group(self):
        return self._research_group


class SDKCrawlerConfiguration(CrawlerConfiguration):
    """
    Configuration of the SDK crawler
    """
    def __init__(self, research_group: str,  app_id: str, app_secret: str,):
        self._app_id = app_id
        self._app_secret = app_secret
        super(SDKCrawlerConfiguration, self).__init__(research_group)

    @property
    def app_id(self):
        return self._app_id
    
    @property
    def app_secret(self):
        return self._app_secret


class FileCrawlerConfiguration(CrawlerConfiguration):
    """
    Configuration of the file crawler
    """
    def __init__(self, research_group: str):
        super(FileCrawlerConfiguration, self).__init__(research_group)


class DatabaseConfiguration:
    """
    Configuration of the database access
    """
    def __init__(self, engine: str, ):
        self._engine = engine

    @property
    def engine(self):
        return self._engine


class MySQLConfiguration(DatabaseConfiguration):
    def __init__(self, hostname: str, port: str, db: str, user: str, secret: str):
        self._hostname = hostname
        self._port = port
        self._db = db
        self._user = user
        self._secret = secret
        super(MySQLConfiguration, self).__init__('mysql')

    @property
    def hostname(self):
        return self._hostname

    @property
    def port(self):
        return self._port

    @property
    def db(self):
        return self._db

    @property
    def user(self):
        return self._user

    @property
    def secret(self):
        return self._secret


class SQLiteConfiguration(DatabaseConfiguration):
    def __init__(self, path: str):
        self._path = path
        super(SQLiteConfiguration, self).__init__('sqlite')

    @property
    def path(self):
        return self._path


class ServiceConfiguration:
    """
    Configuration of the Mendeley Cache
    """
    def __init__(self):
        self._crawler = None
        """:type : MendeleyConfiguration"""

        self._database = None
        """:type : DatabaseConfiguration"""

        self._version = "0.1.0"

    @property
    def crawler(self):
        return self._crawler

    @property
    def database(self):
        return self._database

    @property
    def version(self):
        return self._version

    def load(self):
        """
        The load function loads the configuration from environment variables
        It returns nothing but raises InvalidConfigurationExceptions if something is missing
        :return:
        """

        # First read all environment variables with default values

        # Crawler
        crawler = os.environ['MC_CRAWLER'] if 'MC_CRAWLER' in os.environ else 'file'
        app_id = os.environ['MC_APP_ID'] if 'MC_APP_ID' in os.environ else ''
        app_secret = os.environ['MC_APP_SECRET'] if 'MC_APP_SECRET' in os.environ else ''
        research_group = os.environ['MC_RESEARCH_GROUP'] if 'MC_RESEARCH_GROUP' in os.environ else 'd0b7f41f-ad37-3b47-ab70-9feac35557cc'

        # Database
        database_engine = os.environ['MC_DATABASE_ENGINE'] if 'MC_DATABASE_ENGINE' in os.environ else 'sqlite'
        # Mysql
        database_path = os.environ['MC_DATABASE_PATH'] if 'MC_DATABASE_PATH' in os.environ else ''
        # Sqlite
        database_hostname = os.environ['MC_DATABASE_HOSTNAME'] if 'MC_DATABASE_HOSTNAME' in os.environ else 'localhost'
        database_port = os.environ['MC_DATABASE_PORT'] if 'MC_DATABASE_PORT' in os.environ else ''
        database_db = os.environ['MC_DATABASE_DB'] if 'MC_DATABASE_DB' in os.environ else ''
        database_user = os.environ['MC_DATABASE_USER'] if 'MC_DATABASE_USER' in os.environ else ''
        database_secret = os.environ['MC_DATABASE_SECRET'] if 'MC_DATABASE_SECRET' in os.environ else ''

        def missing_attribute(attribute: str):
            raise InvalidConfigurationException("Environment misses variable: %s" % attribute)

        # Then validate these settings
        if crawler == 'file':
            self._crawler = FileCrawlerConfiguration(research_group)
        elif crawler == 'mendeley':
            if not app_id:
                missing_attribute('MC_APP_ID')
            if not app_secret:
                missing_attribute('MC_APP_SECRET')
            if not research_group:
                missing_attribute('MC_RESEARCH_GROUP')
            self._crawler = SDKCrawlerConfiguration(
                research_group=research_group,
                app_id=app_id,
                app_secret=app_secret
            )
        else:
            raise InvalidConfigurationException('Unknown crawler type %s' % crawler)

        if database_engine == 'sqlite':
            # If no path has been provided the in memory version is used
            self._database = SQLiteConfiguration(database_path)
        elif database_engine == 'mysql':
            if not database_hostname:
                missing_attribute('MC_DATABASE_HOSTNAME')
            if not database_port:
                missing_attribute('MC_DATABASE_PORT')
            if not database_db:
                missing_attribute('MC_DATABASE_DB')
            if not database_user:
                missing_attribute('MC_DATABASE_USER')
            if not database_secret:
                missing_attribute('MC_DATABASE_SECRET')
            self._database = MySQLConfiguration(
                hostname=database_hostname,
                port=database_port,
                db=database_db,
                user=database_user,
                secret=database_secret
            )
        else:
            raise InvalidConfigurationException('Unknown database engine %s' % database_engine)
