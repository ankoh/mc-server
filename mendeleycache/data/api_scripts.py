__author__ = 'kohn'

from sqlalchemy.engine import Engine


class ApiScripts:
    def __init__(self, engine: Engine):
        self._engine = Engine

    def get_documents_by_profile_ids_and_field_ids(self, profile_ids: [int], field_ids: [int]):
        """
        Given profile ids and field ids, queries all documents that belong to the research field
        AND are associated with these profiles
        :return:
        """
        pass


    def get_profiles_by_profile_ids_or_field_ids(self, profile_ids: [int], field_ids: [int], slim: bool):
        """
        Given a list of profile ids and field ids, queries all documents that belong to the research field
        OR are associated with these profiles.
        Futher:
            - slim=true returns a slim version of the profiles for faster network transmission
            - empty lists result in ALL profiles
        :param slim:
        :return:
        """
        pass


    def get_fields(self):
        """
        Queries all research fields
        :return:
        """
        pass


    def get_general_statistics(self):
        """
        Queries the access logs to get the statistics of the past seven weeks (grouped by week)
        :return:
        """
        pass
