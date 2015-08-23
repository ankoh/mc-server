__author__ = 'kohn'

from mendeleycache.config import DatabaseConfiguration, MySQLConfiguration, SQLiteConfiguration
import sqlalchemy
from sqlalchemy.engine import Engine


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
        path = "sqlite://"
        if config.path:
            path += config.path
    else:
        # TODO: Log warning
        return None

    return sqlalchemy.create_engine(path)
