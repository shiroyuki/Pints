'''
Base Controllers
================

:Author: Juti Noppornpitak <jnopporn@shiroyuki.com>
'''

import json
from re   import compile as RegExp

from tori            import __version__
from tori.controller import Controller     as BaseController
from tori.controller import RestController as BaseRestController

from pints.base.metadata import metadata

class Controller(BaseController):
    def __init__(self, *args, **kwargs):
        BaseController.__init__(self, *args, **kwargs)

        self.user        = self.session('user')
        self.transformer = self.component('data_transformer')
        self.params      = self.transformer.simplify(self.request.arguments)

    def authenticated(self):
        return self.user is not None

    def render(self, template_name, **contexts):
        contexts.update(metadata)

        if 'authenticated' not in contexts:
            contexts['authenticated'] = self.authenticated()

        if 'current_user' not in contexts:
            contexts['current_user'] = self.transformer.convert_entity_to_dict(self.user)

        BaseController.render(self, template_name, **contexts)

class RestController(BaseRestController):
    def __init__(self, *args):
        BaseRestController.__init__(self, *args)

        self.user        = self.session('user')
        self.transformer = self.component('data_transformer')
        self.params      = self.transformer.simplify(self.request.arguments)

    def authenticated(self):
        return self.user is not None

    def default_content_type(self):
        return 'application/json'

    def respond(self, serializable_data):
        self.set_header('Content-Type', self.default_content_type())
        self.write(json.dumps(serializable_data))

class EntityController(RestController):
    re_identifier = RegExp('[\`\~\!\@\#\$\%\^\&\*\(\)\_\+\-\=\{\}\|\\\[\];\'\"\<\>\?\/\s\.]+')

    def __init__(self, *args):
        RestController.__init__(self, *args)

        self.service        = self.component(self.service_identifier())
        self.user_directory = self.component('security.db.user')

        assert self.service is not None, 'Entity Service "%s" is not found.' % self.service_identifier()

    def service_identifier(self):
        return 'unknown'

    def entity_alias_column_name(self):
        return 'alias'

    def entity_name_column_name(self):
        return 'name'

    def _get_entity(self, id):
        entity = self.service.get(id)

        if not entity:
            self.set_status(404)
            return False

        return entity

    def list(self):
        db_entities = self.service.get_all()
        entities    = []

        for db_entity in db_entities:
            entities.append(self.transformer.convert_entity_to_dict(db_entity))

        self.respond(entities)

    def retrieve(self, id):
        entity = self._get_entity(id)

        if not entity: return

        self.respond(
            self.transformer.convert_entity_to_dict(entity)
        )

    def create(self):
        if not self.authenticated():
            return self.set_status(403)

        alias = self.entity_alias_column_name()

        if alias not in self.params:
            self.params[alias] = self.params[self.entity_name_column_name()].lower()

        # Retrieve the user ID first. THe default is the current user.
        owner = self.user.id

        if 'owner' in self.params and self.params['owner']:
            owner = self.params['owner']

        # Look up for the user ID
        owner                = self.user_directory.get(owner)
        self.params['owner'] = self.service.session().merge(owner)

        if not owner:
            return self.set_status(405)

        if self.re_identifier.search(self.params[alias]):
            self.params[alias] = self.re_identifier.\
                sub('-', self.params[alias]).\
                lower()

        entity = self.service.make(**self.params)

        self.set_status(
            self.service.post(self.service.make(**self.params))
            and 200
            or  400
        )

        self.service.session().close()
        self.user_directory.session().close()

    def remove(self, id):
        entity = self._get_entity(id)

        if not entity: return

        self.service.delete(entity)

    def update(self, id):
        entity = self._get_entity(id)

        if not entity: return

        alias = self.entity_alias_column_name()

        if alias in self.params and self.re_identifier.search(self.params[alias]):
            self.params[alias] = self.re_identifier.\
                sub('-', self.params[alias]).\
                lower()

        attribute_names = dir(entity)

        for attribute_name, attribute_value in self.params.iteritems():
            if attribute_name not in attribute_names:
                self.set_status(400)
                return

            entity.__setattr__(attribute_name, attribute_value)

        self.set_status(
            self.service.put()
            and 200
            or  500
        )
