__author__ = 'kohn'

from dateutil.parser import parse
import datetime


class Member:
    """
    Class that represents a member of a group via profile_id, a join date and a role
    """
    def __init__(self,
                 profile_id: str,
                 joined: datetime,
                 role: str):
        self.__profile_id = profile_id
        self.__joined = joined
        self.__role = role

    @property
    def profile_id(self) -> str:
        return self.__profile_id

    @property
    def joined(self) -> datetime:
        return self.__joined

    @property
    def role(self) -> str:
        return self.__role


class Document:
    """
    Class that represents the core attributes of a single document.
    As this application will make heavy use of tags and bibtex, those are stored as well
    """
    def __init__(self,
                 core_id: str,
                 core_profile_id: str,
                 core_title: str,
                 core_type: str,
                 core_created: datetime,
                 core_last_modified: datetime,
                 core_abstract: str,
                 core_source: str,
                 core_year: int,
                 core_authors: [(str, str)],
                 core_identifiers: [(str, str)],
                 core_keywords: [str],
                 tags: [str]):
        self.__core_id = core_id
        self.__core_profile_id = core_profile_id
        self.__core_title = core_title
        self.__core_type = core_type
        self.__core_created = core_created
        self.__core_last_modified = core_last_modified
        self.__core_abstract = core_abstract
        self.__core_source = core_source
        self.__core_year = core_year
        self.__core_authors = core_authors
        self.__core_identifiers = core_identifiers
        self.__core_keywords = core_keywords
        self.__tags = tags

    @property
    def core_id(self) -> str:
        return self.__core_id

    @property
    def core_profile_id(self) -> str:
        return self.__core_profile_id

    @property
    def core_title(self) -> str:
        return self.__core_title

    @property
    def core_type(self) -> str:
        return self.__core_type

    @property
    def core_created(self) -> datetime:
        return self.__core_created

    @property
    def core_last_modified(self) -> datetime:
        return self.__core_last_modified

    @property
    def core_abstract(self) -> str:
        return self.__core_abstract

    @property
    def core_source(self) -> str:
        return self.__core_source

    @property
    def core_year(self) -> int:
        return self.__core_year

    @property
    def core_authors(self) -> [(str, str)]:
        return self.__core_authors

    @property
    def core_identifiers(self) -> [(str, str)]:
        return self.__core_identifiers

    @property
    def core_keywords(self) -> [str]:
        return self.__core_keywords

    @property
    def tags(self) -> [str]:
        return self.__tags


class Profile:
    """
    Class that respresents a single author profile
    """
    def __init__(self,
                 identifier: str,
                 first_name: str,
                 last_name: str,
                 display_name: str,
                 link: str):
        self.__identifier = identifier
        self.__first_name = first_name
        self.__last_name = last_name
        self.__display_name = display_name
        self.__link = link

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def display_name(self) -> str:
        return self.__display_name

    @property
    def link(self) -> str:
        return self.__link
