'''
..warning:: Security is not implemented here.
'''

from pints.base.controller import EntityRestController

class ProjectInterface(EntityRestController):
    def service_identifier(self):
        return 'projects'
    
    def entity_alias_column_name(self):
        return 'codename'

class RemainderInterface(EntityRestController):
    def service_identifier(self):
        return 'reminders'
    
    def entity_name_column_name(self):
        return 'summary'

