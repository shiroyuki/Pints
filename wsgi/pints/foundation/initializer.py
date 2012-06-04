from kotoba             import load_from_file
from sqlalchemy.orm.exc import NoResultFound

from pints.security.model   import Group, User, GroupUserManagement, GroupUserManagementLevel
from pints.security.service import Registration

class Initializer(object):
    def __init__(self, db):
        self.db = db
        
        self.registration_service = Registration(self.db)
    
    def get_by_alias(self, kind, alias):
        try:
            session = self.db.session()
            
            return session.query(kind).filter_by(alias=alias).one()
        except NoResultFound:
            return None
    
    def get_groups(self, xml):
        group_xml_list = xml.find('groups group')
        
        # Create default data.
        groups = {
            'root':   Group(name = 'Root',   alias = 'root'),
            'public': Group(name = 'Public', alias = 'public')
        }
        
        # Added any additional groups.
        for group_xml in group_xml_list:
            group = {
                'alias': group_xml.attribute('alias'),
                'name':  group_xml.data()
            }
            
            assert group['alias'] and group['name']
            
            if group['alias'] in groups:
                raise KeyError, 'Group "%s" is duplicated in the initial directory data.' % alias
            
            groups[group['alias']] = Group(**group)
        
        return groups
    
    def get_users(self, xml):
        user_xml_list  = xml.find('users user')
        
        # Create default data.
        users = {}
        
        # Added users.
        for user_xml in user_xml_list:
            user = {
                'alias': user_xml.attribute('alias'),
                'email': None
            }
            
            required_fields = user.keys()
            
            for field in user_xml.children():
                user[field.name()] = field.data()
            
            for key in required_fields:
                assert user[key]
            
            if user['alias'] in users:
                raise KeyError, 'User "%s" is duplicated in the initial directory data.' % alias
            
            users[user['alias']] = self.registration_service.make_user(**user)
        
        return users
    
    def load(self, initial_directory_data_location):
        xml = load_from_file(initial_directory_data_location)
        
        queued_entities = self.get_groups(xml).values() + self.get_users(xml).values()
        
        entities = []
        
        for queued_entity in queued_entities:
            registered_entity = self.get_by_alias(queued_entity.__class__, queued_entity.alias)
            
            if registered_entity: return
            
            entities.append(queued_entity)
        
        self.db.post(*entities)
        
        return entities