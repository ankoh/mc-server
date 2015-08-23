__author__ = 'kohn'

from os.path import exists
from mendeleycache.utils.files import get_path
from mendeleycache.utils.exceptions import InvalidConfigurationException
import yaml


class MendeleyConfiguration:
    """
    Configuration of the Mendeley API app access
    """
    def __init__(self, app_id: str, app_secret: str, research_group: str):
        self.__app_id = app_id
        self.__app_secret = app_secret
        self.__research_group = research_group

    @property
    def app_id(self):
        return self.__app_id
    @property
    def app_secret(self):
        return self.__app_secret
    @property
    def research_group(self):
        return self.__research_group


class DatabaseConfiguration:
    """
    Configuration of the database access
    """
    def __init__(self, engine: str, ):
        self.__engine = engine

    @property
    def engine(self):
        return self.__engine


class MySQLConfiguration(DatabaseConfiguration):
    def __init__(self, engine: str, hostname: str, port: str, db: str, user: str, secret: str):
        self.__hostname = hostname
        self.__port = port
        self.__db = db
        self.__user = user
        self.__secret = secret
        super(MySQLConfiguration, self).__init__(engine)

    @property
    def hostname(self):
        return self.__hostname

    @property
    def port(self):
        return self.__port

    @property
    def db(self):
        return self.__db

    @property
    def user(self):
        return self.__user

    @property
    def secret(self):
        return self.__secret


class SQLiteConfiguration(DatabaseConfiguration):
    def __init__(self, engine: str, path: str):
        self.__path = path
        super(SQLiteConfiguration, self).__init__(engine)

    @property
    def path(self):
        return self.__path


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
        self.__mendeley = None
        self.__database = None
        self.__general = None

    @property
    def mendeley(self):
        return self.__mendeley

    @property
    def database(self):
        return self.__database

    def load(self):
        """
        The load function loads the configuration from disk
        It returns nothing but raises InvalidConfigurationExceptions if something is missing
        :return:
        """

        # Construct a file path relative to the project root
        # TODO: we could also allow an (absolute) path parameter
        path = get_path('config.yml')

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
            self.__mendeley = MendeleyConfiguration(
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
                self.__database = MySQLConfiguration(
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
                self.__database = SQLiteConfiguration(
                    engine=db_data['engine'],
                    path=db_data['path'],
                )
            else:
                raise InvalidConfigurationException("Database engine %s is not supported" % engine)
