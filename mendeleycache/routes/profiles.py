__author__ = 'kohn'

from flask import Flask, request

from mendeleycache.utils.json_encoder import DefaultEncoder
from mendeleycache.data.controller import DataController
from mendeleycache.config import CacheConfiguration
from mendeleycache.logging import log
import re
import json


class ProfilesController:
    def __init__(self, app: Flask, data_controller: DataController, cache_config: CacheConfiguration):
        self._app = app
        self._data_controller = data_controller
        self._cache_config = cache_config

    def register(self):
        self._app.add_url_rule('/profile/page/', methods=['GET'], view_func=self.get_profile_page)
        self._app.add_url_rule('/profiles/', methods=['GET'], view_func=self.get_profiles)

    def get_profile_page(self):
        """
        Searches a profile page
        ATTENTION: At the moment only first_name, last_name queries are supported.
        ID queries could be easily added though
        :return:
        """
        log.info('The route GET /profile/page/ has been triggered')

        if 'first_name' in request.args:
            first_name = request.args['first_name']
            log.debug('Query parameter "first_name" = %s' % first_name)
        else:
            return json.dumps({"error": "You need to provide the query parameter first_name"}, cls=DefaultEncoder), 400

        if 'last_name' in request.args:
            last_name = request.args['last_name']
            log.debug('Query paramter "last_name" = %s' % last_name)
        else:
            return json.dumps({"error": "You need to provide the query parameter last_name"}, cls=DefaultEncoder), 400

        if self._data_controller.api_data.profile_exists(first_name, last_name):
            url = self._cache_config.profile_page_pattern
            url = re.sub(':firstname', first_name, url)
            url = re.sub(':lastname', last_name, url)
            return json.dumps({"url": url}, cls=DefaultEncoder), 200
        else:
            return json.dumps({"error": "No profile found"}, cls=DefaultEncoder), 404


    def get_profiles(self):
        log.info('The route GET /profiles/ has been triggered')

        # Default parameters
        profile_ids = ''
        field_ids = ''
        slim = False

        # Set passed query parameters if existing
        if 'profile-ids' in request.args:
            profile_ids = request.args['profile-ids'].split(',')
            log.debug('Query parameter "profile-ids" = %s' % profile_ids)
        if 'field-ids' in request.args:
            field_ids = request.args['field-ids'].split(',')
            log.debug('Query parameter "field_ids" = %s' % field_ids)
        if 'slim' in request.args:
            slim = bool(request.args['slim'])
            log.debug('Query parameter "slim" = %s' % slim)

        # Trigger the respective methods
        profiles = []
        if slim:
            profiles = self._data_controller.api_data.get_profiles_slim()
        else:
            profiles = self._data_controller.api_data.get_profiles_by_profile_ids_or_field_ids(
                profile_ids=profile_ids,
                field_ids=field_ids
            )

        # Serialize documents
        response = []
        for profile in profiles:
            profile_dict = dict(profile.items())
            response.append(profile_dict)
        return json.dumps(response, cls=DefaultEncoder)
