'''
..warning:: Security is not implemented here.
'''

from pints.base.controller import Controller, EntityController

class ProjectInterface(EntityController):
    def service_identifier(self):
        return 'app.db.project'

    def entity_alias_column_name(self):
        return 'codename'

class ReminderInterface(EntityController):
    def service_identifier(self):
        return 'app.db.reminder'

    def entity_name_column_name(self):
        return 'summary'

class ReminderConnectionInterface(Controller):
    _field_to_service_map = {
        'assignees' : 'security.db.user',
        'projects'  : 'app.db.project'
    }

    def service_identifier(self):
        return 'reminders'

    def list(self, primary_id, field):
        ''' Retrieve the list of all entities. '''
        self.set_status(405)

    def retrieve(self, primary_id, field, secondary_id):
        ''' Retrieve an entity with `id`. '''
        self.set_status(405)

    def create(self, primary_id, field):
        ''' Create an entity. '''
        self.set_status(405)

    def remove(self, primary_id, field, secondary_id):
        ''' Remove an entity with `id`. '''
        self.set_status(405)

    def update(self, primary_id, field, secondary_id):
        ''' Update an entity with `id`. '''
        self.set_status(405)

    # Internal routing

    def get(self, primary_id, field, secondary_id=None):
        ''' Handle GET requests. '''
        if not secondary_id:
            self.list(primary_id, field)
            return

        self.retrieve(int(primary_id), field, int(secondary_id))

    def post(self, primary_id, field, secondary_id=None):
        ''' Handle POST requests. '''
        if secondary_id:
            self.set_status(405)
            return

        self.create(int(primary_id), field)

    def put(self, primary_id, field, secondary_id=None):
        ''' Handle PUT requests. '''
        if not secondary_id:
            self.set_status(405)
            return

        self.update(int(primary_id), field, int(secondary_id))

    def delete(self, primary_id, field, secondary_id=None):
        ''' Handle DELETE requests. '''
        if secondary_id:
            self.set_status(405)
            return

        self.remove(int(primary_id), field, int(secondary_id))
