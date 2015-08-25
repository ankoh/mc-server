__author__ = 'kohn'

from mendeleycache.analyzer.unification import unify_profile_name, unify_field_title, unify_document_title
from mendeleycache.models import CacheDocument, CacheField, CacheProfile, Profile, Document, CacheUnknownProfile
from mendeleycache.analyzer.validator import is_field_tag


class AnalysisController:
    """
    The AnalysisController is used to do the essential work of the MendeleyCache server
    it works on the crawled documents && profiles and merges duplicates + identifies research fields
    """

    def __init__(self):
        self._profiles = []
        self._profile_docs = {}
        self._group_docs = []

        # unified_name_to_profiles maps unified person names to their profiles to eliminate duplicates
        self._unified_name_to_profiles = dict()

        # unified_name_to_unknown_profiles maps unified person names to unknown profiles in the
        # document processing phase eventually dummy profiles will be added for those as well
        self._unified_name_to_unknown_profile = dict()

        # unified_name_to_authored_documents maps unified person names to the authored document titles
        # (resolved via get_documents_by_profile_id)
        self._unified_name_to_authored_documents = dict()

        # unified_name_to_participated_documents maps unified person names to document titles where the name appeared
        # in the "authors" list
        self._unified_name_to_participated_documents = dict()

        # unified_document_title_to_documents maps unified document titles to document objects
        self._unified_document_title_to_documents = dict()

        # unified_field_title_to_fields maps unified field titles to field objects
        self._unified_field_title_to_field = dict()

        # unified_field_title_to_documents maps unified field titles to unified document titles
        self._unified_field_title_to_documents = dict()

    @property
    def unified_name_to_profiles(self):
        return self._unified_name_to_profiles

    @property
    def unified_name_to_unknown_profile(self):
        return self._unified_name_to_unknown_profile

    @property
    def unified_name_to_authored_documents(self):
        return self._unified_name_to_authored_documents

    @property
    def unified_name_to_participated_documents(self):
        return self._unified_name_to_participated_documents

    @property
    def unified_document_title_to_documents(self):
        return self._unified_document_title_to_documents

    @property
    def unified_field_title_to_field(self):
        return self._unified_field_title_to_field

    @property
    def unified_field_title_to_documents(self):
        return self._unified_field_title_to_documents

    def prepare(self, profiles, profile_docs, group_docs):
        """
        Prepare the AnalysisController with data
        :param profiles:
        :param profile_docs
        :param group_docs:
        :return:
        """
        self._profiles = profiles
        self._profile_docs = profile_docs
        self._group_docs = group_docs

    def process_profiles(self):
        """
        Iterates over the profiles and finds duplicates
        :return:
        """
        for profile in self._profiles:
            unified, real = unify_profile_name(profile.first_name, profile.last_name)

            # Check if the name is already stored in the profiles
            # Then store the additional profile
            existing_profiles = []
            if unified in self._unified_name_to_profiles:
                existing_profiles = self._unified_name_to_profiles[unified]
            existing_profiles.append(profile)
            self._unified_name_to_profiles[unified] = existing_profiles

            # Store empty entries in documents maps for that profile
            # (then we don't need to check the key every time)
            self._unified_name_to_authored_documents[unified] = set()
            self._unified_name_to_participated_documents[unified] = set()

    def analyze_author(self, doc_unified: str, author: (str, str)):
        """
        Given a unified document title and an author tuple (first_name, last_name) tries to find a matching profile
        Adds an UnknownProfile if unsuccessful
        :param doc_unified:
        :param author:
        :return:
        """
        # Build the unified name of the found core_author
        author_unified, author_real = unify_profile_name(author[0], author[1])

        # Check if the found author is already linked to a profile
        if author_unified in self._unified_name_to_profiles:
            # If yes, append the doc title to the participated_documents of this author
            participated_docs = self._unified_name_to_participated_documents[author_unified]
            participated_docs.add(doc_unified)
        else:
            # If not, check if there is already an unknown_profile for this unified name
            # If not, create one
            if author_unified not in self._unified_name_to_unknown_profile:
                self._unified_name_to_unknown_profile[author_unified] = CacheUnknownProfile(
                    name=author_real, unified_name=author_unified)
                # Add document to participated_documents
                participated_docs = set()
                participated_docs.add(doc_unified)
                self._unified_name_to_participated_documents[author_unified] = participated_docs
            else:
                # The profile exists -> only add doc to participated_documents
                participated_docs = self._unified_name_to_participated_documents[author_unified]
                participated_docs.add(doc_unified)

    def analyze_field_tag(self, doc_unified: str, tag: str):
        """
        Given a unified document title and a tag, tries to identify a research field
        Updates references accordingly
        :param doc_unified:
        :param tag:
        :return:
        """
        if not is_field_tag(tag):
            return

        # Build the unified name of the found research field tag
        field_unified, field_real = unify_field_title(tag)

        # Check if that research field already exists
        if field_unified in self._unified_field_title_to_field:
            # If yes check if it (CacheField) needs to be updated
            existing_field = self._unified_field_title_to_field[field_unified]
            if len(existing_field.title) < len(field_real):
                existing_field.title = field_real
            existing_field_docs = self._unified_field_title_to_documents[field_unified]
            existing_field_docs.add(doc_unified)
        else:
            # If not add a new CacheField and create a new list for field_to_docs
            self._unified_field_title_to_field[field_unified] = CacheField(
                title=field_real, unified_title=field_unified)
            field_documents = set()
            field_documents.add(doc_unified)
            self._unified_field_title_to_documents[field_unified] = field_documents

    def process_profile_documents(self):
        """
        Iterates over the profile documents, finds research fields, finds duplicates, finds author profiles
        :return:
        """
        for profile_unified in self._unified_name_to_profiles:

            # Check if the profile identifier has stored documents
            if profile_unified not in self._profile_docs:
                # TODO: Log warning for analysis report
                continue

            # Process these documents
            docs = self._profile_docs[profile_unified]
            for doc in docs:
                # Create unified document title
                doc_unified, doc_real = unify_document_title(doc.core_title)

                # Add document to docs
                if doc_unified in self._unified_document_title_to_documents:
                    existing_docs = self._unified_document_title_to_documents[doc_unified]
                    existing_docs.append(doc)
                else:
                    self._unified_document_title_to_documents[doc_unified] = [doc]

                # Append the doc title to the authored_docs of that unified profile name
                authored_docs = self._unified_name_to_authored_documents[profile_unified]
                authored_docs.add(doc_unified)

                # Process core_authors field of the doc to find participants
                for author in doc.core_authors:
                    self.analyze_author(doc_unified, author)

                # Analyze the tags fields of the doc to find research fields
                for tag in doc.tags:
                    self.analyze_field_tag(doc_unified, tag)

    def process_group_documents(self):
        """
        Iterates over the group documents, finds research fields, finds duplicates, finds author profiles
        :return:
        """
        for doc in self._group_docs:
            # Create unified document title
            doc_unified, doc_real = unify_document_title(doc.core_title)

            # Add document to docs
            if doc_unified in self._unified_document_title_to_documents:
                existing_docs = self._unified_document_title_to_documents[doc_unified]
                existing_docs.append(doc)
            else:
                self._unified_document_title_to_documents[doc_unified] = [doc]

            # Try to find the main owner of the document through the document profile_id
            # If not existent do nothing
            # (we can't do much only with the profile_id.
            # We could post-fetch the unknown profiles but that is more involved)
            profile_id = doc.core_profile_id
            if profile_id in self._profiles:
                profile = self._profiles[profile_id]
                unified_name, real_name = unify_profile_name(profile.first_name, profile.last_name)
                if unified_name in self._unified_name_to_authored_documents:
                    authored_documents = self._unified_name_to_authored_documents[unified_name]
                    authored_documents.add(doc_unified)

            # Process core_authors field of the doc to find participants
            for author in doc.core_authors:
                self.analyze_author(doc_unified, author)

            # Analyze the tags fiels of the doc to find research fields
            for tag in doc.tags:
                self.analyze_field_tag(doc_unified, tag)

    def execute(self):
        """
        Process all input
        :return:
        """
        self.process_profiles()
        self.process_profile_documents()
        self.process_group_documents()
