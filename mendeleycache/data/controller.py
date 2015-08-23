__author__ = 'kohn'

from mendeleycache.data.config import create_engine
from mendeleycache.config import DatabaseConfiguration


class DataController:
    """
    The DataController provides access to the engine
    """

    def __init__(self, config: DatabaseConfiguration):
        self._config = config
        self._engine = create_engine(self._config)

    @property
    def engine(self):
        """
        Return the initialized database engine
        :return:
        """
        return self._engine
