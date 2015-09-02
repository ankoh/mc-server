__author__ = 'kohn'

import unicodedata
import re


"""
I'll cap the unified strings at 150 chars.
Should be definitely enough to get unique names
http://stackoverflow.com/questions/4715415/base64-what-is-the-worst-possible-increase-in-space-usage
"""

def unify_document_title(title: str) -> (str, str):
    """
    Unifies a document title
    :param title:
    :return:
    [0] contains the unified title
    [1] contains the potentially slightly modified real title
    """

    # Remove all spaces and convert to lowercase
    unified_title = title.replace(" ","").lower()
    # Now remove all these unneeded ugly symbols
    unified_title = re.sub('[-_.,:;\|/\{\}\(\)\[\]\'\"\+]','', unified_title)
    trimmed_unified_title = unified_title[:150]
    return trimmed_unified_title, title


def unify_field_title(title: str):
    """
    Unifies a research field title (tag)
    :param title:
    :return:
    [0] contains the unified title
    [1] contains the derived real title
    """

    # Convert to lowercase
    prep_title = title.lower()
    # Now remove all these unneeded ugly symbols
    prep_title = re.sub('[.,:;\|/\{\}\(\)\[\]\'\"\+]','', prep_title)
    # Replace multiple whitespaces with one
    prep_title = re.sub(' +', ' ', prep_title)

    # The real title is now the replacement of dashes with whitespace
    real_title = prep_title.title()
    # The unified title is the removal of the dashes and whitespace
    unified_title = re.sub('[ \-]','', prep_title)
    trimmed_unified_title = unified_title[:150]
    return trimmed_unified_title, real_title


def unify_profile_name(first_name: str, last_name: str):
    """
    Unifies a profile name
    :param first_name:
    :param last_name:
    :return:
    [0] contains the unified name
    [1] contains the potentially slightly modified real name
    """
    concat_title = first_name + " " + last_name
    # Strip leading and trailing spaces and then replace double white space two times
    # (3 -> 2 -> 1)
    concat_title = concat_title.strip().replace("  ", " "). replace("  ", " ")

    # The unified title is again the lowercase version without spaces
    unified_title = concat_title.replace(" ", "").lower()
    unified_title = re.sub('[-_.,:;\|/\{\}\(\)\[\]\'\"\+]','', unified_title)
    trimmed_unified_title = unified_title[:150]
    return trimmed_unified_title, concat_title
