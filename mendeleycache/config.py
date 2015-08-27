__author__ = 'kohn'

import os
from os.path import exists
from mendeleycache.utils.files import get_relative_path
from mendeleycache.utils.exceptions import InvalidConfigurationException
import yaml


class MendeleyConfiguration:
    """
    Configuration of the Mendeley API app access
    """
    def __init__(self, app_id: str, app_secret: str, research_group: str):
        self._app_id = app_id
        self._app_secret = app_secret
        self._research_group = research_group

    @property
    def app_id(self):
        return self._app_id
    
    @property
    def app_secret(self):
        return self._app_secret

    @property
    def research_group(self):
        return self._research_group


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
    def __init__(self, engine: str, hostname: str, port: str, db: str, user: str, secret: str):
        self._hostname = hostname
        self._port = port
        self._db = db
        self._user = user
        self._secret = secret
        super(MySQLConfiguration, self).__init__(engine)

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
    def __init__(self, engine: str, path: str):
        self._path = path
        super(SQLiteConfiguration, self).__init__(engine)

    @property
    def path(self):
        return self._path


class GeneralConfiguration:
    """
    General configuration of the Mendeley Cache
    """
    def __init__(self):
        pass


class ServiceConfiguration:
    """
    Configuration of the Mendeley Cache
    """
    def __init__(self):
        self._mendeley = None
        """:type : MendeleyConfiguration"""

        self._database = None
        """:type : DatabaseConfiguration"""

        self._general = None
        """:type : GeneralConfiguration"""

        self._version = "0.1.0"

    @property
    def mendeley(self):
        return self._mendeley

    @property
    def database(self):
        return self._database

    @property
    def version(self):
        return self._version

    def load(self):
        """
        The load function loads the configuration from disk
        It returns nothing but raises InvalidConfigurationExceptions if something is missing
        :return:
        """

        # Construct a file path relative to the project root
        if "MENDELEY_CACHE_CONFIG" in os.environ:
            path_str = os.environ["MENDELEY_CACHE_CONFIG"]
            path = os.path.abspath(path_str)
        else:
            path = get_relative_path('config.yml')

        # Check if path exists
        if not exists(path):
            raise InvalidConfigurationException("config.yml not found")

        def missing_attribute(attribute: str):
            raise InvalidConfigurationException("config.yml misses attribute: %s" % attribute)

        # Parse yaml and get attributes
        with open(path, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

            # First check the yaml top level attributes
            if 'mendeley' not in cfg:
                missing_attribute('mendeley')
            if 'database' not in cfg:
                missing_attribute('database')
            # if 'general' not in cfg:
            #    missing_attribute('general')

            # Then start fetching the mendeley api config
            mendeley_data = cfg['mendeley']
            if 'app_id' not in mendeley_data:
                missing_attribute('mendeley.app_id')
            if 'app_secret' not in mendeley_data:
                missing_attribute('mendeley.app_secret')
            if 'research_group' not in mendeley_data:
                missing_attribute('mendeley.research_group')
            self._mendeley = MendeleyConfiguration(
                mendeley_data['app_id'],
                mendeley_data['app_secret'],
                mendeley_data['research_group']
            )

            # Check the database configuration
            db_data = cfg['database']
            if 'engine' not in db_data:
                missing_attribute('database.engine')

            engine = db_data['engine']
            if engine == 'mysql':
                if 'hostname' not in db_data:
                    missing_attribute('database[mysql].hostname')
                if 'port' not in db_data:
                    missing_attribute('database[mysql].port')
                if 'db' not in db_data:
                    missing_attribute('database[mysql].db')
                if 'user' not in db_data:
                    missing_attribute('database[mysql].user')
                if 'secret' not in db_data:
                    missing_attribute('database[mysql].secret')
                self._database = MySQLConfiguration(
                    engine=db_data['engine'],
                    hostname=db_data['hostname'],
                    port=db_data['port'],
                    db=db_data['db'],
                    user=db_data['user'],
                    secret=db_data['secret']
                )
            elif engine == 'sqlite':
                if 'path' not in db_data:
                    missing_attribute('database[sqlite].path')
                self._database = SQLiteConfiguration(
                    engine=db_data['engine'],
                    path=db_data['path'],
                )
            else:
                raise InvalidConfigurationException("Database engine %s is not supported" % engine)
