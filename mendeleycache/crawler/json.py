__author__ = 'kohn'

from mendeleycache.utils.reflection import get_class_attributes, get_default, get_dict_if_key_exists
from mendeleycache.models import Document, Profile, Member
from dateutil.parser import parse
from datetime import date


def get_members_from_json(json_data) -> [Member]:
    result = []
    for element in json_data:
        m = get_member_from_json(element)
        if m.role != 'follower':
            result.append(m)
    return result


def get_member_from_json(json_data) -> Member:
    identifier = json_data['profile_id']
    role = json_data['role']
    joined = parse(json_data['joined'])
    return Member(identifier, joined, role)


def get_profile_from_json(json_data) -> Profile:
    identifier = json_data['id']
    first_name = json_data['first_name']
    last_name = json_data['last_name']
    display_name = json_data['display_name']
    link = json_data['link']
    return Profile(identifier, first_name, last_name, display_name, link)


def get_document_from_json(json_doc) -> Document:
    """
    Given a json object return a Document object
    :param json_doc:
    :return:
    """
    # Core attributes
    core_id = json_doc['id']
    core_profile_id = json_doc['profile_id']
    core_title = json_doc['title']
    core_type = get_default(json_doc, 'type', 'conference_proceedings')
    core_created = parse(json_doc['created'])
    core_last_modified = parse(json_doc['last_modified'])
    core_year = int(get_default(json_doc, 'year', date.today().year))
    core_abstract = get_default(json_doc, 'abstract', "")
    core_source = get_default(json_doc, 'source', "")

    # Core tuples
    core_authors = []
    core_keywords = []
    tags = []

    for author in get_dict_if_key_exists(json_doc, 'authors'):
        first_name = get_default(author, 'first_name', "")
        last_name = get_default(author, 'last_name', "")
        core_authors.append((first_name, last_name))

    for keyword in get_dict_if_key_exists(json_doc, 'keywords'):
        core_keywords.append(keyword)

    for tag in get_dict_if_key_exists(json_doc, 'tags'):
        tags.append(tag)

    # Append new document to result list
    return Document(
        core_id=core_id,
        core_profile_id=core_profile_id,
        core_title=core_title,
        core_type=core_type,
        core_created=core_created,
        core_last_modified=core_last_modified,
        core_abstract=core_abstract,
        core_source=core_source,
        core_year=core_year,
        core_authors=core_authors,
        core_keywords=core_keywords,
        tags=tags
    )