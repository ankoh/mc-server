__author__ = 'kohn'

from mendeleycache.config import ServiceConfiguration
import sqlalchemy


def create_engine(config: ServiceConfiguration):
    if config.database.engine == "mysql":
        pass
    elif config.database.engine == "sqlite":
        pass
    else:
        # TODO: Log warning
        return None
